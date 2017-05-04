#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import jnpr.junos.exception
import os
import sys
import getpass
import argparse
import socket

# Parser configuration
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="allows you to add a list of IPs separated by spaces")
parser.add_argument("-f", "--fqdn", help="allows you to add list of FQDNs separated by spaces")
parser.add_argument("-l", "--load", help="add the path to a file containing target FQDNs or IPs")
parser.add_argument('hosts', nargs='*')
args = parser.parse_args()


def main(args, argv):
    # Check if any arguments were added
    if len(argv) == 1:
        '''
        I will add a function to load a list from a file or entering FQDNs manually,
        for now you need to add them as arguments.
        '''
        print("please use --help or -h to learn how to use this script")
    else:
        print("---")
        devices = sys.argv[2:]
        if args.fqdn:
            print("Validating FQDNs:")
            for fqdn in devices:
                try:
                    print(fqdn, "--> ", end="")
                    sys.stdout.flush()
                    print(socket.gethostbyname(fqdn))
                except socket.error:
                    print("error:", fqdn, "is not resolvable!")
                    exit()
        elif args.ip:
            print("Validating IPs:")
            for ip in devices:
                try:
                    print(ip, "...", end="")
                    sys.stdout.flush()
                    socket.inet_aton(ip)
                    print("ok")
                except socket.error:
                    print("error:", ip, "is not a valid IP-address!")
                    exit()
        elif args.load:
            print("loading file from", sys.argv[2], "...", end="")
            sys.stdout.flush()
            devices = open(sys.argv[2]).read().splitlines()
            print("done")
        # If neither --ip or --fqdn is added as the first argument exit the script
        else:
            print("please use --help or -h to learn how to use this script")
            exit()
        print("---")
        print("Please enter your username and password: ")
        # Ask for user input of the username
        username = input('Username: ')
        # Ask for hidden(no echo to shell) user input of the password
        password = getpass.getpass('Password: ')
        print("---")
        # Set cwd to the path of the current working direcotry of the user executing the script
        cwd = os.getcwd()

        def locate_file():
            dir = input('Is the configuration file in the same directory as this script? (y/n): ').lower()
            if dir == 'y':
                name = input('Please enter the _exact_ name of the config file: ')
                if os.path.isfile(os.path.join(cwd, name)) is True:
                    print("---")
                    return name
                else:
                    print("No file with the name", name, "exists in this directory.(check permissions!)")
                    exit()
            elif dir == 'n':
                path = input('Please enter the exact path to the config file: ')
                if os.path.isfile(path) is True:
                    return path
                else:
                    print("No such file exists at", path, "(check permissions)!")
                    exit()
            else:
                print("Sorry...the file must me on this system. I can not load remote files (yet!)")
                exit()

        def netconf(file_path, conf_method):
            for idx, fqdn in enumerate(devices):
                try:
                    dev = Device(host=fqdn, user=username, password=password, normalize=True)
                    print(fqdn, ": connecting...", end="")
                    sys.stdout.flush()
                    dev.open()
                    print("done")
                    dev.timeout = 300
                    print(fqdn, ": entering configuration mode...", end="")
                    sys.stdout.flush()
                    cfg = Config(dev)
                    print("done")
                    print(fqdn, ": entering exclusive configuration mode...", end="")
                    sys.stdout.flush()
                    try:
                        cfg.lock()
                        print("done")
                    except jnpr.junos.exception.LockError as err:
                        print("error: " + repr(err))
                        exit()
                    print(fqdn, ": loading the configuration file...", end="")
                    sys.stdout.flush()
                    try:
                        cfg.load(path=file_path, format=conf_method, merge=True)
                        print("done")
                    except jnpr.junos.exception.ConfigLoadError as err:
                        print("error: " + repr(err))
                        exit()
                    print(fqdn, ": checking the configuration for errors...", end="")
                    sys.stdout.flush()
                    try:
                        cfg.commit_check()
                        print("done")
                    except jnpr.junos.exception.CommitError as err:
                        print("error: " + repr(err))
                        print(fqdn, ": rolling back configuration...", end="")
                        sys.stdout.flush()
                        try:
                            cfg.rollback(rb_id=0)
                            print("done")
                        except jnpr.junos.exception.SwRollbackError as err:
                            print("error: " + repr(err))
                            print("Please login to", fqdn, "and rollback the configuration manually!")
                            exit()
                    print("---")
                    print("Do you want to make the following changes:")
                    cfg.pdiff()
                    print("---")
                    askForCommit = input("Commit changes? (y/n): ").lower()
                    if askForCommit == 'y':
                        print(fqdn, ": running commit...", end="")
                        sys.stdout.flush()
                        try:
                            cfg.commit()
                            print("done")
                        except jnpr.junos.exception.CommitError as err:
                            print("error: " + repr(err))
                    else:
                        print(fqdn, ": rolling back configuration...", end="")
                        sys.stdout.flush()
                        try:
                            cfg.rollback(rb_id=0)
                            print("done")
                        except jnpr.junos.exception.SwRollbackError as err:
                            print("error: " + repr(err))
                    print(fqdn, ": exiting exclusive configuration mode...", end="")
                    sys.stdout.flush()
                    try:
                        cfg.unlock()
                        print("done")
                    except jnpr.junos.exception.UnlockError as err:
                        print("error: " + repr(err))
                    print(fqdn, ": closing connection...", end="")
                    sys.stdout.flush()
                    dev.close()
                    print("done")
                except jnpr.junos.exception.ConnectError as err:
                    print("error: " + repr(err))

        def convert(conf_method):
            if conf_method == 'snip':
                conf_method = "text"
                return conf_method
            elif conf_method == 'set':
                conf_method = "set"
                return conf_method
            else:
                print("oops. something went wront with the method you entered")
                exit()

        print("What configuration method would you like to use?")
        print("You can either use configuration 'snip'pets or 'set' commands")
        method = input('Please enter "snip" or "set": ')
        method = convert(method)
        conf_file = locate_file()
        netconf(conf_file, method)
        print("Exiting...")
        exit()


if __name__ == '__main__':
    main(args, sys.argv)
else:
    main(args, sys.argv)

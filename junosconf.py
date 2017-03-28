from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import os

router = {
        'test1': 'ENTER IP HERE',
        'test2': 'ENTER SECOND IP HERE'}

username = "ADD YOUR USERNAME HERE"
password = "ADD THE PASSWORD HERE"

cwd = os.getcwd()

print ("This script will update the configuration of the following Junos devices:")
print ("#######################")
for key,value in router.items():
    print(key,":", value)
print ("#######################")

def locate_file(dir):
    if dir == 'y':
        name = input('Please enter the _exact_ name of the file containing the config/commands: ')
        file_exists = os.path.isfile(os.path.join(cwd, name))
        if file_exists == True:
            return name
        else:
            print ("No file with the name",name,"exists in this directory. Please also check the file permissions!")
            exit()
    elif dir == 'n':
        path = input('Please enter the _exact_ path to the file containing the config/commands: ')
        path_exists = os.path.isfile(path)
        if path_exists == True:
            return path
        else:
            print ("No such file exists at",path,"(please also check the file permissions)!")
            exit()
    else:
        print ("Sorry...the file must me on this system. I can not load remote files (yet!)")
        exit()

def get_file(conf_method):
    dir = input('Is the configuration file in the same directory as this script? (y/n): ').lower()
    conf_file = locate_file(dir)
    return conf_file

def netconf(file_path,conf_method):
    for fqdn in router:                 
        dev = Device(host=router[fqdn], user=username, password=password)
        print (router[fqdn],": connecting...")
        dev.open()
        dev.timeout = 300
        print (router[fqdn],": connection established")
        cfg = Config(dev)
        print (router[fqdn],": loading configuration file")
        cfg.load(path=file_path,format=conf_method, merge=True)
        print (router[fqdn],": checking configuration for errors...")
        cfg.commit_check()
        print (router[fqdn],": running commit...")
        cfg.commit()
        print (router[fqdn],": commit successful")
        print (router[fqdn],": closing session...")
        dev.close()
        print (router[fqdn],": session closed")

def convert(conf_method):
    if conf_method == 'snip':
        conf_method = "text"
        return conf_method
    elif conf_method == 'set':
        conf_method = "set"
        return conf_method
    else:
        print ("oops. something went wront with the method you entered")

print ("What configuration method would you like to use?")
print ("You can either use configuration 'snip'pets or 'set' commands")
method = input('Please enter "snip" or "set": ')
method = convert(method)
conf_file = get_file(method)
netconf(conf_file,method)
print ("Exiting...")
exit()

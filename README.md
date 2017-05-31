# junosconf
A script to help getting information from devices running the Junos OS operating system or pushing configuration changes to them.

## Setup enviroment
- Python 3.x
- A device running Junos OS with NETCONF enabled and a user account configured with appropriate permissions
```
set system services netconf ssh
```

- Setup Junipers ["py-junos-eznc"](https://github.com/Juniper/py-junos-eznc)
The repo now comes preinstalled with junos-eznc and all dependencies in a virtualenv.
Feel free to use it, setup your own virtualenv or just use the globally installed modules on your system.
Checkout the requirements.txt file for more information what the dependencies are.

## Usage

Execute the script with either -i/--ip if you want to use IP-addresses or -f/--fqdn if you want to use FQDN's to connect to your devices.
After the first argument add a comma separated list of either IP's or FQDN's.

You can also load a file containing a list of targets/hosts (each host must be in a new line with no spaces in between).
You need to make sure that these are working hosts because the script doesn't resolv the FQDN's or validate the IP's for you.

The rest should be pretty much self explanatory, but I will a more detailed README later on.

## Examples

With FQDN's
```
./junosconf.py -f edge2.isp.com edge3.isp.com edge4.isp.com edge5.isp.com
```
or IP's
```
./junosconf.py -i 10.0.2.100 10.13.37.7 192.168.4.20 10.10.10.10
```
or a independent file with list of hosts
```
./junosconf.py -l ~/development/junosconf/examples/hosts/random_hosts
```

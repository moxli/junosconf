# junosconf
A script to help getting information from devices running the Junos OS operating system or pushing configuration changes to them.

## Setup enviroment
- Python 3.x
- A device running Junos OS with NETCONF enabled and a user account configured with appropriate permissions
```
set system services netconf ssh
```
- Setup Junipers ["py-junos-eznc"](https://github.com/Juniper/py-junos-eznc)

Install pip
```
sudo apt-get install python3-pip
```

Install dependencies
```
sudo pip install ncclient
sudo pip install Jinja2
sudo pip install lxml
sudo pip install netaddr
sudo pip install paramiko
sudo pip install scp
```

Install py-junos-eznc
```
sudo pip install junos-eznc
```

## Usage

At the current stage of the script you need to decide between the usage of IP-addresses or fully qualified domain names.

Execute the script with either one of these arguments:
If you want to use ip addresses add -i or --ip and if you want to use FQDN's add -f or --fqdn.
After the first argument add a comma separated list (just more arguments) of either IP's or FQDN's.

You can also load a file containing a list of targets/hosts (each host must be in a new line with no spaces in between).
You need to make sure that these are working hosts because the script doesn't resolv the FQDNs or validate the IPs.

The rest should be pretty much self explanatory, but I will a more detailed README later on.

## Example

With FQDN's
```
./junosconf.py -f edge2.isp.com edge3.isp.com edge4.isp.com edge5.isp.com
```
or IP's
```
./junosconf.py -i 10.0.2.100 10.13.37.7 192.168.4.20 10.10.10.10
```
With a independent file of hosts
```
./junosconf.py -l ~/development/junosconf/examples/just-a-bunch-of-ips
```

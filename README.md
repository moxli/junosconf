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

The first thing to do is writing your login credentials and the Junos device IP addresses in to the junosconf.py script

### Login credentials 
```
username = "ADD YOUR USERNAME HERE"
password = "ADD THE PASSWORD HERE"
```
### Junos device IP addresses
You can also add the FQDN/hostname/whatever in the key section of the dicitonary to identify the IP in the value section
```
router = {
        'test1': 'ENTER IP HERE',
        'test2': 'ENTER SECOND IP HERE'}
```

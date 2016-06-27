### Need
Update script provided by DuckDNS may not be useful as is for users on ACT broadband. DuckDNS's update API finds IP from request and updates it as IP for your domain. It works fine for most of the broadband providers. However, on ACT broadband, your router is behind couple of NATs and only NAT's IP is updated as your IP. Update API should be called along with your router's (actual) IP address.

### What is this script
This script identifies your actual IP address from portal.acttv.in portal and calls DuckDNS's update API. This script can be scheduled as cron job similar to the DuckDNS's default script.

### Usage
```python [script_name>].py -d [your domain] -t [your token]```
or for help
```python [script_name].py -h```

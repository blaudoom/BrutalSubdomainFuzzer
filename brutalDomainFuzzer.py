import requests, sys, time
from pathlib import Path

ip = sys.argv[1]
domain = sys.argv[2]
subdomainlist = sys.argv[3]

customerror=""
if(len(sys.argv) > 4):
	customerrorfilename = sys.argv[4]
	customerrorfile = open(customerrorfilename, 'r')
	customerror = customerrorfile.read()
	print('Custom error in use:\n'+customerror)

hosts = open('/etc/hosts','r')
hostlines = hosts.readlines()
backup = open('/etc/hosts_bkup','w')
backup.writelines(hostlines)
backup.close()
print("Backupfile of hosts written in /etc/hosts_bkup")


subdomainsfile = open(subdomainlist,'r')
subdomains = subdomainsfile.readlines()

print("||domain||response||custom errorfile returned?||")
for subdomain in subdomains:
	fulldomain = subdomain.strip()+'.'+domain
	resolvestring = ip +'\t'+fulldomain+'\n'
	hosts = open('/etc/hosts','a')
	hosts.write(resolvestring)
	hosts.close()
	response = requests.get('http://'+fulldomain)
	print("||"+fulldomain+"||"+str(response.status_code)+"||"+str(response.text.strip() == customerror.strip())+"||")
	if response.text.strip() != customerror.strip():

		Path("responses").mkdir(parents=True, exist_ok=True)
		responsefile = open('responses/'+fulldomain, 'w+')
		responsefile.write(response.text)
		responsefile.close()

	hosts = open('/etc/hosts','w')	
	hosts.writelines(hostlines)
	hosts.close()
	

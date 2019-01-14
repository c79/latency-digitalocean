#!/usr/bin/env python3

from	operator	import	itemgetter
from	urllib.request	import	urlopen
from	subprocess	import	Popen, PIPE
from	platform	import	system				as	system_name
from	sys		import	exit				as	sys_exit
from	re		import	compile				as	re_compile


# settings
## set count on ping command
ping_count = 4
## other ping parameters (like '-i 0.2 -f')
ping_other_param = ''


if system_name().lower()=='linux':
	param = '-c ' + str(ping_count) + ' ' + str(ping_other_param)
else:
	print("Unsupported")
	sys_exit(2)


def ping(host):
	return Popen("ping " + param + ' ' + host, shell=True, stdout=PIPE).stdout.read()


def speedtest():
	print("Getting DigitalOcean servers...")

	url = "http://speedtest-nyc1.digitalocean.com/"
	resp = urlopen(url).read().decode('utf-8')

	expression = re_compile('<a href=\"http://(speedtest-[a-z]{3}[0-9]{1,}.digitalocean.com)\">[A-Z]{3}[0-9]{1,}</a>')

	global servers
	servers = {}

	for server in expression.findall(resp):
		servers[server] = None

	print("Got DigitalOcean servers!\n")


def ping_servers():
	expression = re_compile(b'(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+) ms')
	expression2 = re_compile('[a-z]{3}[0-9]{1,}')

	global server_region
	server_region = {}

	for key in servers.keys():
		server_region[key] = expression2.search(key).group(0).lower()
		print("Pinging {}...".format(str(server_region[key])))
		servers[key] = float(expression.search(ping(key)).group(2))
		print("Done!\n")


def results():
	i = 0
	print("\n\nLowest latency region: ")
	for key, value in sorted(servers.items(), key = itemgetter(1), reverse = False):
		i += 1
		print('{}) {}: {} ms'.format(str(i), server_region[key], str(value)))


speedtest()
ping_servers()
results()

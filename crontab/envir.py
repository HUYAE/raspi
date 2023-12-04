import datetime

now = datetime.datetime.now()

if now.hour % 6 == 0:
	import grow
else:
	import dht22
	

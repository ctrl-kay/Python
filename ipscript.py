import os, re, ipwhois
ipList = open("iplist.txt", "r")
writeFile = open("asnoutput.txt", "a")

for x in ipList:
	ip = x
	myData = os.popen('tracert ' + ip).read()
	route = re.findall('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', myData)[1:]
	for hop in route:
		try:
			myIp = ipwhois.net.Net(hop)
			myObj = ipwhois.asn.IPASN(myIp)
			results = myObj.lookup()
			outputData = [hop, results['asn'], results['asn_description']]
			writeFile.write(str(outputData) + "\n")
		except: 
			print("Non-lookupable IP address, sucka!")
			writeFile.write("Non-lookupable IP address, sucka!\n")
	writeFile.write("\n") 



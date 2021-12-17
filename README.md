# Log4J-Scanner
Something I built to test for Log4J vulnerabilities on customer networks. 

I'm not responsible if your computer blows up, catches fire or your network breaks. 
This is desugned to rotate through /24 networks and ping all IPs. if a ICMP request is returned, it then will create a thread to test ports 1-10000 with the payload in the headers.
if a connection comes back in to the main host you are sending from on the designated port, then the vulnerability worked.

Please do not use this to attack people. this is to find vulnerable devices on the network so you can patch it. 

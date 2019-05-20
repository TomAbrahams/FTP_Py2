# -*- coding: utf-8 -*-
"""
Created on Sun May 07 09:35:49 2017

@author: Thomas
"""

# -*- coding: utf-8 -*-
"""
Created on Sat May 06 21:39:21 2017

@author: Thomas
"""

#!/usr/bin/env python

import socket
import commands
import sys
import os

# Command line checks 
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <PORT NUMBER>" 
                                 
def lsmethod():
    data = ""
    for line in commands.getstatusoutput('ls -l'):
        data +=str(line)
    return data
def recvAll(sock, numBytes):
	# The buffer
	recvBuff = ""	
	# The temporary buffer
	tmpBuff = ""	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:	
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)	
		# The other side has closed the socket
		if not tmpBuff:
			break	
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	return recvBuff


TCP_DATA_PORT = int(sys.argv[1])
BUFFER_SIZE = 65550  # Normally 1024, but we want fast response
# Build 

# Command Sockets
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind(('', TCP_DATA_PORT))
c.listen(1)
commandSock, addr = c.accept()
# See if the data is a receive socket #1R.
# This is when the fork should start.
confirm = recvAll(commandSock,2) #1R GO

print 'Connection address:', addr
print confirm
print "Beginning the program."
flag = True

while flag:
    message = recvAll(commandSock,6)    #Send command 2 cmd
    if(message == "QUIT##"):
        flag = False
        print "Closing the server"
    elif(message == "LS####"):   
        d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        d.bind(('', 0))
        properSocket = str(d.getsockname()[1])
        while len(properSocket) < 10:
            properSocket = "0" + properSocket
        print "Sending the item"
        commandSock.send(properSocket)  #3Send!
        d.listen(1)
        downloadSock, addr = d.accept()
        #the Ls data
        lsData = lsmethod()
        sizeOflsData = len(lsData)
        print "The size:", sizeOflsData
        sizeOflsData = str(sizeOflsData)
        while len(sizeOflsData) < 10:
            sizeOflsData = "0"+sizeOflsData
        print sizeOflsData
        print "The size of ls data = ", int(sizeOflsData)
        downloadSock.sendall(sizeOflsData) # Send the Size portion.
        print "Send the ls data"
        downloadSock.sendall(lsData)  # Send the Data entirely
        downloadSock.close()
    elif(message== "PUT ##"):
        d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        d.bind(('', 0))
        properSocket = str(d.getsockname()[1])
        while len(properSocket) < 10:
            properSocket = "0" + properSocket
        print "Sending the item"
        commandSock.sendall(properSocket)  #3Send!
        d.listen(1)
        downloadSock, addr = d.accept()
        #Download sock
        sizeFileName = recvAll(downloadSock, 10)# Send the size of the filename.
        sizeFileName = int(sizeFileName)
        fileName = recvAll(downloadSock, sizeFileName) #Get name
        print "received name:", fileName
        print "getting size of data..."
        sizeOfData = recvAll(downloadSock, 10) #Get size of put data
        sizeOfData = int(sizeOfData)
        fileData = recvAll(downloadSock, sizeOfData)
        print "writing the file to ", fileName
        downloaded = open(fileName,"w")
        downloaded.writelines(fileData)
        downloaded.close()
        print "Closing download socket"
        downloadSock.close()
    elif(message == "GET ##"):
        d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        d.bind(('', 0))
        properSocket = str(d.getsockname()[1])
        while len(properSocket) < 10:
            properSocket = "0" + properSocket
        print "Sending the item"
        commandSock.sendall(properSocket)  #3Send!
        d.listen(1)
        downloadSock, addr = d.accept()
        #Download sock
        sizeFileName = recvAll(downloadSock, 10)# Send the size of the filename.
        sizeFileName = int(sizeFileName)
        fileName = recvAll(downloadSock, sizeFileName) #Get name
        
        #File read for sending.
        with open(fileName,"r") as myFile:
            data = myFile.read()
        sizeOfGetData = len(data)
        sizeOfGetData = str(sizeOfGetData)        
        while len(sizeOfGetData) < 10:
            sizeOfGetData = "0"+sizeOfGetData
        print "Size of the data...", sizeOfGetData
        print "Int conversion...", int(sizeOfGetData)
        downloadSock.sendall(sizeOfGetData) #Send size of put data
        print "Data Size Sent!"
        downloadSock.sendall(data)
        print "Data Sent!"
    
  
#myFile.close()
commandSock.close()

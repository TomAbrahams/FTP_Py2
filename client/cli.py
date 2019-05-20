# -*- coding: utf-8 -*-
"""
Created on Sun May 07 09:35:02 2017

@author: Thomas
"""

#!/usr/bin/env python

import socket
import commands
import sys

# Command line checks 
if len(sys.argv) < 3:
	print "USAGE python " + sys.argv[0] + " <server_machine> <server_port>" 


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
# Open the ports for the command channel.
TCP_IP = sys.argv[1]
TCP_COMMAND_PORT = int(sys.argv[2])
BUFFER_SIZE = 65550
command = ""

commandSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
commandSock.connect((TCP_IP, TCP_COMMAND_PORT))
commandSock.sendall("GO") #1S Send connected!




while(command != "QUIT"):
    command = raw_input("ftp>")
    theOrder = command[0:3]
    fileName = ""
    if(len(theOrder) > 2):
        theNameOfSentRecFile = str(command[4:])
        fileName = theNameOfSentRecFile
    
    
    
    if(command == "?"):
        print "get <file name> (downloads file <file name> from the server)"
        print "put <file name> (uploads file <file name> to the server)"
        print "ls (lists files on the server)"
        print "lls (lists files on the client)"
        print "quit (disconnects from the server and exits)"
    elif(command == "lls"):
        print(lsmethod())
    elif(command.upper() =="QUIT"):
        print "Disconnecting..."
        command = command.upper()
        commandSock.sendall("QUIT##")  #Send Command 2 cmd
    elif(command.upper() == "LS"):
        print "Sending LS####"
        commandSock.sendall("LS####") #Send Command 2 cmd
        #Make the socket.
        print "Sent LS####"
        download_port_num = recvAll(commandSock,10)   #3R Got number
        download_port_num = int(download_port_num)
        #Made Scoket.
        downloadSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        downloadSock.connect((TCP_IP, download_port_num))
        #Size of ls
        sizeOfls = recvAll(downloadSock,10) # Get the size portion.
        print "ls header length: ",sizeOfls
        sizeOfls = int(sizeOfls)
        print "Size of ls:", sizeOfls
        lsData = recvAll(downloadSock, sizeOfls) #Get the data entirely.
        print lsData #Print the data.
        #So put has been sent.
        #size = downloadSock.send()
    elif(len(command) > 3 and command.upper()[0:3] == "PUT"):
        request = "PUT ##"
        #Make the socket.
        commandSock.sendall(request)
        download_port_num = recvAll(commandSock,10)   #3R Got number
        download_port_num = int(download_port_num)
        #Made Scoket.
        downloadSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        downloadSock.connect((TCP_IP, download_port_num))
        #So download Socket is made.
        #Get the length...
        print "Filename is: ",fileName
        # the rest of the item
        sizeOfFileName = len(fileName)
        sizeOfFileName = str(sizeOfFileName)
        while len(sizeOfFileName) < 10:
            sizeOfFileName = "0" + sizeOfFileName            
        print "Size of filename", sizeOfFileName
        downloadSock.sendall(sizeOfFileName) #Size of file name
        print "Send the filename"
        downloadSock.sendall(fileName) #Send name
        # send the file name.
        with open(fileName,"r") as myFile:
            data = myFile.read()
        sizeOfPutData = len(data)
        sizeOfPutData = str(sizeOfPutData)
        
        while len(sizeOfPutData) < 10:
            sizeOfPutData = "0"+sizeOfPutData
        print "Size of the data...", sizeOfPutData
        print "Int conversion...", int(sizeOfPutData)
        downloadSock.sendall(sizeOfPutData) #Send size of put data
        print "Data Size Sent!"
        downloadSock.sendall(data)
        print "Data Sent!"
        
        
    elif(len(command) > 3 and command.upper()[0:3] == "GET"):
        request = "GET ##"
        #Make the socket.
        #Make the socket.
        commandSock.sendall(request)
        download_port_num = recvAll(commandSock,10)   #3R Got number
        download_port_num = int(download_port_num)
        #Made Scoket.
        downloadSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        downloadSock.connect((TCP_IP, download_port_num))
        print "Filename is: ",fileName
        # the rest of the item
        sizeOfFileName = len(fileName)
        sizeOfFileName = str(sizeOfFileName)
        while len(sizeOfFileName) < 10:
            sizeOfFileName = "0" + sizeOfFileName            
        print "Size of filename", sizeOfFileName
        downloadSock.sendall(sizeOfFileName) #Size of file name
        print "Send the filename"
        downloadSock.sendall(fileName) #Send name
        #Got the name.
        print "the name:", fileName
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


        
commandSock.close()




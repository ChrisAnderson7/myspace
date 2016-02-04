#!/usr/bin/env python
#Open SSHv2 connections to devices

import paramiko
import time
import re
import sys


def open_ssh_conn(ip):
    #Change Exception message
    
    try:
        #loop counter
        #Defining the credentials file
        #user_file = sys.argv[1]
        print "print in testbranch1"
        user = raw_input("Enter the username and hit enter ")
        
        #defining the commands file
        #cmd_file = sys.argv[2]
        
        #Define SSH parameters
        #selected_user_file = open(user_file,'r')
        
        #start from begining of file   
        #selected_user_file.seek(0)
        
        #reading the username from the file
        #username = selected_user_file.readlines()[0].split(',')[0]
        
        #startingfrom begining of file
        #selected_user_file.seek(0)
        
        #reading the password from the file
        #password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")
        password = raw_input("Enter the password ")
        
        #logging into device invoking the SSHClient class 
        session = paramiko.SSHClient()
        
        #for testing purposes, this allows auto-accepting unknown host keys
        #DO NOT use in production! The default would be to RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
        #connect to the device using username and pw
        session.connect(ip,username=user,password=password)
      
        #start an interactive shell session on the router  
        connection = session.invoke_shell()
        
        #setting terminal length for entire output - no paginations
        connection.send("terminal length 0\n")
        time.sleep(1)
        
        #Entering global config mode
        #connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)
        
        #open user selected file for reading
        cmd_file = raw_input("Enter the name of the command file exa. hpcmd.txt -> ")

        if (cmd_file == 'hpcmd.txt'):
            selected_cmd_file = open(cmd_file,'r')
            selected_cmd_file.seek(0)
            doloop = 'true'
            #starting from the begining of file
        else:
            doloop =  'false'
            print "\n"
            print "There was a mistake in the command file name"
            print "\n"
            print "Ending program before processing login to device check inputs"
            print "============================================================="

        

        x = 0

        while doloop == 'true':
            #writing each line in the file to the device
            for each_line in selected_cmd_file.readlines():
            
                #print "entering the connection.send stuff"
                connection.send(each_line)
                #connection.send("write memory" + '\n')
                #print "each line -> %s " % each_line
                #print "------------------------------"
                time.sleep(2)
            
                #closing the user file
                #selected_user_file.close()

                #closing the command file
                #selected_cmd_file.close()

                #checking command router output for IOS syntax errors max possible 65535
                router_output =  connection.recv(65535)

                #checking command output of IOS syntax errors
                if re.search(r"Invalid input: ", router_output):
                    print "------------------Error Handling BEGIN---------------------------------------------"
                    print "There was at least one IOS syntax error on device %s" % ip
                    print "There may be a syntax error in the following line -> " + each_line
                    print "------------------Error Handling END-----------------------------------------------"

                else:
                    x = x + 1
        
                    
                #print "-------------after checking output-----------------------------"
                #Test for reading command output

                #closing the connection
                session.close()
            doloop = 'false'

        print "\n"
        print " Program Results...."
        print "\nDONE for device %s" % ip + " AND %s commands completed succesfully " % x
        print "\n"

    except paramiko.AuthenticationException:
                
            print "* Invalid username or password. \n* Please check the usnername\pw for the device cofiguration!"     
            print "* Closing program \n"
                
            #calling the ssh function
open_ssh_conn("192.168.1.93")

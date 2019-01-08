import socket
import sys, pprint
import ssl

PlayAgain = True
Debug = True

while PlayAgain:
    
    #-- Reset vars if reset (play agian)
    connected = 0
    closeSocket = ""
    Finish = False
    NoG = 10
    #--
    
    while connected == 0:
        connectTo = str(raw_input("What is the address? (I.E. 127.0.0.1): "))
        port = int(raw_input("Which port do you want to connect to? (I.E. 4000): "))
        try:
            server_address = (connectTo, port)
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            ts = ssl.wrap_socket(s, certfile="100215286.crt", keyfile="100215286.key",
            ca_certs="5cc515_root_ca.crt")

            print >>sys.stderr, 'CONNECTING TO %s ON PORT %s' % server_address
            
            ts.connect(server_address)
            
            #print repr(ts.getpeername())
            #print ts.cipher()
            #print pprint.pformat(ts.getpeercert())
            
            connected = 1
            print "CONNECTED TO SERVER"
            
            #-- Hello/Greetings
            greet = "HELLO\n\r"

            if Debug:
                print "\n"
                print >>sys.stderr, '%s: SENDING "%s"' % (ts.getsockname(), greet)
            ts.send(greet)

            data = ts.recv(1024)
            if Debug:
                print >>sys.stderr, '%s: RECEIVED "%s"' % (ts.getsockname(), data)
                
            #invalid data, tampering
            if greet != data:
                print "\n"
                print >>sys.stderr, '%s: RECEIVED GUESS "%s" AND DATA "%s" INVALID (MISSMATCH), CLOSING SOCKET' % (s.getsockname(), greet, data)
                ts.close
                        
            if not data:
                print "\n"
                print >>sys.stderr, 'CLOSING SOCKET', ts.getsockname()
                ts.close()

            data = ts.recv(1024)
            if Debug:
                print "\n"
                print >>sys.stderr, '%s: RECEIVED GREETINGS "%s"' % (ts.getsockname(), data)

            if not data:
                print "\n"
                print >>sys.stderr, 'CLOSING SOCKET', ts.getsockname()
                Finish = True
                ts.close()
                    
            #-- datatypes
            datatype = data.split("\n\r")
                        
            if datatype[0] == "GREETINGS":
                print "\n"
                print "Greetings From", server_address
            #--
                    
        except socket.error, e:
            if connected == 0:
                print "\n"
                print "CANNOT CONNECT TO THE SERVER, TRY AGAIN"
        
    while not Finish:
        #-- check if int
        NotInt = True
        while NotInt:
            try:
                print "\n"
                print "Guesses Left:", NoG
                guess = int(input("Your guess? "))
                NotInt = False
            except:
                print "\n"
                print "Please enter a Number (i.e. 10)"
        #--

        GUESS = "GUESS\n\r" + str(guess)

        if Debug:
            print "\n"
            print >>sys.stderr, '%s: SENDING "%s"' % (ts.getsockname(), GUESS)
        ts.send(GUESS)

        data = ts.recv(1024)
        if Debug:
            print >>sys.stderr, '%s: RECEIVED "%s"' % (ts.getsockname(), data)

        #invalid data, tampering
        if GUESS != data:
            print "\n"
            print >>sys.stderr, '%s: RECEIVED GUESS "%s" AND DATA "%s" INVALID (MISSMATCH), CLOSING SOCKET' % (ts.getsockname(), guess, data)
            ts.close
                
        if not data:
            print "\n"
            print >>sys.stderr, 'CLOSING SOCKET', ts.getsockname()
            Finish = True
            ts.close()

        data = ts.recv(1024)
        if Debug:
            print "\n"
            print >>sys.stderr, '%s: RECEIVED "%s"' % (ts.getsockname(), data)
        
        if not data:
            print "\n"
            print >>sys.stderr, 'CLOSING SOCKET', ts.getsockname()
            Finish = True
            ts.close()
                
        #-- datatypes
        datatype = data.split("\n\r")

        if datatype[0] == "CORRECT":
            print "\n"
            print "You Are Correct"
            Finish = True
            
        elif datatype[0] == "OUT":
            print "\n"
            print "You Are Out of Guesses"
            Finish = True

        elif datatype[0] == "FAR":
            print "\n"
            NoG = NoG - 1
            print "You Are Way Off"

        elif datatype[0] == "CLOSE":
            print "\n"
            NoG = NoG - 1
            print "You Are Close"

        else:
            print "\n"
            print >>sys.stderr, 'RECEIVED INVALID DATA: "%s" FROM %s' % (data, ts.getpeername())

        if not data:
            print "\n"
            print >>sys.stderr, 'CLOSING SOCKET', ts.getsockname()
            Finish = True
            ts.close()

        #--

                
    while closeSocket != "Y" and closeSocket != "y" and closeSocket != "N" and closeSocket != "n":
        print "\n"
        closeSocket = str(raw_input("Play again? Y/N or y/n: "))
        if closeSocket == "N" or closeSocket == "n":
            print "\n"
            if Debug:
                print >>sys.stderr, 'CLOSING SOCKET', ts.getsockname()
            PlayAgain = False
            ts.close()
        elif closeSocket == "Y" or closeSocket == "y":
            print "\n"
            if Debug:
                print >>sys.stderr, 'RESETING CLIENT', ts.getsockname()
            PlayAgain = True
            ts.close()

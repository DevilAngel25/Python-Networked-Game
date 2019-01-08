import socket
import sys

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
            print >>sys.stderr, 'CONNECTING TO %s ON PORT %s' % server_address
            s.connect(server_address)
        
            connected = 1
            print "CONNECTED TO SERVER"
            
            #-- Hello/Greetings
            greet = "ADMIN\n\r"

            if Debug:
                print "\n"
                print >>sys.stderr, '%s: SENDING "%s"' % (s.getsockname(), greet)
            s.send(greet)

            data = s.recv(1024)
            if Debug:
                print >>sys.stderr, '%s: RECEIVED "%s"' % (s.getsockname(), data)
                
            #invalid data, tampering
            if greet != data:
                print "\n"
                print >>sys.stderr, '%s: RECEIVED GUESS "%s" AND DATA "%s" INVALID (MISSMATCH), CLOSING SOCKET' % (s.getsockname(), greet, data)
                s.close
                        
            if not data:
                print "\n"
                print >>sys.stderr, 'CLOSING SOCKET', s.getsockname()
                s.close()

            data = s.recv(1024)
            if Debug:
                print "\n"
                print >>sys.stderr, '%s: RECEIVED GREETINGS "%s"' % (s.getsockname(), data)

            if not data:
                print "\n"
                print >>sys.stderr, 'CLOSING SOCKET', s.getsockname()
                Finish = True
                s.close()
                    
            #-- datatypes
            datatype = data.split("\n\r")
                        
            if datatype[0] == "GREETINGS":
                print "\n"
                print "Greetings Admin From", server_address
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
            print >>sys.stderr, '%s: SENDING "%s"' % (s.getsockname(), GUESS)
        s.send(GUESS)

        data = s.recv(1024)
        if Debug:
            print >>sys.stderr, '%s: RECEIVED "%s"' % (s.getsockname(), data)

        #invalid data, tampering
        if GUESS != data:
            print "\n"
            print >>sys.stderr, '%s: RECEIVED GUESS "%s" AND DATA "%s" INVALID (MISSMATCH), CLOSING SOCKET' % (s.getsockname(), guess, data)
            s.close
                
        if not data:
            print "\n"
            print >>sys.stderr, 'CLOSING SOCKET', s.getsockname()
            Finish = True
            s.close()

        data = s.recv(1024)
        if Debug:
            print "\n"
            print >>sys.stderr, '%s: RECEIVED "%s"' % (s.getsockname(), data)
        
        if not data:
            print "\n"
            print >>sys.stderr, 'CLOSING SOCKET', s.getsockname()
            Finish = True
            s.close()
                
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
            print >>sys.stderr, 'RECEIVED INVALID DATA: "%s" FROM %s' % (data, s.getpeername())

        if not data:
            print "\n"
            print >>sys.stderr, 'CLOSING SOCKET', s.getsockname()
            Finish = True
            s.close()

        #--

                
    while closeSocket != "Y" and closeSocket != "y" and closeSocket != "N" and closeSocket != "n":
        print "\n"
        closeSocket = str(raw_input("Play again? Y/N or y/n: "))
        if closeSocket == "N" or closeSocket == "n":
            print "\n"
            if Debug:
                print >>sys.stderr, 'CLOSING SOCKET', s.getsockname()
            PlayAgain = False
            s.close()
        elif closeSocket == "Y" or closeSocket == "y":
            print "\n"
            if Debug:
                print >>sys.stderr, 'RESETING CLIENT', s.getsockname()
            PlayAgain = True
            s.close()

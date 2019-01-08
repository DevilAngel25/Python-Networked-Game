import select
import socket
import sys
import Queue
import os
import random
import ssl

class Player():
      Name = ""
      NoG = 10
      Score = 0
      Guess = 0

def within(value, goal, n):
      if abs(value - goal) <= n:
            return True
      else:
            return False

#vars
Message = ""
Name = ""
NoG = 0
Guess = 0
connected = 0
Debug = True

while connected == 0:
      port = int(raw_input("Please enter the port you wish to connect to: "))
      try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            server.setblocking(0)

            server_address = ('localhost', port)
            print >>sys.stderr, 'STARTING SERVER ON %s PORT %s' % server_address
            
            server.bind(server_address)
            server.listen(5)
            
            connected = 1
            print "SERVER CREATED SUCCESSFULLY" 
      except socket.error, e:
            if connected == 0:
                  print "CANNOT CONNECT, TRY AGAIN"

inputs = {}
inputs[server] = server

outputs = []

message_queues = {}

while inputs:
      if Debug:
            print >>sys.stderr, '\nwaiting for the next event'
      read, write, ex = select.select(inputs, outputs, inputs)

      for s in read:
            if s is server:
                  (connection, client_address) = s.accept()
                  ts = ssl.wrap_socket(connection, certfile="server.crt", keyfile="server.key",
                  server_side=True, cert_reqs=ssl.CERT_REQUIRED,
                  ca_certs="root_ca.crt")
                  
                  print >>sys.stderr, 'NEW CONNECTION FROM', client_address
                  connection.setblocking(0)
                  
                  inputs[ts] = Player()
                  
                  inputs[ts].RN = random.randrange(1, 10, 1)
                  inputs[ts].Name = str(client_address)
                  inputs[ts].NoG = 10
                  inputs[ts].Score = 0
                  inputs[ts].Guess = 0
                  
                  #-- Debug
                  if Debug:
                        print "\n"
                        print "Random number is : ", inputs[ts].RN
                        print "Name is : ", inputs[ts].Name
                        print "Number of Guesses is : ", inputs[ts].NoG
                        print "Score is : ", inputs[ts].Score
                        print "The Guess is : ", inputs[ts].Guess
                  #--

                  message_queues[ts] = Queue.Queue()
            else:
                  data = s.recv(1024)
                  if data:
                        if Debug:
                              print "\n"
                              print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())

                        #-- datatypes
                        datatype = data.split("\n\r")
                        
                        if datatype[0] == "HELLO":
                              if Debug:
                                    print "\n"
                                    print >>sys.stderr, 'HELLO PLAYER: %s' % (inputs[s].Name)
                              Message = "GREETINGS\n\r"
                              
                        elif datatype[0] == "ADMIN":
                              if Debug:
                                    print "\n"
                                    print >>sys.stderr, 'HELLO ADMIN: %s' % (inputs[s].Name)
                              Message = "GREETINGS\n\r"

                        elif datatype[0] == "GUESS":
                              Guess = int(datatype[1])
                              inputs[s].Guess = Guess
                              if Debug:
                                    print "\n"
                                    print >>sys.stderr, 'The Guess is: %s from player %s ' % (inputs[s].Guess, inputs[s].Name)
                        
                              #-- Game Logic
                              if inputs[s].Guess > inputs[s].RN or inputs[s].Guess < inputs[s].RN:
                                    if within(inputs[s].Guess, inputs[s].RN, 3) == False:
                                          if Debug:
                                                print "\n"
                                                print >>sys.stderr, 'Player %s is WAY OFF' % (inputs[s].Name)
                                          Message = "FAR\n\r"
                                    else:
                                          if Debug:
                                                print "\n"
                                                print >>sys.stderr, 'Player %s is LESS THAN THREE AWAY' % (inputs[s].Name)
                                          Message = "CLOSE\n\r"
                                          
                                    inputs[s].Score = inputs[s].Score - 1
                                    inputs[s].NoG = inputs[s].NoG - 1

                              elif inputs[s].Guess == inputs[s].RN:
                                    Message = "CORRECT\n\r"
                                    if Debug:
                                          print "\n"
                                          print >>sys.stderr, 'Player %s is CORRECT' % (inputs[s].Name)

                                    inputs[s].Score = inputs[s].Score + 10
                                    
                                    if os.path.exists('Scores.txt') :
                                          f = open('Scores.txt', 'ab')
                                          f.write('\r\n' + str(inputs[s].Name) + '\t' + str(inputs[s].NoG) + '\t' + str(inputs[s].Score))
                                          f.close()
                                          if Debug:
                                                print "\n"
                                                print >>sys.stderr, 'CLIENT DATA SAVED'
                                    else :
                                          if Debug:
                                                print "\n"
                                                print >>sys.stderr, 'NO FILE EXISTS, CREATING NEW FILE!'
                                          f = open('Scores.txt', 'wb')
                                          f.write("Client Name (Address)" + '\t' + "Guesses" + '\t' + "Score")
                                          f.close()

                                          f = open('Scores.txt', 'ab')
                                          f.write('\r\n' + str(inputs[s].Name) + '\t' + str(inputs[s].NoG) + '\t' + str(inputs[s].Score))
                                          f.close()
                                          if Debug:
                                                print >>sys.stderr, 'CLIENT DATA SAVED'
            
                              if inputs[s].NoG == 0:
                                    Message = "OUT\n\r"
                                    if Debug:
                                          print "\n"
                                          print >>sys.stderr, 'Player %s is OUT OF GUESSES' % (inputs[s].Name)
                              #--
                        else:
                              print "\n"
                              print >>sys.stderr, 'RECIEVED INVALID DATA: "%s" FROM %s' % (data, s.getpeername())
                        #--
                              
                        #-- Debug    
                        if Debug:    
                              print "\n"
                              print "Random number is : ", inputs[s].RN
                              print "Name is : ", inputs[s].Name
                              print "Number of Guesses is : ", inputs[s].NoG
                              print "Score is : ", inputs[s].Score
                              print "The Guess is : ", inputs[s].Guess
                        #--
                        
                        message_queues[s].put(data)
                        
                        if Message != "":
                              message_queues[s].put(Message)
                              Message = ""
                              
                        if s not in outputs:
                              outputs.append(s)
                  else:
                        print >>sys.stderr, 'CLOSING ', client_address, ' AFTER NO DATA TO READ'
                        print "\n"
                        
                        if s in outputs:
                              outputs.remove(s)
                              
                        del inputs[s] 
                        s.close()

                        del message_queues[s]
                        
      #-- Handle Output
      for s in write:
            try:
                  next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                  if Debug:
                        print "\n"
                        print >>sys.stderr, 'OUTPUT QUEUE FOR ', s.getpeername(), 'IS EMPTY'
                  outputs.remove(s)
            else:
                  if Debug:
                        print "\n"
                        print >>sys.stderr, 'SENDING "%s" TO %s' % (next_msg, s.getpeername())
                  s.send(next_msg)
      #--

      #-- handle exceptions
      for s in ex:
            print "\n"
            print >>sys.stderr, 'HANDLING EXCEPTIONAL CONDITION FOR ', s.getpeername()
            del inputs[s] 
            if s in outputs:
                  outputs.remove(s)
            s.close()
            
            del message_queues[s]
      #--

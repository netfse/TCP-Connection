from socket import *
import re

# set socket and timeout
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.settimeout(5) 

# valid serverName and serverPort
regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
Valid = False

serverName = ''
serverPort = 0

while not Valid:
    serverInput = input('Enter: serverName serverPort\n').split(' ')
    
    try:
        serverName = str(serverInput[0])
        serverPort = int(serverInput[1])

        if(not re.search(regex, serverName)):
            print("Invalid Server Ip address: %s, please try again" %(str(serverInput[0])))
            continue

        if(serverPort <= 0):
            print("serverPort should be positive number: %s, please try again" %(str(serverInput[1])))
            continue

        Valid = True

    except IndexError:
        print("ServerName and serverPort should not be empty, please try again")
        continue
        
    except ValueError:
        print("Invalid Server port: %s, please try again" %(str(serverInput[1])))
        continue

ServerConnection = False

# connecting to the server
try:
    clientSocket.connect((serverName,serverPort))
    print ("Successful connection with the server: %s and the port: %d" %(serverName, serverPort))
    ServerConnection = True 

except OSError as error:
    print ("Fail connection with the server: %s and the port: %d" %(serverName, serverPort))
    ServerConnection = False

#Command 
while ServerConnection:
    
    command = input('Input command: ')
    clientSocket.send(command.encode())

    if command=='QUIT':
        modifiedMsg = clientSocket.recv(1024)
        print(modifiedMsg.decode())
        break

    elif command=='POST':
        print('IP Address: %s Port Number: %d' %(serverName, serverPort))
        print('Connect status: OK/ERROR')
        print('Send status: OK/ERROR \n')

        msg = '   '

        while msg != '#':
            msg = input('Please input sentence:')
           
            clientSocket.send(msg.encode())
        modifiedMsg = clientSocket.recv(1024)

        print(modifiedMsg.decode())
    
    elif command == 'READ':
        print('IP Address: %s Port Number: %d \n' %(serverName, serverPort))
        print('Connect status: OK/ERROR\n')
        print('Send status: OK/ERROR\n')

        while True: # read msg until "#"
            modifiedMsg = clientSocket.recv(1024)
            receiveMsg = modifiedMsg.decode()
            print(receiveMsg)
            if receiveMsg == "server: #":
                break

    else:
        modifiedMsg = clientSocket.recv(1024)
        print(modifiedMsg.decode())

#Close the connection
clientSocket.close()

import socket
import random

WINDOW_SIZE = 4

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 12344  # initiate port no above 1024
    win_start = 0
    win_end   = win_start + WINDOW_SIZE - 1
    receiver = []
    _data = []
    received_data = []

    received_all = False

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: ", str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        rec = str(data).split(',')
        print(rec)
        for i in range(0, len(rec) - 1, 2):
            if int(rec[i]) not in receiver:
                receiver.append(int(rec[i]))
                _data.append(str(rec[i+1]))
                print("Received Frame -> " + str(rec[i]) + " (Data=" + str(rec[i+1]) + ")")
            
        print(receiver)
        print(_data)

        if len(receiver) == WINDOW_SIZE:
            randy = random.randint(1, 100)
            print(randy)
            if randy > 70 and randy <= 90:
                ack = "NACK" + str(receiver[0])
                print("Rejecting NACK    -> ", ack)
            else:
                ack = "ACK" + str(receiver.pop(0))
                received_data.append(_data.pop(0))
                print("Sending ACK    -> ", ack)
            conn.send(ack.encode())

        print("Current Received Data => ", received_data)





        # rec[0] = int(rec[0])
        # rec[1] = int(rec[1])
        # lim = int(rec[0]) + WINDOW_SIZE - 1
        # count = 0
        # flag = 0
        # ack = int(rec[0])
	
	
        # # randy = random.randint(1, 4)
        # # if new == 1 : 			#you received a new frame of a new window
        # #     while(count != randy):
        # #         temp = random.randint(rec, lim)
                
        # #         if temp not in receiver:
        # #             print("Received Frame -> ", temp)
        # #             count+=1
        # #             flag = 1       #Atleast one new frame added in receiver buffer
        # #             receiver.append(temp)
        # # else :
        # print("Received Frame -> ", rec[0]) #you received a new frame of an old window  
        # # receiver.append(rec[1])
        # flag = 1
        # if(flag == 1):
        #     for i in range(rec[0],lim+1):
        #         if i not in receiver:
        #             ack = i
        #             break
        #         ack = i+1
    
        # print("Sending ACK    -> ", ack) #next expected frame
        # print('***************************************************')
        # data = 'ACK' + str(ack)
        # conn.send(data.encode())  # send data to the client

        # if ack > win_end :
        #     win_start = ack
        #     win_end   = win_start + WINDOW_SIZE - 1
        #     new = 1			# now receive a new frame of a new window
        # else :
        #     new = 0 		# now received a new frame of an old window

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()

############################# OUTPUT : Server Side ##########################
'''
Connection from:  ('127.0.0.1', 40912)
Received Frame ->  0
Received Frame ->  3
Received Frame ->  2
Received Frame ->  1
Sending ACK    ->  4
***************************************************
Received Frame ->  6
Received Frame ->  5
Sending ACK    ->  4
***************************************************
Received Frame ->  4
Sending ACK    ->  7
***************************************************
Received Frame ->  7
Sending ACK    ->  8
***************************************************
Received Frame ->  9
Received Frame ->  11
Received Frame ->  8
Received Frame ->  10
Sending ACK    ->  12
***************************************************
'''
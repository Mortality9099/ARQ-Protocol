
import datetime
import socket
import time

TIME_OUT = 1
DATA = ['mojsdsaddaewssw', 
        'awewasdxcsdadsds', 
        'wewe232ew22', 3, 4, 5, 6, 7, 8, 0, 67, 6, 
        1, 6, 6, 6, 32, 6, 6, 12, 3,3 , 3, 2]

def client_program():
    window_size = int(input("Enter Window Size: "))
    win_start = 0
    win_end = win_start + window_size - 1
    host = input("Enter Ip(leave blank if you want to connect to same pc): ")  # as both code is running on same pc
    if host == "":
        host = socket.gethostname()
    port = 12344  # socket server port number
    window = []
    _data = []
    transfer_time = []
    data_index = 0

    reject = False
    reject_index = 0
    flag = True

    initial = 1 #start of the initialization
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print('Window Size is ', window_size)

    while True:
        print("1. Selective Repeat ARQ protocol.\n")
        print("2. Go Back N Protocol\n")
        print("0. Exit")
        print("*** Print 'Close' if you want to stop the proccess of tranfering ***")
        option = input()
        
        if option == "1":
            message = input("Hit any key to start sending frames -> ")  # take input
            while message.lower().strip() != 'close':
                print("Sending frames...")
                if (initial == 1):
                    for i in range(window_size):
                        window.append(i)
                        _data.append(DATA[i])
                        data_index = i

                    for i in window :
                        print("Sending Frame -> " + str(i) + "," + str(DATA[i]))

                if reject:
                    # client_socket.send((str(window[reject_index]) + ',' + str(_data[reject_index]) + ',').encode())
                    transfer_time.append(send_message(client_socket, str(window[reject_index]) + ',' + str(_data[reject_index]) + ','))
                else:
                    if initial == 1:
                        for i in range(len(window)):
                            # client_socket.send(window[i])  # send message
                            # client_socket.send((str(window[i]) + ',' + str(_data[i]) + ',').encode())  # send message
                            transfer_time.append(send_message(client_socket, str(window[i]) + ',' + str(_data[i]) + ','))
                        initial = 0
                    elif window_size == len(window):
                        # client_socket.send(window[len(window) - 1])
                        # client_socket.send((str(window[window_size - 1]) + ',' + str(_data[window_size - 1]) + ',').encode())
                        transfer_time.append(send_message(client_socket, str(window[window_size - 1]) + ',' + str(_data[window_size - 1]) + ','))

                data = client_socket.recv(1024).decode() 

                print('Received Ack from Server : ' + data)
                ack = str(data)
                result = ack[0]
                number = 0
                if result == 'N': # NACK
                    reject = True
                    reject_index = int(ack[4:])
                    print(reject_index)
                if result == 'A': # ACK
                    reject = False
                    number = ack[3:]
                    window.pop(0)
                    _data.pop(0)
                    if data_index != len(DATA) - 1 :
                        data_index = data_index + 1
                        window.append(data_index%window_size)
                        _data.append(DATA[data_index])
                    
                    print(str(window))
                    print(str(_data))
                    print(str(transfer_time))
                    
                message = input("Hit any key to start sending frames -> ")  # again take input

            client_socket.close()  # close the connection
        
        elif option == "0":
            client_socket.close()  # close the connection
            exit()
            

def send_message(socket: socket.socket, message: str) -> int:
    before_ = time.time_ns()
    socket.send(message.encode())
    after_ = time.time_ns()
    duration = after_ - before_
    print(before_)
    print(after_)
    return duration

if __name__ == '__main__':
    client_program()
    



######################### OUTPUT : Client Side #################################
'''
Window Size is  4
******** Enter "bye" to close connection ***************
Hit any key to start sending frames -> 
Sending frames...
Frame ->  0
Frame ->  1
Frame ->  2
Frame ->  3
************************************
Received ACK server: 4
Hit any key to start sending frames -> 
Sending frames...
Frame ->  4
Frame ->  5
Frame ->  6
Frame ->  7
************************************
Received ACK server: 4
Hit any key to start sending frames -> 
Sending frames...
Frame ->  4
************************************
Received ACK server: 7
Hit any key to start sending frames -> 
Sending frames...
Frame ->  7
************************************
Received ACK server: 8
Hit any key to start sending frames -> 
Sending frames...
Frame ->  8
Frame ->  9
Frame ->  10
Frame ->  11
************************************
Received ACK server: 12
Hit any key to start sending frames -> bye
'''
#Kelly Chibuike Ojukwu

import socket
import select
import sys
import re
import signal
import queue
import sll
from datetime import datetime as dt
import os


'''
    Example: HTTP Request
    ● HTTP Request = Request line + Header fields + Empty line
    ● Request line (case sensitive):
    ○ GET /filename HTTP/1.0
    ● Each header field:
    ○ Case-insensitive field name
    ○ Colon (“:”)
    ○ Optional leading whitespace
    ○ Case-insensitive field value
    ○ Optional trailing whitespace
    ● Correct format:
    ○ GET /filename HTTP/1.0\r\nConnection:Keep-alive\r\n\r\n
    ○ GET /filename HTTP/1.0\r\nConnection: keep-alive\r\n\r\n
    ○ GET /filename HTTP/1.0\r\n\r\n
    ○ On Windows, a newline is denoted with “\r\n”
    ○ On Unix-like operating systems, “\n” = “\r\n” (your code should support both)
'''


TIMEOUT_TIME = 30
# A map that holds all info on a specific socket relevant to the server:
# Includes time of creation, timeout time etc
# Has the following schema socket 
signal.signal(signal.SIGTSTP, signal.SIG_IGN)
# Sockets we are looking to read from
input_sockets = []
# Scokets we are looking to write to
output_sockets = []


socket_map = {}

socket_info = {"last_line": None,
               "requests" : [],
               "last accessed time": None
               
               }


requests_response = {
    200: "OK",
    400: "Bad Request",
    404: "Not Found",}

persistent_map = {
    True: "keep-alive",
    False: "close",
    
}

http_response_start = "HTTP/1.0"
http_response_response_end = "\nConnection: "
http_bad_request_response_end = " close\n\n"

# Handles new line and forbidden char differences between Unix-like and Windows OS
forbbidden_chars = "[/]"

next_line_char = "\\r\\n|\\n" #"\n\r|\n"
'''if sys.platform.startswith('win'):
    next_line_char = "\r\n"
    forbbidden_chars = "[\\<\\>\\:\"\\\/\\|\\?\\*]"
'''
# Map of queues for outgoing messages, ensures that message is sent to the client end of socket that triggered it
message_queues = {}
requests_map = {}

def close_socket(t_socket: socket):
    if t_socket in input_sockets: input_sockets.remove(t_socket)
    if t_socket in output_sockets: output_sockets.remove(t_socket)
    t_socket.close()
def main(ip_address : str, port_number: int):
    # Create a socket for the server that is non-blocking and bind it to a port

    # Create the socket for the server and put it into input sockets array
    
    server_socket = ServerSocketManager.create_socket(ip_address, port_number)
    server_socket_holder = SocketHolder(server_socket, None)
    input_sockets = [server_socket]
    output_sockets = []
    while (input_sockets):
        # Wait until we have a socket to read/write/exception 
        readable, writable, exceptions = select.select(input_sockets, output_sockets, input_sockets)

        # Kill elderly sockets
        for s in output_sockets:
            if socket_map[s].should_socket_kill():

                close_socket(s)
                
        
        for the_socket in readable:
            #The server socket is ready to accept a connection
            if the_socket is server_socket:
                # Create a socket for communication with the client and put it in a socketHolder object
                client_socket, address = the_socket.accept()
                
                client_socket.setblocking(0)
                socket_holder = SocketHolder(client_socket, None)

                # Create relationship between socket's map and holder
                socket_map[client_socket] = socket_holder
                input_sockets.append(client_socket)

                message_queues[client_socket] = queue.Queue()


            # There is a client socket that wants to message server
            else:
                #Receive the data from the client
                data = the_socket.recv(1024).decode()
                
                #Process the data and transform it into a map of arrays of requests (finished and wip)
                if data:
                    if the_socket not in output_sockets:
                        output_sockets.append(the_socket)

                    requests_map = socket_holder.process_input(data)
                    for request in requests_map["finished"]:
                        print("We're in finished: ", request)
                        socket_holder.process_request(request)
                    print(data)
                    #validate_request(data)
                    #print(data)

        for the_socket in writable:
            try:
                next_message = message_queues[the_socket].get_nowait()
            except queue.Empty:
                output_sockets.remove(the_socket)
            else:
                

                return
                
            #return
        #for object in exceptions:
            #return
        
    

    
    # socket_map["sfferver socket"] = server_socket
    # Keep going forever unless kill code is sent
    #Wait around for new clients to establish connections by creating a client socket so long as server sock is not closed
    
    
    '''while len(server_socket) > 0:
        
        client_socket, address = server_socket.accept()

        if client_socket is not None:
            #client_socket.setblocking(0)
            client_socket.setsockopt(socket.SOL_SOCKET,  socket.SO_REUSEADDR, 1)
            client_socket.send("Hi you are connected\n".encode())
            client_socket_list.append(client_socket)
    #while (True):
    '''



    #    return


#def handle_client_input(client_socket, input, ):
def send_response(request: str, destination_socket: socket):
    response = ""

    return response

'''Valid requests have the following form


'''

def find_file(filename : str):
    try:
        return open(filename)
    except FileNotFoundError:
        return None

# A valid request is made on a socket that exists
def validate_request(request:str):
    #If the input is valid request line then create a new request object in sockets request array.
    if is_valid_request(request):
        print("Valid request")
    if is_valid_header(request):
        print("Valid header")
    print("is request valid")


    
 

def is_valid_request(request:str)->bool:
    #valid_http_request = "GET /.*\s+HTTP/1.0\s*"
    valid_http_request = 'GET /((\S*)|(".*"))\s* HTTP/1.0\s*'

    '/((\S+)|(".*"))\s* HTTP'
    matched_request = re.fullmatch(valid_http_request, request)
    if matched_request is not None:
        return True
    return False
    
def is_valid_header(request:str)->bool:
    valid_http_header = ("Connection:\s*(Keep-alive|close)\s*|\s*")
    matched_header = re.fullmatch(valid_http_header, request, flags= re.I)
    if matched_header is not None:
        return True
    return False


def retrieve_proper_request(request):
    filename = "/.+[^",forbbidden_chars,"] "
    print(filename)




    







    

        
        

# Class on seperate thread that waits asynchronously so that sockets can be created at any time and added to a queue
class ServerSocketManager:

    # Used to enforce condition that only one socket is opened for each connection
    open_sockets = {}
    def self(self):
        return

    # Create a new socket and bind it to an ip address and port number

    def create_socket(ip_address: str, port_number: int) -> socket:
            address_tuple = (ip_address, port_number)
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_socket.setsockopt(socket.SOL_SOCKET,  socket.SO_REUSEADDR, 1)
            #new_socket.setblocking(0)

            new_socket.bind(address_tuple)
            new_socket.listen(5)
            #new_socket.accept()
            return new_socket


    def kill_socket(self, socket_id):
        target_socket = self.open_sockets[socket_id]
        if target_socket is not None:
            target_socket
            self.open_sockets.pop(socket_id)










# Take in input line by line, when double new line is found then put request in request array

main("", 9998)
#validate_request("")
#retrieve_proper_request("")

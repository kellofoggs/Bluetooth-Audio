import re
import socket
from socket import BTPROTO_RFCOMM 
from time import sleep
class SocketHolder:
    the_socket = None
    last_accessed_time = None
    #A list with each line that has been given to the server from the respective client
    input_list = None
    persistent = False
    input_message = None
    unprocessed_message = None
    actualized_requests = None
    valid_requests = None
    potential_requests = None
    def __init__(self, socket, creation_time):
        self.the_socket = socket.socket(socket.AF_, socket.SOCK_STREAM)
        self.last_accessed_time = dt.now()
        #print(self.creation_time)
        self.input_list = sll.single_linked_list()
        self.input_message = str()
        self.potential_requests = []

        self.valid_requests = []
        self.actualized_requests = []

    # Checks if connection has violated timeout
    def should_socket_kill(self):
        current_time = dt.now()
        if (current_time - self.last_accessed_time).seconds >= 30:
            return True
        return False
    
    def set_persistent(self, input: bool):
        self.persistent = input
        
    def add_to_input_list(self,input:str):
        self.input_list.add(input)
        end_line_match = re.fullmatch(next_line_char)
        #We're at the end of a request
        if end_line_match is not None:
            return
        
    #Takes in an input string and adds it to potential requests
    def process_input(self, input: str):

        # Split apart the input into a string array line by line. 
        # An item in the array with all whitespace characters represents a double new line
        self.potential_requests.extend(input.splitlines())
        print(self.potential_requests)
        #print("Init state of potential requests: ",self.potential_requests)
        actualized_requests = []
        index = 0

        
      

        while index < len(self.potential_requests):
            print(index)
            print(self.potential_requests)
            print(">", self.potential_requests[index], " @: ", index)
            # Check if the request is invalid (ignore empty lines before a request)
            
            if not is_valid_request(self.potential_requests[0]) :
                #If we have leading whitespace before get requests
                if re.match("\S", self.potential_requests[0]) is None:
                    self.potential_requests.pop(0)
                    index = 0
                    continue
                print(self.potential_requests[0])
                print("The ",self.potential_requests.pop(0), end= " is a ")
                print("BAAAD REQUEST")

                # Stop actualized requests list at the first badly formed request line
                print(actualized_requests)
                return {"finished":actualized_requests}
            
            #Longer than 2 lines for request
            if index > 2:
                print("Bad requests 22222")
                return {"finished": actualized_requests}
                
            
            # If we have found a double new line in our text (end of request)
            if re.match("\S", self.potential_requests[index]) is  None:
                
                
                #Get everything before the double new line and add to list of complete requests
                request = self.potential_requests[:index]
                #print("Look here nigga: ", request," ", index)
                if len(request) != 0:
                    actualized_requests.append(request)
                #print(request)
                print("The removed: head ", self.potential_requests.pop(0))
                for i in range(0, index):
                    print("The ", i , "to be removed: ", self.potential_requests.pop(0))
                index = 0
                continue
            
        
            index = index+1

        for request in self.potential_requests:
            if not is_valid_request(request) and not is_valid_header(request):
                self.potential_requests.remove(request)
        #print("potential reqs: ", self.potential_requests)    
        print("Actualized request: ", actualized_requests, "\n")
        return {"finished": actualized_requests,
                "wip": self.potential_requests}
    
    # Processes requests that have been verified to have a proper first line and size of 2 at most
    def process_request(self, request: []):
        self.persistent = False
        request_line = request[0]
        print(request_line)
        temp_file_name = re.search('/((\S*)|(".*"))\s* HTTP',request_line).group()
        if not temp_file_name.__contains__('"'):
            temp_file_name = re.split("\s",temp_file_name)[0]
        else:
            temp_file_name = re.search('(".*")').group()
        #Remove space after file name and HTTP tag
        file_name = temp_file_name[1:]#[1:len(temp_file_name)-5]
        print(temp_file_name)
        print(len(temp_file_name))
        print("File name is: |", file_name,"|")
        if file_name == "":
            file_name = "index.html"
        print(len(file_name))
        print(request_line.split(" "))

        print(request)
        header_line = None
        #A good request will at most have 2 lines
        if len(request ) > 2:
            print("Bad request")
            return
        
        

        if is_valid_request(request_line) :
            if len(request) > 1:
                header_line = request[1]
                if not is_valid_header(header_line):
                    print("Header line makes invalid!")
                else:
                    print ("THIS Is a valid request")
                    self.send_file(file_name)
                
            else:
                print(request, "Is a valid request")
                self.send_file(file_name)
            
        else:
            print("Bad request")
        return
    
    #Preps a header to be sent to a client's terminal
    def send_header(self, response_code):
        message = "HTTP/1.0 " + str(response_code) +" "+ requests_response[response_code] +"\nConnection: " + persistent_map[self.persistent] +"\n\n"
        self.send_to_client(message)

    #Preps a file to be sent to a client's terminal
    def send_file(self,file_name):
        #print(file_name)
        file_contents = None
        #open(file_name).read()
        try:
            file_contents = open(file_name).read()
        except FileNotFoundError:
            self.send_header(404)
            #input_sockets.remove(self.the_socket)
            #del self
            return

        #self.the_socket.send(file_contents)
        self.send_header(200)
        self.send_to_client(file_contents)

    # Sends a string message to a client's terminal
    def send_to_client(self, message):
        print(message)
        total_sent = 0
        message_size = sys.getsizeof(message)-49
        print(message_size)
        while total_sent < message_size :
            bytes_sent = self.the_socket.send(message[total_sent:].encode())
            total_sent = total_sent + bytes_sent
            #print(bytes_sent)

class BluetoothSocket:

    socket_AF = socket.AF_BLUETOOTH 
    
    socket_conn_mode = socket.SOCK_STREAM
    protocol = socket.BTPROTO_RFCOMM
    bluetooth_address:str = None
    bluetooth_channel:int = None
    _socket:socket.socket = None
    
    def __init__(self, bluetooth_address:str='', bluetooth_port:int=0):
        self.bluetooth_address = bluetooth_address
        self.bluetooth_channel = bluetooth_port
        self.create_socket()
        pass

    def create_socket(self):
        if self._socket is None:
            self._socket = socket.socket(family=self.socket_AF, type=self.socket_conn_mode, proto=self.protocol )
            self._socket.bind((self.bluetooth_address, self.bluetooth_channel))

        else:
            raise Exception(f"A socket with the following criteria \naddress family:{self.socket_AF}\n socket already exists")
        pass

    def kill_socket(self):
        self._socket.close()
        pass


print(socket.AF_BLUETOOTH)
my_socket = BluetoothSocket()

sleep(10)
my_socket.kill_socket()
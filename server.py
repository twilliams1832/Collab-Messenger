import threading
import queue
from socket import *
import sys
import select
import signal

class Server():
    def __init__(self):
        self.IP = '127.0.0.1'
        self.port = 21000
        self.address = (self.IP, self.port)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setblocking(0)
        self.socket.bind(self.address)
        self.inputs = [ self.socket ]
        self.outputs = []
        self.output_buffer = []
        self.clients = {}

        #Register Ctrl-C Sighandler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        #Listen for two client connections
        try:
            self.socket.listen(2)
            
        except:
            print('Error')
        
        self.client_message_queues = {}

        self.thread_continue = True
        self.output_thread = threading.Thread(target=self.output)
        #self.output_thread.start()
        self.wait_for_input()


    def server_shutdown(self):
        message = ['c', 'SERVER_OFFLINE']

        for client in self.clients:
            self.clients[client].send(str(message).encode())

        self.cleanup()
    

    def cleanup(self):
        self.thread_continue = False
        self.socket.close()
        if self.output_thread.is_alive():
            self.output_thread.join()
        
        if self.output_thread.is_alive():
            print('ERROR: thread still alive')

        else:
            sys.exit()
        
    def signal_handler(self, signum, frame):
        print("\nSignal->", signum, frame)
        #Send server shutdown command
        self.server_shutdown()
        
        
    def output(self):
        while self.thread_continue:
            try:
                output_message = input()
                print("Server message:", output_message)
                self.process_server_message(output_message)
                
            except KeyboardInterrupt:
                self.server_shutdown()


    def process_server_message(self, message):
        pass
    
    def wait_for_input(self):
        print('Listening...')
        while self.inputs:
            #Wait for sockets to be ready for processing
            readable, writable, exceptional = select.select(self.inputs,
                                                            self.outputs,
                                                            self.inputs, 0)
            #Handle inputs
            for s in readable:
                if s is self.socket:
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    self.inputs.append(connection)
                    print("Client", connection.getpeername(),
                          "connected")

                    #Append connection to clients
                    if len(self.clients) == 0:
                        self.clients['a'] = connection

                        message = ['c', 'PEER_NOT_READY']
                        connection.send(str(message).encode())

                    else:
                        self.clients['b'] = connection
                        message = ['c', 'PEER_READY']

                        #Send peer ready command to both clients
                        for client in self.clients:
                            self.clients[client].send(str(message).encode())

                    #Give client a message queue
                    self.client_message_queues[connection] = queue.Queue()

                else:
                    try:
                        data = s.recv(1024)

                    except:
                        message = ['c', 'PEER_DISCONNECTED']
                        for client in self.clients:
                            if s == self.clients[client]:
                                print("Client ", client,
                                      " disconnected")

                                if client == 'a':
                                    if 'b' in self.clients:
                                        self.clients['b'].send(str(message).encode())
                                        print("Sent:", str(message))

                                else:
                                    if 'a' in self.clients:
                                        self.clients['a'].send(str(message).encode())
                                        print("Sent:", str(message))
                                
                            break

                        #Remove connection from outputs and inputs
                        if s in self.outputs:
                            self.outputs.remove(s)
                        self.inputs.remove(s)

                        #Remove connection from readable and writable
                        if s in writable:
                            writable.remove(s)
                        readable.remove(s)

                        #Close and remove connection from client list
                        if 'a' in self.clients.keys():
                            if s == self.clients['a']:
                                self.clients['a'].close()
                                del self.clients['a']


                        if 'b' in self.clients.keys():
                            if s == self.clients['b']:
                                self.clients['b'].close()
                                del self.clients['b']

                               
                            
                    if data:
                        receiver = None
                        
                        if 'a' in self.clients.keys():
                            if s == self.clients['a']:
                                if 'b' in self.clients.keys():
                                    receiver = self.clients['b']
                                    client_id = 'a'

                        if 'b' in self.clients.keys():
                            if s == self.clients['b']:
                                if 'a' in self.clients.keys():
                                    receiver = self.clients['a']
                                    client_id = 'b'
                                    
                        print("Received data from client ",
                              client_id, ":", data)

                        message = ['m', data.decode()]
                        if receiver != None:
                            self.client_message_queues[receiver].put(str(message).encode())

                            if receiver not in self.outputs:
                                #print('Appended ', s.getpeername())
                                self.outputs.append(receiver)
                    else:
                        pass

            #Handle outputs
            for s in writable:
                try:
                    next_msg = self.client_message_queues[s].get_nowait()
                    
                except queue.Empty:
                    pass

                else:
                    if s not in self.clients.values():
                        #Flush next_msg
                        pass
                    
                    else:
                        print("Message sent ", next_msg.decode())
                        try:
                            s.send(next_msg)
                        except:
                            pass

            #Handle exceptional conditions
            for s in exceptional:
                pass


if __name__ == '__main__':
    server = Server()
                    

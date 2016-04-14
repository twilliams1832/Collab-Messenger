import threading
from socket import *
import sys
import select
from tkinter import *
import GUI
import queue

class Client():
    def __init__(self, server_address):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.server_address = (server_address, 21000)
        #self.socket.settimeout(30)
        
        try:
            self.socket.connect(self.server_address)
            #self.socket.settimeout(None)
            
        except Exception as inst:
            print("Could not connect to server ", str(inst))
            sys.exit()

        else:
            self.polling = True
            self.input_buffer = []
            self.GUI = GUI.GUI(self)
            self.main_thread = threading.Thread(target=self.wait_for_input)
            self.main_thread.start()
            self.message_queue = queue.Queue()

    def wait_for_input(self):
        while self.polling:
            try:
                self.receive_message()
            except:
                pass

            

    def send_message(self, message):
        self.socket.send(message.encode())


    def process_message(self, _message):
        print("Message", _message)
        #Messages should be in form of:
        #['op_code', 'MESSAGE']
        #Ex. ['c', 'PEER_NOT_READY']

        response = eval(_message)
        command = response[0]
        message = response[1]

        
        
        if command == 'c':
            if message == 'PEER_NOT_READY':
                self.GUI.disable_entry()

            elif message == 'PEER_READY':
                self.GUI.enable_entry()

            elif message == 'SERVER_OFFLINE':
                self.server_offline()

            elif message == 'PEER_DISCONNECTED':
                self.partner_disconnected()
                
            else:
                pass
            
        #Regular message command    
        elif command == 'm':
            self.GUI.receive_message(message)

        else:
            pass
        
    def receive_message(self):
        try:
            message = self.socket.recv(1024)
            self.process_message(message.decode())
        except:
            print(str(sys.exc_info[0]))
        
        

    def partner_disconnected(self):
        self.GUI.message('Peer disconnected', 'Peer went offline')
        self.GUI.disable_entry()
        
    def server_offline(self):
        self.GUI.message('Connection Error', 'Server went offline')
        self.GUI.disable_entry()
        self.cleanup()
        
    def cleanup(self):
        self.polling = False
        self.socket.close()
        self.main_thread.join()

        if self.main_thread.is_alive():
            print('ERROR: thread still alive')

        else:
            sys.exit()
        
if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    client = Client('localhost')
    root.mainloop()
    

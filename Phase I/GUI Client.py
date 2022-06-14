 import socket #------------- Socket library
from tkinter import * #----- GUI library



#--------------------------------------------------------------------------------------------
# Initialization 
#--------------------------------------------------------------------------------------------
#############################################################################################

Client = socket.socket()#---------------------- Initialize the client socket
host = socket.gethostname()#------------------- Get the client name
ip = socket.gethostbyname(host)#--------------- Get the client IP address
print('Client IP: ',ip,'\n\n')#---------------- Printing the client IP address on the CLI
print('Please enter the server IP and press connect to start chatting...')
##############################################################################################










#-----------------------------------------------------------------------------------------------------------------------------------------------------
# Methods for conncting to the server, Sending and Receiving messages to and from Cleint and exiting the conversation  
#-----------------------------------------------------------------------------------------------------------------------------------------------------
######################################################################################################################################################
def connect():
    host = IP_address.get()#----------------------------- Get the server IP adress that was enterd by the client 
    port = 1234#----------------------------------------- Assigning the port variable to the server port
    Client.connect((host, port))#------------------------ Start calling the server with the connect() method


    
def send():
    message = Message_Entry.get()#----------------------- Get the message that was typed by Me(Client) and save it to message variable.
    Client.send(message.encode())#----------------------- Encode the message to bytes because that what sockets deals with, then send it to the server. 
    Text_Box.insert(END,"Me: "+ message)#---------------- Insert the message that was sent by Me(Client) in the text box.
   
        

def receive():
    message = Client.recv(1024)#------------------------- Receive the message that was sent by the server with buffer size of 1024 bytes. 
    message = "Server: " + message.decode()#------------- Decode the message from bytes so that it can be shown in the text box.
    Text_Box.insert(END, message)#----------------------- Insert the server's message in the text box.



def exit():
    message = "The Connction was cut by the client."#--- A message that indicates the clinet has exited
    Client.send(message.encode())#---------------------- Encode the message to bytes because that what sockets deals with, then send it to the server. 
    Client.close()#------------------------------------- Close the client socket
    root.quit()#---------------------------------------- Colse the GUI frame

######################################################################################################################################################










#--------------------------------------------------------------------------------------------------
# GUI Initializing
#--------------------------------------------------------------------------------------------------
###################################################################################################

root = Tk()#-------------------------------- Initialize the main frame
root.geometry("600x569+650+150")#----------- Determine its geometry
root.title("Chat app")#--------------------- Set its title


#------------------------------------------- IP address Entry box
IP_address = Entry(root)
IP_address.place(relx=0.2, rely=0.035,height=34, relwidth=0.357)


#------------------------------------------- Connect button
Connect = Button(root,text="Connect",background="#00c131",foreground="#ffffff",command=connect)
Connect.place(relx=0.083, rely=0.035, height=33, width=66)

#------------------------------------------- Send button
Send = Button(root,text="Send",background="#0080ff",foreground="#ffffff",command=send)
Send.place(relx=0.067, rely=0.633, height=60, width=75)


#------------------------------------------- Receive button
Receive = Button(root,text="Display",background="#d9d9d9",foreground="#000000",command=receive)
Receive.place(relx=0.067, rely=0.160, height=100, width=75)

#------------------------------------------- Exit button
Exit = Button(root,text="Exit",background="#d9d9d9",foreground="#000000", command=exit)
Exit.place(relx=0.417, rely=0.844, height=33, width=116)


#------------------------------------------- Messages Entery box
Message_Entry = Entry(root)
Message_Entry.place(relx=0.2, rely=0.622,height=74, relwidth=0.707)


#------------------------------------------- Messages Display box
Text_Box = Listbox(root)
Text_Box.place(relx=0.2, rely=0.156, relheight=0.439, relwidth=0.707)


#------------------------------------------- Main loop for the GUI
root.mainloop()

######################################################################################################

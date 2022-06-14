import socket #------------- Socket library
from tkinter import * #----- GUI library



#--------------------------------------------------------------------------------------------
# Initialization 
#--------------------------------------------------------------------------------------------
#############################################################################################

print("Initializing....\n")
s = socket.socket() #----------------------- Initialize the server socket
port = 1234 #------------------------------- Assign a server port
host = socket.gethostname()#---------------- Get the server name
ip = socket.gethostbyname(host)#------------ Get the server IP address
s.bind((host, port))#----------------------- Binding the server's host and port to its socket
print('Server IP: ',ip,'\n')#--------------- Printing the server IP address on the CLI

##############################################################################################





#------------------------------------------------------------------------------------------------------------------------------------------------
# Listening for calls and accepting them  
#------------------------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################################

print("Wating for the client to call...")

s.listen(1)#--------------------------------------- Listening for calls coming from the Client.
Connection_channel, addr = s.accept()#------------------- After receiving a call, the server accepts it and establish a channel to communicate through.

##################################################################################################################################################





#-----------------------------------------------------------------------------------------------------------------------------------------------------
# Methods for Sending and Receiving messages to and from Cleint
#-----------------------------------------------------------------------------------------------------------------------------------------------------
######################################################################################################################################################

def send():
    message = Message_Entry.get()#----------------------- Get the message that was typed by Me(Server) and save it to message variable.
    Connection_channel.send(message.encode())#----------- Encode the message to bytes because that what sockets deals with, then send it to the client 
    Text_Box.insert(END,"Me: "+ message)#---------------- Insert the message that was sent by Me(Server) in the text box.
   
        

def receive():
    message = Connection_channel.recv(1024)#------------- Receive the message that was sent by the client with buffer size of 1024 bytes. 
    message = "Client: " + message.decode()#------------- Decode the message from bytes so that it can be shown in the text box.
    Text_Box.insert(END, message)#----------------------- Insert the Client's message in the text box.

######################################################################################################################################################





#--------------------------------------------------------------------------------------------------
# GUI Initializing
#--------------------------------------------------------------------------------------------------
###################################################################################################

root = Tk()#-------------------------------- Initialize the main frame
root.geometry("600x569+650+150")#----------- Determine its geometry
root.title("Chat app")#--------------------- Set its title

#------------------------------------------- Send button
Send = Button(root,text="Send",background="#0080ff",foreground="#ffffff",command=send)
Send.place(relx=0.067, rely=0.633, height=60, width=75)


#------------------------------------------- Receive button
Receive = Button(root,text="Display",background="#d9d9d9",foreground="#000000",command=receive)
Receive.place(relx=0.067, rely=0.160, height=100, width=75)


#------------------------------------------- Messages Entery box
Message_Entry = Entry(root)
Message_Entry.place(relx=0.2, rely=0.622,height=74, relwidth=0.707)


#------------------------------------------- Messages Display box
Text_Box = Listbox(root)
Text_Box.place(relx=0.2, rely=0.156, relheight=0.439, relwidth=0.707)



root.mainloop()#---------------------------- Main loop for the GUI

######################################################################################################

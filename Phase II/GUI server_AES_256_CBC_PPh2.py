import socket #------------- Socket library
from tkinter import * #----- GUI library



#-------------------------------------------------------------------------------------------------------------------
# The crypto library was installed using the following command: >> pip3 install pycryptodome
#-------------------------------------------------------------------------------------------------------------------
####################################################################################################################
from Crypto.Cipher import AES#------------------------------ AES crypto system 
from Crypto.Hash import SHA256#----------------------------- Sha256 hash function 
from Crypto.Random import get_random_bytes#----------------- Random bytes generator to be used in generating IV
from Crypto.Util.Padding import pad, unpad#----------------- Padding and unpadding functions


key = '201337310'.encode()#--------------------------------- Encoding my ID to bytes to be used in the hash function
Hashed_key = SHA256.new(key).digest()#---------------------- The hash function that hashes the ID
print("The hashed key of 201337310: ", Hashed_key.hex())#--- Print the hashed key on the CMD
####################################################################################################################
        





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
print('Server IP: ',ip,'\n')#--------------- Printing the server IP address on the CMD

##############################################################################################





#------------------------------------------------------------------------------------------------------------------------------------------------
# Listening for calls and accepting them  
#------------------------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################################

print("Wating for the client to call...")

s.listen(1)#--------------------------------------- Listening for calls coming from the Client.
Connection_channel, addr = s.accept()#------------- After receiving a call, the server accepts it and establish a channel to communicate through.
iv = Connection_channel.recv(16)#------------------ Receiving the IV from the client side 

##################################################################################################################################################





#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Methods for Sending and Receiving messages to and from Cleint with AES_256_CBC crypto system
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
##############################################################################################################################################################

def send():

    message = Message_Entry.get()#----------------------------------- Get the message that was typed by Me(Server) and save it to message variable
    cipher1 = AES.new(Hashed_key, AES.MODE_CBC, iv)#----------------- The cipher function of the encryption that takes the key, the mode and the IV as inputs
    ct = cipher1.encrypt(pad(message.encode(),16))#------------------ The encryption function with the padding function that generates the ciphertext
    Connection_channel.send(ct)#------------------------------------- Sending the ciphertext of the server's message to the client 
    Text_Box.insert(END,"My plaintext: "+ message)#------------------ Displaying the plaintext of Me(server)
    Text_Box.insert(END,"Shared IV: "+cipher1.iv.hex())#------------- Displaying the Shared IV in hexadicemal 
    Text_Box.insert(END,"My chiphertext: "+ct.hex())#---------------- Displaying the ciphertext of Me(server) in hexadicemal 
    Text_Box.insert(END,"")#----------------------------------------- Print a line
        

def receive():
   
    message = Connection_channel.recv(1024)#------------------------- Receive the message that was sent by the client with buffer size of 1024 bytes. 
    cipher2 = AES.new(Hashed_key, AES.MODE_CBC, iv)#----------------- The cipher function of the decryption that takes the key, the mode and the IV as inputs 
    pt = unpad(cipher2.decrypt(message),16)#------------------------- The decryption function with the unpadding function that generates the plaintext
    mpt = pt.decode()#----------------------------------------------- Decode the plaintext from bytes so that it can be shown in the text box
    Text_Box.insert(END,"Client's ciphertext: "+ message.hex())#----- Displaying the ciphertext of the otherside(client) in hexadicemal  
    Text_Box.insert(END,"Shared IV: "+cipher2.iv.hex())#------------- Displaying the shared IV in hexadicemal 
    Text_Box.insert(END,"Client's plaintext: "+mpt)#----------------- Displaying the plaintext of the otherside(client) 
    Text_Box.insert(END,"")#----------------------------------------- Print a line
##############################################################################################################################################################





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

###################################################################################################


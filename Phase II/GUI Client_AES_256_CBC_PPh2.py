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
IV = get_random_bytes(16)
####################################################################################################################






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
# Methods for conncting to the server, Sending and Receiving messages to and from server with AES_256_CBC crypto system and exiting the conversation  
#-----------------------------------------------------------------------------------------------------------------------------------------------------
######################################################################################################################################################
def connect():
    host = IP_address.get()#----------------------------------------- Geting the server IP adress that was enterd by the client 
    port = 1234#----------------------------------------------------- Assigning the port variable to the server port
    Client.connect((host, port))#------------------------------------ Start calling the server with the connect() method
    Client.send(IV)#------------------------------------------------- Sending the IV to the server side 
    
        
def send():
    message = Message_Entry.get()#----------------------------------- Geting the message that was typed by Me(Client) and save it to message variable.
    cipher1 = AES.new(Hashed_key, AES.MODE_CBC, IV)#----------------- The cipher function of the encryption that takes the key, the mode and the IV as inputs
    ct = cipher1.encrypt(pad(message.encode(),16))#------------------ The encryption function with the padding function that generates the ciphertext
    Client.send(ct)#------------------------------------------------- Sending the ciphertext of the client's message to the server 
    Text_Box.insert(END,"My plaintext: "+ message)#------------------ Displaying the plaintext of Me(client)
    Text_Box.insert(END,"Shared IV: "+cipher1.iv.hex())#------------- Displaying the Shared IV in hexadicemal 
    Text_Box.insert(END,"My chiphertext: "+ct.hex())#---------------- Displaying the ciphertext of Me(client) in hexadicemal
    Text_Box.insert(END,"")#----------------------------------------- Print a line
        

def receive():
    
    message = Client.recv(1024)#------------------------------------- Receive the message that was sent by the server with buffer size of 1024 bytes. 
    cipher2 = AES.new(Hashed_key, AES.MODE_CBC, IV)#----------------- The cipher function of the decryption that takes the key, the mode and the IV as inputs 
    pt = unpad(cipher2.decrypt(message),16)#------------------------- The decryption function with the unpadding function that generates the plaintext
    mpt = pt.decode()#----------------------------------------------- Decode the message from bytes so that it can be shown in the text box.
    Text_Box.insert(END,"Server's ciphertext: "+ message.hex())#----- Displaying the ciphertext of the otherside(Server) in hexadicemal 
    Text_Box.insert(END,"Shared IV: "+cipher2.iv.hex())#------------- Displaying the shared IV in hexadicemal 
    Text_Box.insert(END,"Server's plaintext: "+mpt)#----------------- Displaying the plaintext of the otherside(Server)
    Text_Box.insert(END,"")#----------------------------------------- Print a line


def exit():
    message = "The Connction was cut by the client."#---------------- A message that indicates the clinet has exited
    Client.send(message.encode())#----------------------------------- Encode the message to bytes because that what sockets deals with, then send it to the server. 
    Client.close()#-------------------------------------------------- Close the client socket
    root.quit()#----------------------------------------------------- Colse the GUI frame

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

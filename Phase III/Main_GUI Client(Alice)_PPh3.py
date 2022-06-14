import socket #------------- Socket library
from tkinter import * #----- GUI library
import time #--------------- Time library

#-------------------------------------------------------------------------------------------------------------------
# The crypto library was installed using the following command: >> pip3 install pycryptodome
#-------------------------------------------------------------------------------------------------------------------
####################################################################################################################
from Crypto.Cipher import AES#------------------------------ AES crypto system 
from Crypto.Hash import SHA256#----------------------------- Sha256 hash function 
from Crypto.Random import get_random_bytes#----------------- Random bytes generator to be used in generating IV
from Crypto.Util.Padding import pad, unpad#----------------- Padding and unpadding functions




#-----------------------------------------------------------------------------------------------------
# RSA credentials for both Alice(Client) and Bob(Server) public key of both and private key for Alice 
#-----------------------------------------------------------------------------------------------------
N_Bob = 15087901461302145926152661281728621908195308879932886656790145723523545901479279301546123923946190657457479724190879902146613302214570147947970214792592614859326126148392859548570815281970882126593282193327905705727972439239261505972661683928395083995239706395306439906595506639996796819063530219241485952641552797263801984982842534096294028942738269336473602466756226688987654098320320096540762762540094316316093648980980758313646756534089422533409854076075853407629629406962294294071626960069847402735846734289622733622276498498275831163162940495828938716271604715603158491602491156489600489155587587364920253363140696029140027582916026915581
e_Bob = 3
N_Alice = 9817766666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666670379887169999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999874799999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999581325509666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666555969
e_Alice = 5
d_Alice = 1963553333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333334075977433999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999973706666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666582695006399999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999977869
###################################################################################################################
#d_Alice = 5


#--------------------------------------------------------------------------------------------
# Diffie-Hellman credentials for sharing keys that both Alice and Bob have the same
#--------------------------------------------------------------------------------------------
g = 2
m = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF", 16)
###################################################################################################################






#--------------------------------------------------------------------------------------------
# Initialing socket
#--------------------------------------------------------------------------------------------
#############################################################################################
Client = socket.socket()#---------------------- Initialize the client socket
host = socket.gethostname()#------------------- Get the client name
ip = socket.gethostbyname(host)#--------------- Get the client IP address
Alice_id = ip#--------------------------------- To be used instead of Alice's name
print('Client IP: ',ip,'\n\n')#---------------- Printing the client IP address on the CLI
print('Please enter the server IP and press connect to start chatting...')
##############################################################################################






#-----------------------------------------------------------------------------------------------------------------------------------------------------
# Conncting to the server and applying the modified SSH protocol
#-----------------------------------------------------------------------------------------------------------------------------------------------------
######################################################################################################################################################
def connect():
    host = IP_address.get()#----------------------------------------- Geting the server IP adress that was enterd by the client 
    port = 1234#----------------------------------------------------- Assigning the port variable to the server port
    Client.connect((host, port))#------------------------------------ Start calling the server with the connect() method
    Bob_id = host#--------------------------------------------------- To be used instead of Bob name


    #------------------------------------------------------------------------------------------------------
    # Initialing the needed variables
    #------------------------------------------------------------------------------------------------------
    #######################################################################################################
    global k #--------------------------------------- The hash of the shared key that is H(g^ab mod m)
    global IV#--------------------------------------- Intialization vector
    a = int(get_random_bytes(256).hex(), 16)#-------- Alice's secret that is randomly picked as 256 bytes
    RA = int(get_random_bytes(32).hex(), 16)#-------- Alice's response that is randomly picked as 32 bytes
    Alice_key = pow(g,a,m)#-------------------------- Alice's key that is g^a mod m
    IV = get_random_bytes(16)#----------------------- Intialization vector
    Client.send(bytes(IV.hex(),'utf-8'))#------------ Sending the IV to the server side
    Client.send(" ".encode())
    #######################################################################################################
    print('\n')
    print("a: ",a)#---------------------------------- printing a before destroying it
    print('\n')
   

    #------------------------------------------------------------------------------------------------------
    # Step 1 in the protocol (Sending Alice's message)
    #------------------------------------------------------------------------------------------------------
    #######################################################################################################
    Client.send(bytes(str(Alice_key), 'utf-8'))#------------------ Sending Alice's key
    Client.send(" ".encode())
    Client.send(bytes(str(RA),'utf-8'))#-------------------------- Sending Alice's response
    #######################################################################################################


    #------------------------------------------------------------------------------------------------------
    # Step 2 in the protocol (Receiving Bob's message)
    #------------------------------------------------------------------------------------------------------
    #######################################################################################################
    time.sleep(4)#------------------------------- wating for the buffer to be loaded
    data = Client.recv(2048)#-------------------- receiving Bob's message that includes RB, Bob's key and SB 
    data2 = str(data).split(" ")
    Bob_key = int(data2[0][2:])#----------------- Bob's key 
    RB = int(data2[1])#-------------------------- RB
    SB = int(data2[2][0:-1])#-------------------- SB
    #######################################################################################################
    

    #--------------------------------------------------------------------------------------------------------------------------
    # After step 2 and before step 3
    #--------------------------------------------------------------------------------------------------------------------------
    ###########################################################################################################################
    H_Bob = pow(SB, e_Bob, N_Bob)#----------------------------- Alice extracts H that was signed by Bob using his public key

    #--------------------------------------------------------------------------------------------------------------------------
    # Alice computes H by using the following credentials to compare it with the H extracted from Bob's SB
    #--------------------------------------------------------------------------------------------------------------------------
    shared_key = pow(Bob_key,a,m)#----------------------------- The shared key that is g^ab mod m using diffie-Hellman concept
    a = 0#----------------------------------------------------- Destroy Alice's secret a
    
    H = SHA256.new(bytes(Bob_id,'utf-8'))#--------------------- Hashing Bob's id that is his ip address
    H.update(bytes(str(Alice_id),'utf-8'))#-------------------- Hashing Alice's id that is her ip address
    H.update(bytes(str(RA),'utf-8'))#-------------------------- Hashing Alice's response 
    H.update(bytes(str(RB),'utf-8'))#-------------------------- Hashing Bob's response
    H.update(bytes(str(Bob_key),'utf-8'))#--------------------- Hashing Bob's key
    H.update(bytes(str(Alice_key),'utf-8'))#------------------- Hashing Alice's key
    H.update(bytes(str(shared_key),'utf-8'))#------------------ Hashing the shared key
    

    #------------------------------------------------------------------------------------------------------------------------------------
    # Alice compares between the computed H and the extracted H in case to proceed to step 3 or not
    #------------------------------------------------------------------------------------------------------------------------------------
    k = SHA256.new(bytes(str(shared_key), 'utf-8')).digest()#--------------- The hashed shared key to be used in the encryption in step 3
    if (H_Bob == int.from_bytes(H.digest(), 'big')):
        print("RA: ",RA)#--------------------------------------------------- printing RA
        print('\n')
        print("RB: ",RB)#--------------------------------------------------- printing RB
        print('\n')
        print("k: ", k.hex())#---------------------------------------------- printing k
        print('\n')
        print("IV: ",IV.hex())#--------------------------------------------- printing IV
        print('\n')
        print('Bob was authenticated')
        #------------------------------------------------------------------------------------------------------------
        # Step 3 in the protocol (Bob was authenticated)
        #------------------------------------------------------------------------------------------------------------
        cipher1 = AES.new(k, AES.MODE_CBC, IV)#-------------- AES_256_CBC cryptosystem object with the key k
        SA = pow(int(H.hexdigest(),16),d_Alice,N_Alice)#----- computing SA to be encrypted
        message = str(Alice_id) +','+ str(SA)#--------------- The message to be encrypted that is Alice's id and SA
        ct = cipher1.encrypt(pad(message.encode(),16))#------ Encryption of message 
        Client.send(ct)#------------------------------------- Sending the encrypted message to Bob

        #--------------------------------------------------------------------------------------------------------------------------
        # Authentication of Bob failed since computed H doesn't match extracted H, so the chat session will be terminated by Alice
        #--------------------------------------------------------------------------------------------------------------------------
    else:
        print('\n')
        print('Bob was NOT authenticated')
        Client.close()#-------------------------------------- Terminate session
        print("The session was terminated")
        

       
#-----------------------------------------------------------------------------------------------------------------------------------------------------
# Methods for Sending and Receiving messages to and from server with AES_256_CBC crypto system using the shared key k
#-----------------------------------------------------------------------------------------------------------------------------------------------------
######################################################################################################################################################        
def send():
    message = Message_Entry.get()#----------------------------------- Geting the message that was typed by Me(Client) and save it to message variable.
    cipher1 = AES.new(k, AES.MODE_CBC, IV)#-------------------------- The cipher function of the encryption that takes the key, the mode and the IV as inputs
    ct = cipher1.encrypt(pad(message.encode(),16))#------------------ The encryption function with the padding function that generates the ciphertext
    Client.send(ct)#------------------------------------------------- Sending the ciphertext of the client's message to the server 
    Text_Box.insert(END,"My plaintext: "+ message)#------------------ Displaying the plaintext of Me(client)
    Text_Box.insert(END,"Shared IV: "+cipher1.iv.hex())#------------- Displaying the Shared IV in hexadicemal 
    Text_Box.insert(END,"My chiphertext: "+ct.hex())#---------------- Displaying the ciphertext of Me(client) in hexadicemal
    Text_Box.insert(END,"")#----------------------------------------- Print a line
        

def receive():
    
    message = Client.recv(1024)#------------------------------------- Receive the message that was sent by the server with buffer size of 1024 bytes. 
    cipher2 = AES.new(k, AES.MODE_CBC, IV)#-------------------------- The cipher function of the decryption that takes the key, the mode and the IV as inputs 
    pt = unpad(cipher2.decrypt(message),16)#------------------------- The decryption function with the unpadding function that generates the plaintext
    mpt = pt.decode()#----------------------------------------------- Decode the message from bytes so that it can be shown in the text box.
    Text_Box.insert(END,"Server's ciphertext: "+ message.hex())#----- Displaying the ciphertext of the otherside(Server) in hexadicemal 
    Text_Box.insert(END,"Shared IV: "+cipher2.iv.hex())#------------- Displaying the shared IV in hexadicemal 
    Text_Box.insert(END,"Server's plaintext: "+mpt)#----------------- Displaying the plaintext of the otherside(Server)
    Text_Box.insert(END,"")#----------------------------------------- Print a line


def exit():
    message = "The Connction was cut by the client."#---------------- A message that indicates the clinet has exited
    Client.send(message.encode())#----------------------------------- Encode the message to bytes because that what sockets deals with, then send it to the server. 
    k = 0#----------------------------------------------------------- destroying k
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

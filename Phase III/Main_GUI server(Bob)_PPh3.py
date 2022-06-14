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
d_Bob = 10058600974201430617435107521152414605463539253288591104526763815682363934319519534364082615964127104971653149460586601431075534809713431965313476528395076572884084098928573032380543521313921417728854795551937137151981626159507670648441122618930055996826470930204293271063671093331197879375686812827657301761035198174962715900876153234552785544181054835749942370967437185843619914728059902864344342859888034699883585799130981350237636153188742815324953099764948643456788639007887886403438993058241944164904154523410816741102582581098133680345529231452184034403290696613649203275866969189929186963176508358727615013530566120192776478699438696467   
############################################################################################
#d_Bob = 5

#--------------------------------------------------------------------------------------------
# Diffie-Hellman credentials for sharing keys that both Alice and Bob have the same
#--------------------------------------------------------------------------------------------
g = 2
m = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF", 16)
#############################################################################################



#--------------------------------------------------------------------------------------------
# Initialing socket
#--------------------------------------------------------------------------------------------
#############################################################################################
print("Initializing....\n")
s = socket.socket() #----------------------- Initialize the server socket 
port = 1234 #------------------------------- Assign a server port
host = socket.gethostname()#---------------- Get the server name
ip = socket.gethostbyname(host)#------------ Get the server IP address
Bob_id = ip#-------------------------------- To be used instead of Bob's name
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
Alice_id = addr[0]#-------------------------------- To be used instead of Alice's name
#################################################################################################################################################


#------------------------------------------------------------------------------------------------------
# Initialing the needed variables
#------------------------------------------------------------------------------------------------------
#######################################################################################################
b = int(get_random_bytes(256).hex(), 16)#--------------- Bob's secret
RB = int(get_random_bytes(32).hex(),16)#---------------- Bob's response
Bob_key = pow(g,b,m)#----------------------------------- Bob's key that is g^b mod m


#-------------------------------------------------------------------------------------------------------------------
# Step 1 in the protocol (Receiving Alice's message)
#-------------------------------------------------------------------------------------------------------------------
####################################################################################################################
time.sleep(2)#----------------------------------------- wating for the buffer to be loaded
data = Connection_channel.recv(1024)#------------------ Receiving the message that comes from Alice's side 
data2 = str(data).split(" ")
iv = bytearray.fromhex((data2[0])[2:])#---------------- Receiving the IV from the client side for ASE cryptosystem
Alice_key = int(data2[1])#----------------------------- Alice's key
RA = int((data2[2])[0:-1])#---------------------------- Alice's response
print('\n')
print("b: ",b)#----------------------------------------- printing b




#---------------------------------------------------------------------------------------------------------------------------
# Step 2 in the protocol (Sending Bob's message)
#---------------------------------------------------------------------------------------------------------------------------
############################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------
# Bob computes H by using the following credentials to compute SB
#---------------------------------------------------------------------------------------------------------------------------
shared_key = pow(Alice_key,b,m)#----------------------------- The shared key that is g^ab mod m using diffie-Hellman concept
b = 0#------------------------------------------------------- Destroy Bob's secret b

H = SHA256.new(bytes(Bob_id,'utf-8'))#----------------------- Hashing Bob's id that is his ip address
H.update(bytes(str(Alice_id),'utf-8'))#---------------------- Hashing Alice's id that is her ip address
H.update(bytes(str(RA),'utf-8'))#---------------------------- Hashing Alice's response
H.update(bytes(str(RB),'utf-8'))#---------------------------- Hashing Bob's response
H.update(bytes(str(Bob_key),'utf-8'))#----------------------- Hashing Bob's key
H.update(bytes(str(Alice_key),'utf-8'))#--------------------- Hashing Alice's key
H.update(bytes(str(shared_key),'utf-8'))#-------------------- Hashing the shared key


SB = pow(int(H.hexdigest(),16),d_Bob,N_Bob)#----------------- computing SB to be sent to Alice


Connection_channel.send(bytes(str(Bob_key), 'utf-8'))#------- Sending Bob's key
Connection_channel.send(" ".encode())
Connection_channel.send(bytes(str(RB),'utf-8'))#------------- Sending Bob's response
Connection_channel.send(" ".encode())
Connection_channel.send(bytes(str(SB), 'utf-8'))#------------ Sending SB


#---------------------------------------------------------------------------------------------------------------------------------
# Step 3 in the protocol (Receiving Alice's message)
#---------------------------------------------------------------------------------------------------------------------------------
##################################################################################################################################
k = SHA256.new(bytes(str(shared_key), 'utf-8')).digest()#------------ The hashed shared key to be used in the encryption in step 3
ct = Connection_channel.recv(1024)#---------------------------------- Receiving the encrypted message
cipher2 = AES.new(k, AES.MODE_CBC, iv)#------------------------------ AES_256_CBC cryptosystem object with the key k
pt = unpad(cipher2.decrypt(ct),16)#---------------------------------- The decryption of Alice's encrypted message
pt2 = str(pt).split(',')

SA = int((pt2[1])[:-1])#--------------------------------------------- Extracting SA from Alice's plaintext
H_Alice = pow(SA, e_Alice, N_Alice)#--------------------------------- Extracting H of Alice from SA  
###################################################################################################################################



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# After Step 3 and before step 4(step of exchanging messages) that Bob compares his H against Alice's H if they matches the Alice's was authenticated and Bob can proceed to step 4,
# otherwise the session will be terminated
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#####################################################################################################################################################################################
if (H_Alice == int.from_bytes(H.digest(), 'big')):
        print('\n')
        print("RA: ",RA)#--------------------------------------- printing RA
        print('\n')
        print("RB: ",RB)#--------------------------------------- printing RB
        print('\n')
        print("k: ", k.hex())#---------------------------------- printing k
        print('\n')
        print("IV: ",iv.hex())#--------------------------------- printing IV
        print('\n')
        print('Alice was authenticated')
        
else:
        print('\n')
        print('Alice was NOT authenticated')
        Connection_channel.close()#--------- Terminate session
        print("The session was terminated")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Methods for Sending and Receiving messages to and from Cleint with AES_256_CBC crypto system
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
##############################################################################################################################################################

def send():

    message = Message_Entry.get()#----------------------------------- Get the message that was typed by Me(Server) and save it to message variable
    cipher1 = AES.new(k, AES.MODE_CBC, iv)#----------------- The cipher function of the encryption that takes the key, the mode and the IV as inputs
    ct = cipher1.encrypt(pad(message.encode(),16))#------------------ The encryption function with the padding function that generates the ciphertext
    Connection_channel.send(ct)#------------------------------------- Sending the ciphertext of the server's message to the client 
    Text_Box.insert(END,"My plaintext: "+ message)#------------------ Displaying the plaintext of Me(server)
    Text_Box.insert(END,"Shared IV: "+cipher1.iv.hex())#------------- Displaying the Shared IV in hexadicemal 
    Text_Box.insert(END,"My chiphertext: "+ct.hex())#---------------- Displaying the ciphertext of Me(server) in hexadicemal 
    Text_Box.insert(END,"")#----------------------------------------- Print a line
        

def receive():
    

   
    message = Connection_channel.recv(1024)#------------------------- Receive the message that was sent by the client with buffer size of 1024 bytes. 
    cipher2 = AES.new(k, AES.MODE_CBC, iv)#----------------- The cipher function of the decryption that takes the key, the mode and the IV as inputs 
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


#Nikhil Kamichetty (1001679614)
#Aashish Geeshpathy Krishnamurthy (1001715288)

import sys
import time
import socket
import pickle
import random
import datetime
import threading
import MissionTCP_Server as Base

from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler

Chan_Count = 0
Mission_Count = -1

localHost = Base.localHost

Listen_Port = Base.Mapping.get('Ann')

Resp_Port = Base.Mapping.get('A')

Ann_Chan = './Files/Ann/Ann-Chan.txt'
Ann_Jan = './Files/Ann/Ann-Jan.txt'

Ann_Chan_Log = './Files/Ann/AnnChanLog.txt'
Ann_Jan_Log = './Files/Ann/AnnJanLog.txt'

Base.LogWrite(Ann_Chan_Log, 'w', '')
Base.LogWrite(Ann_Jan_Log, 'w', '')

Ann_Chan_Data = Base.ReadFile(Ann_Chan)
Ann_Jan_Data = Base.ReadFile(Ann_Jan)

Exit = threading.Event() 

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    """Handle requests in a separate thread."""

class TCPRequestHandler(BaseRequestHandler):
    
    def handle(self):

        Packet_Rx = self.request.recv(4096)
        Packet_Rx_Decode = pickle.loads(Packet_Rx)
        
        Sender = Base.GetKey(Packet_Rx_Decode.get('Source ID'))

        global Mission3Counter

        if Packet_Rx_Decode.get('Fin Bit') == 1 and Mission3Counter == 7:

            Src_ID = Listen_Port
            Dest_ID = Base.Mapping.get('Jan')
            Seq_Num = Packet_Rx_Decode.get('Acknowledgement Number')
            Ack_Num = Packet_Rx_Decode.get('Sequence Number') + 1
            Packet_Dat = ''
            Priority_Pointer = 0
            Syn_Bit = 0
            Fin_Bit = 1
            Reset_Bit = 0
            Terminate_Bit = 0

            Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, SeqNum, Packet_Dat, Priority_Pointer, Syn_Bit, FinBit, Reset_Bit, Terminate_Bit)

            Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

            Timestamp = time.time()
            Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            Data += 'Mission Complete, Communication with Jan Completed. Step 2.\n\n'
            Base.LogWrite(Ann_Jan_Log, 'a', Data)
            print('Fin Bit Received, Sending Fin Bit to Jan...\n')
            print('Ann Terminating Connection...')
            Exit.set()

        elif Packet_Rx_Decode.get('Urgent Pointer') == 1 and Mission3Counter == 5:
            
            Mission3Counter = 7
            Src_ID = Listen_Port
            Dest_ID = Base.Mapping.get('Jan')
            Seq_Num = Packet_Rx_Decode.get('Acknowledgement Number')                                                                               
            Ack_Num = Packet_Rx_Decode.get('Sequence Number') + len(Packet_Rx_Decode.get('Data'))
            Packet_Dat = 'Meeting Location : 32.76 N, -97.07 W\n'
            Priority_Pointer = 0
            Syn_Bit = 0
            Fin_Bit = 0                                              
            Reset_Bit = 0
            Terminate_Bit = 0
           
            Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

            Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

            Timestamp = time.time()
            Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            Data += 'Received the Following Line - \n'
            Data += Packet_Rx_Decode.get('Data')
            Data += 'Acknowledgement Transmitted along with the Line\n'
            Data += Packet_Dat + '\n\n'
            Base.LogWrite(Ann_Jan_Log, 'a', Data)
            print('Urgent Pointer Received : ' + Packet_Rx_Decode.get('Data'))
            print('\nAnn -> Jan : Meeting Location : 32.76 N, -97.07 W\n')

        elif Packet_Rx_Decode.get('Urgent Pointer') == 1 and Mission3Counter == 1: 
            
            Mission3Counter = 5
            Src_ID = Listen_Port
            Dest_ID = Base.Mapping.get('Jan')
            Seq_Num = Packet_Rx_Decode.get('Acknowledgement Number')                                                                                 
            Ack_Num = Packet_Rx_Decode.get('Sequence Number') + len(Packet_Rx_Decode.get('Data'))
            Packet_Dat = 'PEPPER THE PEPPER\n' 
            Priority_Pointer = 0
            Syn_Bit = 0
            Fin_Bit = 0                                               
            Reset_Bit = 0
            Terminate_Bit = 0

            Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

            Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

            Timestamp = time.time()
            Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            Data += 'Received the Following Line - \n'
            Data += Packet_Rx_Decode.get('Data')
            Data += 'Acknowledgement Transmitted along with the Line\n'
            Data += Packet_Data + '\n\n'
            Base.LogWrite(Ann_Jan_Log, 'a', Data)
            print('Urgent pointer Received : ' + Packet_Rx_Decode.get('Data'))
            print('\nAnn -> Jan : Execute\n' + 'Authorization Code for the AirForce Headquarters:\n' + 'PEPPER THE PEPPER\n')

        elif Mission3Counter < 0:

            if Packet_Rx_Decode.get('Syn Bit') == 1 and Packet_Rx_Decode.get('Acknowledgement Number') == -1:
                
                Src_ID = Listen_Port
                Dest_ID = Packet_Rx_Decode.get('Source ID')
                Seq_Num = random.randint(10000, 99999)
                Ack_Num = Packet_Rx_Decode.get('Sequence Number') + 1
                Packet_Dat = ''
                Priority_Pointer = 0
                Syn_Bit = 1
                Fin_Bit = 0                                               
                Reset_Bit = 0
                Terminate_Bit = 0

                Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

                Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

                Timestamp = time.time()
                Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                
                if Sender == 'Jan':
                    
                    Data += 'Jan Attempted to Connect. Sent Syn Bit -> 1, Step 2 of the Handshake.\n\n'
                    Base.LogWrite(Ann_Jan_Log, 'a', Data)
                
                elif Sender == 'Chan':
                    
                    Data += 'Chan Attempted to Connect. Sent Syn Bit -> 1, Step 2 of the Handshake.\n\n'
                    Base.LogWrite(Ann_Chan_Log, 'a', Data)                      

            elif Packet_Rx_Decode.get('Syn Bit') == 1:

                Src_ID = Listen_Port
                Dest_ID = Packet_Rx_Decode.get('Source ID')
                Seq_Num = Packet_Rx_Decode.get('Acknowledgement Number')
                Ack_Num = Packet_Rx_Decode.get('Sequence Number') + 1
                Priority_Pointer = 0
                Syn_Bit = 0
                Fin_Bit = 0                                              
                Reset_Bit = 0
                Terminate_Bit = 0

                if Sender == 'Jan':
                    
                    try:
                        Packet_Dat = Ann_Jan_Data.pop(0)
                    except IndexError:
                        print('Ann-Jan.txt is Empty.\n\n')

                elif Sender == 'Chan':
                    
                    try:
                        Packet_Dat = Ann_Chan_Data.pop(0)
                    except IndexError:
                        print('Ann-Chan.txt is Empty.\n\n')

                Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

                Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

                Timestamp = time.time()
                Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                
                if Sender == 'Jan':
                   
                    Data += 'Connection with Jan Successful. Step 3 of the Handshake. Following Data Sent.\n'
                    Data += Packet_Dat + '\n\n'
                    Base.LogWrite(Ann_Jan_Log, 'a', Data)
                
                elif Sender == 'Chan':
                    
                    Data += 'Connection with Chan Successful. Step 3 of the Handshake. Following Data Sent.\n'
                    Data += Packet_Data + '\n\n'
                    Base.LogWrite(Ann_Chan_Log, 'a', Data)

            else:

                global Chan_Count 

                if Chan_Count == 5:
                    
                    Chan_Count += 1
                    Mission3Counter = 1
                    print("Terminating Connection With Chan -> Compromised.\n")

                    Src_ID = Listen_Port
                    Dest_ID = Base.Mapping.get('Jan')
                    Seq_Num = random.randint(10000, 99999)                                                                             
                    Ack_Num =  Packet_Rx_Decode.get('Sequence Number') + 1 
                    Packet_Dat = 'Communication with Chan has been Compromised!'
                    Priority_Pointer = 1
                    Syn_Bit = 0
                    Fin_Bit = 0
                    Reset_Bit = 0
                    Terminate_Bit = 0  

                    Response_Packet = Baseer.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

                    Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

                    Timestamp = time.time()
                    Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                    Data += 'Communication with Chan has been Terminated.\n\n'
                    Base.LogWrite(Ann_Jan_Log, 'a', Data)
                    print('Ann -> Jan : Urgent Pointer On : Communication with Chan has been Compromised!')
                    
                    Src_ID = Listen_Port
                    Dest_ID = Base.Mapping.get('Chan')
                    Seq_Num = Packet_Rx_Decode.get('Acknowledgement Number')                                                                                  
                    Ack_Num = Packet_Rx_Decode.get('Sequence Number') + len(Packet_Rx_Decode.get('Data')) 
                    Packet_Dat = ''
                    Priority_Pointer = 0
                    Syn_Bit = 0 
                    Fin_Bit = 0
                    Reset_Bit = 1
                    Terminate_Bit = 1

                    Response_Packet = Baseer.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, SeqNum, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

                    Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

                    Timestamp = time.time()
                    Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                    Data += 'Communication with Chan has been Terminated.\n\n'
                    Base.LogWrite(Ann_Chan_Log, 'a', Data)

                else:

                    Src_ID = Listen_Port
                    Dest_ID = Packet_Rx_Decode.get('Source ID')
                    Seq_Num = Packet_Rx_Decode.get('Acknowledgement Number')
                    Ack_Num = Packet_Rx_Decode.get('Sequence Number') + len(Packet_Rx_Decode.get('Data')) 
                    Priority_Pointer = 0
                    Syn_Bit = 0
                    Fin_Bit = 0                                
                    Reset_Bit = 0
                    Terminate_Bit = 0

                    if Sender == 'Jan':
                        
                        try:
                            Packet_Dat = Ann_Jan_Data.pop(0)
                        except IndexError:

                            Src_ID = Listen_Port
                            Dest_ID = Base.Mapping.get('Jan')
                            Seq_Num = random.randint(10000, 99999)
                            Ack_Num =  Packet_Rx_Decode.get('Sequence Number') + 1 
                            Packet_Dat = 'Communication with Chan has been Compromised!'
                            Priority_Pointer = 1
                            Syn_Bit = 0
                            Fin_Bit = 0
                            Reset_Bit = 0
                            Terminate_Bit = 0                                                            
                            Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Ter_Bit)

                            Base.SerializeAndSendPacket(Response_Packet, Resp_Port)
 
                            Timestamp = time.time()
                            Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                            Data += 'Communication with Chan has been Terminated.\n\n'
                            Base.LogWrite(Ann_Jan_Log, 'a', Data)

                    elif Sender == 'Chan':
                        
                        try:
                            Packet_Data = Ann_Chan_Data.pop(0)
                        except IndexError:
                            pass

                    Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

                    Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

                    Timestamp = time.time()
                    Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                    Data += 'Received the Following Line -\n'
                    Data += Packet_Rx_Decode.get('Data')
                    Data += 'Acknowledgement sent along with the Line - \n'
                    Data += Packet_Dat + '\n\n'

                    if Sender == 'Jan':
                        
                        Base.LogWrite(Ann_Jan_Log, 'a', Data)
                           
                    elif Sender == 'Chan':
                        
                        Base.LogWrite(Ann_Chan_Log, 'a', Data)
                        Chan_Count += 1
                                    
        return

def AgentServer ():
    
    try:
        Server = ThreadedTCPServer((localHost, Listen_Port), TCPRequestHandler)
       
        Server.timeout = 0.01
        Server.daemon_threads = True

        while not Exit.isSet():
            Server.handle_request()   

        Server.server_close()           
    except:
        print('Problem creating Server for Ann.')
    
    sys.exit()

if __name__ == '__main__':
    
    try:
        Exit.clear()                    
        
        Ann_Server = threading.Thread(target = AgentServer, args = ())

        AnnServer.start()

        time.sleep(10)
    except:
        print ("Couldn't create Thread for Ann's Router.")

    try:
        Src_ID = Listen_Port
        Dest_ID = Base.Mapping.get('Chan')
        Seq_Num = random.randint(10000, 99999)
        Ack_Num = -1
        Packet_Dat = ''
        Priority_Pointer = 0
        Syn_Bit = 1
        Fin_Bit = 0                                         
        Reset_Bit = 0
        Terminate_Bit = 0

        Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

        Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

        Timestamp = time.time()
        Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
        Data += "Connection setup with Chan started. Step 1 of the Handshake.\n\n"
        Base.LogWrite(Ann_Chan_Log, 'a', Data)

        while not Exit.isSet():
            pass

        Ann_Server.join()
                
        sys.exit()
    
    except KeyboardInterrupt:
        Exit.set()

        Ann_Server.join()
                
        sys.exit()
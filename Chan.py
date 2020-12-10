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

localHost = Base.localHost

Listen_Port = Base.Mapping.get('Chan')

Resp_Port = Base.Mapping.get('E')

Chan_Jan = './Files/Chan/Chan-Jan.txt'
Chan_Ann = './Files/Chan/Chan-Ann.txt'

Chan_Jan_Log = './Files/Chan/ChanJanLog.txt'
Chan_Ann_Log = './Files/Chan/ChanAnnLog.txt'

Base.LogWrite(Chan_Jan_Log, 'w', '')
Base.LogWrite(Chan_Ann_Log, 'w', '')

Chan_Jan_Data = Base.ReadFile(Chan_Jan)
Chan_Ann_Data = Base.ReadFile(Chan_Ann)

Exit = threading.Event() 

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    """Handle requests in a separate thread."""

class TCPRequestHandler(BaseRequestHandler):
    
    def handle(self):

        Packet_Rx = self.request.recv(4096)
        Packet_Rx_Decode = pickle.loads(Packet_Rx)
        
        Sender = Base.GetKey(Packet_Rx_Decode.get('Source ID'))

        if Packet_Rx_Decode.get('Ter Bit') == 1:
           
            print('Ann -> Ordered Termination of the Connection!\n')
            Exit.set()

        elif Packet_Rx_Decode.get('Syn Bit') == 1 and Packet_Rx_Decode.get('Acknowledgement Number') == -1:

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
                Base.LogWrite(Chan_Jan_Log, 'a', Data)
          
            elif Sender == 'Ann':
               
                Data += 'Ann Attempted to connect. Sent Syn Bit -> 1, Step 2 of the Handshake.\n\n'
                Base.LogWrite(Chan_Ann_Log, 'a', Data)                      

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
                    Packet_Dat = Chan_Jan_Data.pop(0)
                except IndexError:
                    print('Chan-Jan.txt is empty.\n\n')

            elif Sender == 'Ann':
                
                try:
                    Packet_Dat = Chan_Ann_Data.pop(0)
                except IndexError:
                    print('Chan-Ann.txt is empty.\n\n')

            Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

            Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

            Timestamp = time.time()
            Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            
            if Sender == 'Jan':
               
                Data += 'Connection with Jan Successful. Step 3 of the Handshake. Following Data Sent.\n'
                Data += Packet_Dat + '\n\n'
                Base.LogWrite(Chan_Jan_Log, 'a', Data)
            
            elif Sender == 'Ann':
                
                Data += 'Connection with Ann Successful. Step 3 of the Handshake. Following Data Sent.\n'
                Data += Packet_Dat + '\n\n'
                Base.LogWrite(Chan_Ann_Log, 'a', Data)

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
                    Packet_Dat = Chan_Jan_Data.pop(0)
                except IndexError:
                    pass

            elif Sender == 'Ann':
                
                try:
                    Packet_Dat = Chan_Ann_Data.pop(0)
                except IndexError:
                    pass

            Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

            Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

            Timestamp = time.time()
            Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            Data += 'Received the Following Line.\n'
            Data += Packet_Rx_Decode.get('Data')
            Data += 'Acknowledgement sent along with the Line\n'
            Data += Packet_Dat + '\n\n'

            if Sender == 'Jan':
                
                Base.LogWrite(Chan_Jan_Log, 'a', Data)
            
            elif Sender == 'Ann':
                
                Base.LogWrite(Chan_Ann_Log, 'a', Data)

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
        print('Problem Creating Server for Chan.')

    sys.exit()

if __name__ == '__main__':
    
    try:
        Exit.clear()                    

        Chan_Server = threading.Thread(target = AgentServer, args = ())

        Chan_Server.start()

        time.sleep(10)
    except:
        print ("Couldn't create Thread for Chan's Router.")

    try:
        Src_ID = Listen_Port
        Dest_ID = Base.Mapping.get('Jan')
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
        Data += "Connection with Jan started. Step 1 of the Handshake.\n\n"
        Base.LogWrite(Chan_Jan_Log, 'a', Data)

        while not Exit.isSet():
            pass

        Chan_Server.join()
                
        sys.exit()
    except KeyboardInterrupt:
        print('Keyboard interrupt\n')
        Exit.set()

        Chan_Server.join()
                
        sys.exit()
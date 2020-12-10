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

Mission3Counter = -1

localHost = Base.localHost

Listen_Port = Base.Mapping.get('Jan')
Resp_Port = Base.Mapping.get('F')

Jan_Chan = './Files/Jan/Jan-Chan.txt'
Jan_Ann = './Files/Jan/Jan-Ann.txt'

Jan_Chan_Log = './Files/Jan/JanChanLog.txt'
Jan_Ann_Log = './Files/Jan/JanAnnLog.txt'
Jan_AirForce_Log = './Files/Jan/JanAirForceLog.txt'

Base.LogWrite(Jan_Chan_Log, 'w', '')
Base.LogWrite(Jan_Ann_Log, 'w', '')
Base.LogWrite(Jan_AirForce_Log, 'w', '')

Jan_Chan_Data = Base.ReadFile(Jan_Chan)
Jan_Ann_Data = Base.ReadFile(Jan_Ann)

Exit = threading.Event() 

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    """Handle requests in a separate thread."""

class TCPRequestHandler(BaseRequestHandler):
    
    def handle(self):

        Packet_Rx = self.request.recv(4096)
        Packet_Rx_Decode = pickle.loads(Packet_Rx)

        Sender = Base.GetKey(Packet_Rx_Decode.get('Source ID'))
        
        global Mission3Counter

        if Packet_Rx_Decode.get('Fin Bit') == 1 and Mission3Counter == 8:
        
            Timestamp = time.time()
            Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            Data += 'Acknowledgement Received, Communication with Ann Completed.Step 3.\n\n'
            Base.LogWrite(Jan_Ann_Log,'a', Data)
            print('Fin Bit Received...\n')
            print('Jan Ending Connection...')
            Exit.set()
        
        elif Mission3Counter == 6:

            Mission3Counter = 8

            Src_ID = Listen_Port
            Dest_ID = Base.Mapping.get('Ann')
            Seq_Num = Packet_Rx_Decode.get('Acknowledgement Number')
            Ack_Num = Packet_Rx_Decode.get('Sequence Number') + len(Packet_Rx_Decode.get('Data'))    
            Packet_Dat = 'Request to Complete Mission?\n'
            Priority_Pointer = 0
            Syn_Bit = 0
            Fin_Bit = 1
            Reset_Bit = 0
            Terminate_Bit = 0

            Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

            Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

            Timestamp = time.time()
            Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            Data += 'Received the Following Line -\n'
            Data += Packet_Rx_Decode.get('Data')
            Data += 'Acknowledgement sent along with the Below Line. This is the first step of the connection teardown.\n'
            Data += Packet_Dat + '\n\n'
            Base.LogWrite(Jan_Ann_Log, 'a', Data)
            print('Jan -> Ann: Sending Finish Bit to Ann.\n')

        elif Mission3Counter == 4 and incomingPacketDecoded.get('Data') == 'Success!':

            Mission3Counter = 6
            Src_ID = Listen_Port
            Dest_ID = Base.Mapping.get('Ann')
            Seq_Num = Packet_Rx_Decode.get('Acknowledgement Number')
            Ack_Num = Packet_Rx_Decode.get('Sequence Number') + len(Packet_Rx_Decode.get('Data'))
            Packet_Dat = 'The Authorization Code:\n' + 'Congratulations, we have fried dry green leaves!\n' 
            Priority_Pointer = 1
            Syn_Bit = 0
            Fin_Bit = 0                                  
            Reset_Bit = 0
            Terminate_Bit = 0

            Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

            Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

            Timestamp = time.time()
            Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            Data += 'Received the following Line - \n'
            Data += incomingPacketDecoded.get('Data')
            Data += 'Acknowledgement sent along with the Line.\n'
            Data += Packet_Dat + '\n\n'
            Base.LogWrite(Jan_Ann_Log, 'a', Data)
            print('Received Success from Headquarters.\n')
            print('Jan -> Ann : Urgent Pointer On : The Authorization Code :\n' + 'Congratulations, we have fried dry green leaves!\n')

        elif Mission3Counter == 2 and Packet_Rx_Decode.get('Data') == 'PEPPER THE PEPPER\n':

            Src_ID = Listen_Port
            Dest_ID = Base.Mapping.get('H')
            Seq_Num = random.randint(10000, 99999)
            Ack_Num = -1
            Packet_Dat = 'Location of Target : (32° 43 22.77 N,97° 9 7.53 W)\n' + 'The Authorization Code for the AirForce Headquarters:\n' + 'PEPPER THE PEPPER\n' 
            Priority_Pointer = 1
            Syn_Bit = 0
            Fin_Bit = 0                                      
            Reset_Bit = 0
            Terminate_Bit = 0

            Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

            Base.SerializeAndSendPacket(Response_Packet, Base.Mapping.get('H'))

            Timestamp = time.time()
            Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            Data += 'Received the following Line - \n'
            Data += Packet_Rx_Decode.get('Data')
            Data += 'Acknowledgement sent along with the Line\n'
            Data += Packet_Dat + '\n\n'
            Base.LogWrite(Jan_AirForce_Log, 'a', Data)
            Mission3Counter = 4
            print('Recieved Authorization Code from Ann!\n')
            print('Jan -> AirForce: Location of target: (32° 43 22.77 N,97° 9 7.53 W)\n' + 'The Authorization Code for the AirForce Headquarters:\n' + 'PEPPER THE PEPPER\n')

        elif Packet_Rx_Decode.get('Urgent Pointer') == 1:

            Mission3Counter = 2
            Src_ID = Listen_Port
            Dest_ID = Base.Mapping.get('Ann')
            Seq_Num = Packet_Rx_Decode.get('Acknowledgement Number')
            Ack_Num = Packet_Rx_Decode.get('Sequence Number') + len(Packet_Rx_Decode.get('Data'))
            Packet_Dat = 'Location of Target: (32° 43 22.77 N,97° 9 7.53 W)\n' + 'Request for Mission Execution?\n' 
            Priority_Pointer = 1
            Syn_Bit = 0
            Fin_Bit = 0                                         
            Reset_Bit = 0
            Terminate_Bit = 0

            Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

            Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

            Timestamp = time.time()
            Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
            Data += 'Received the following Line - \n'
            Data += Packet_Rx_Decode.get('Data')
            Data += 'Acknowledgement sent along with Line\n'
            Data += Packet_Dat + '\n\n'
            Base.LogWrite(Jan_Ann_Log, 'a', Data)
            print('Urgent Pointer Received : ' + Packet_Rx_Decode.get('Data')) 
            print('Jan -> Ann : Urgent Pointer On : Location of Target : (32° 43 22.77 N,97° 9 7.53 W)\n' + 'Request for a Mission Execution?\n')

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
                
                if Sender == 'Chan':
                    
                    Data += 'Chan Attempted to Connect. Sent packet, Syn Bit - 1, Step 2 of the Handshake.\n\n'
                    Base.LogWrite(Jan_Chan_Log, 'a', Data)
                
                elif Sender == 'Ann':
                    
                    Data += 'Ann Attempted to Connect. Sent packet, Syn Bit - 1, Step 2 of the Handshake.\n\n'
                    Base.LogWrite(Jan_Ann_Log, 'a', Data)                      

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

                if Sender == 'Chan':
                    
                    try:
                        Packet_Dat = Jan_Chan_Data.pop(0)
                    except IndexError:
                        print('Jan-Chan.txt is empty.\n\n')

                elif Sender == 'Ann':
                    
                    try:
                        Packet_Dat = Jan_Ann_Data.pop(0)
                    except IndexError:
                        print('Jan-Ann.txt is empty.\n\n')

                Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

                Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

                TimeStamp = time.time()
                Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                
                if Sender == 'Chan':
                    
                    Data += 'Connection with Chan Successful. Step 3 of the Handshake. Following Data Sent.\n'
                    Data += Packet_Dat + '\n\n'
                    Base.LogWrite(Jan_Chan_Log, 'a', Data)
                
                elif Sender == 'Ann':
                    
                    Data += 'Connection with Ann Successful. Step 3 of the Handshake. Following Data Sent.\n'
                    Data += Packet_Dat + '\n\n'
                    Base.LogWrite(Jan_Ann_Log, 'a', Data)

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

                if Sender == 'Chan':
                    
                    try:
                        Packet_Dat = Jan_Chan_Data.pop(0)
                    except IndexError:
                        pass

                elif Sender == 'Ann':
                    
                    try:
                        Packet_Dat = Jan_Ann_Data.pop(0)
                    except IndexError:
                        pass

                Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

                Base.SerializeAndSendPacket(Response_Packet, Resp_Port)

                Timestamp = time.time()
                Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                Data += 'Received the Following Line - \n'
                Data += Packet_Rx_Decode.get('Data')
                Data += 'Acknowledgement sent along with the Line\n'
                Data += Packet_Dat + '\n\n'

                if Sender == 'Chan':
                    Base.LogWrite(Jan_Chan_Log, 'a', Data)
                elif Sender == 'Ann':
                    Base.LogWrite(Jan_Ann_Log, 'a', Data)

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
        print('Problem creating Server for Jan.')
    
    sys.exit()

if __name__ == '__main__':
    
    try:

        Exit.clear()                    

        Jan_Server = threading.Thread(target = AgentServer, args = ())

        Jan_Server.start()

        time.sleep(10)
    except:
        print ("Couldn't create Thread for Jan's Router.")

    try:
        Src_ID = Listen_Port
        Dest_ID = Base.Mapping.get('Ann')
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
        Data += "Connection with Ann started. Step 1 of the Handshake.\n\n"
        Base.LogWrite(Jan_Ann_Log, 'a', Data)

        while not Exit.isSet():
            pass

        Jan_Server.join()
                
        sys.exit()
    except KeyboardInterrupt:
        Exit.set()

        Jan_Server.join()
                
        sys.exit()
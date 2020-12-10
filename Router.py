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

Layout_Graph = { 'A': {'B': 4, 'C': 3, 'E': 7}, 'B': {'A': 4, 'C': 6, 'L': 5}, 'C': {'A': 3, 'B': 6, 'D': 11}, 'D': {'C': 11, 'L': 9, 'F': 6, 'G': 10}, 'E': {'A': 7, 'G': 5}, 'F': {'L': 5, 'D': 6}, 'G': {'E': 5, 'D': 10}, 'L': {'B': 5, 'D': 9, 'F': 5} }

AirForce_Jan_Log = './Files/AirForceJanLogFile.txt'

#Shortest Paths
Ann_Jan = Base.Dijkstra_Algo(Layout_Graph,'F','A', Visited = [], Dist = {}, Pred = {})
Ann_Jan.insert(0,'Ann')
Ann_Jan.append('Jan')
Jan_Ann = Ann_Jan[::-1]
print("Shortest Paths b/w Ann & Jan - ")
print("Ann -> Jan : " + str(Ann_Jan))
print("Jan -> Ann : " + str(Jan_Ann) + "\n\n")

Jan_Chan = Base.Dijkstra_Algo(Layout_Graph,'E','F', Visited = [], Dist = {}, Pred = {})
Jan_Chan.insert(0,'Jan')
Jan_Chan.append('Chan')
Chan_Jan = Jan_Chan[::-1]
print("Shortest Paths b/w Jan & Chan - ")
print("Jan -> Chan : "+ str(Jan_Chan))
print("Chan -> Jan : "+ str(Chan_Jan)+ "\n\n")

Ann_Chan = Base.Dijkstra_Algo(Layout_Graph,'E','A', Visited = [], Dist = {}, Pred = {})
Ann_Chan.insert(0, 'Ann')
Ann_Chan.append('Chan')
Chan_Ann = Ann_Chan[::-1]
print("Shortest Paths b/w Ann & Chan - ")
print("Ann -> Chan : " + str(Ann_Chan))
print("Chan -> Ann : " + str(Chan_Ann)+ "\n\n")

localHost = Base.localHost

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    """Handle requests in a separate thread."""

def TCPHandler(routerName):
    class RequestHandler(BaseRequestHandler):
        
        def handle(self):

            Pack_Tx = self.request.recv(4096)
            Packet = pickle.loads(Pack_Tx)
            print(routerName + '\n' + str(Packet) + '\n')
            
            Src_ID = Packet.get('Source ID')
            Dest_ID = Packet.get('Destination ID')

            if Src_ID == Base.Mapping.get('Ann') and Dest_ID == Base.Mapping.get('Jan'):
                
                Base.PassPacket(Ann_Jan, routerName, Pack_Tx)

            elif Src_ID == Base.Mapping.get('Jan') and Dest_ID == Base.Mapping.get('H'):
                
                Src_ID = Base.Mapping.get('H')
                Dest_ID = Base.Mapping.get('Jan')
                Seq_Num = random.randint(10000, 99999)
                Ack_Num = Packet.get('Sequence Number') + len(Packet.get('Data'))    
                Packet_Dat = 'Success!'
                Priority_Pointer = 0
                Syn_Bit = 0
                Fin_Bit = 0
                Reset_Bit = 0
                Terminate_Bit = 0

                Response_Packet = Base.NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Packet_Dat, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit)

                Base.SerializeAndSendPacket(Response_Packet, Dest_ID)

                Timestamp = time.time()
                Data = datetime.datetime.fromtimestamp(Timestamp).strftime('%Y-%m-%d %H:%M:%S') + '\n'
                Data += 'Received the Following Line - \n'
                Data += Packet.get('Data')
                Data += 'Acknowledgement sent along with the Line\n'
                Data += Packet_Dat + '\n\n'
                Base.LogWrite(AirForce_Jan_Log, 'w', Data)

                print('Airforce -> Jan: Success!')
            
            # Jan -> Ann
            elif Src_ID == Base.Mapping.get('Jan') and Dest_ID == Base.Mapping.get('Ann'):    
                
                Base.PassPacket(Jan_Ann, routerName, Pack_Tx)
            
            # Jan -> Chan
            elif Src_ID == Base.Mapping.get('Jan') and Dest_ID == Base.Mapping.get('Chan'):    
                
                Base.PassPacket(Jan_Chan, routerName, Pack_Tx)

            # Packet is from Chan to Jan
            elif Src_ID == Base.Mapping.get('Chan') and Dest_ID == Base.Mapping.get('Jan'):    
                
                Base.PassPacket(Chan_Jan, routerName, Pack_Tx)

            # Packet is from Ann to Chan
            elif Src_ID == Base.Mapping.get('Ann') and Dest_ID == Base.Mapping.get('Chan'):    
                
                Base.PassPacket(Ann_Chan, routerName, Pack_Tx)
            
            # Packet is from Jan to Ann
            elif Src_ID == Base.Mapping.get('Chan') and Dest_ID == Base.Mapping.get('Ann'):    
                
                Base.PassPacket(Chan_Ann, routerName, Pack_Tx)

            else:
                
                print('Graph Error!' + '\n\n')

            return

    return RequestHandler

def ThreadRouter (exitEvent, routerName):
    
    try:
        RequestHandler = TCPHandler(routerName)
        Server = ThreadedTCPServer((localHost, Base.Mapping.get(routerName)), RequestHandler)
       
        Server.timeout = 0.01
        Server.daemon_threads = True

        while not Exit.isSet():
            Server.handle_request()     

        Server.server_close()         
    except:
        print('Unable to Create Router' + routerName + '.')
    
    sys.exit()


if __name__ == '__main__':
    
    try:
        Exit = threading.Event()
        Exit.clear()

        A = threading.Thread(target = ThreadRouter, args = (Exit, 'A'))
        B = threading.Thread(target = ThreadRouter, args = (Exit, 'B'))
        C = threading.Thread(target = ThreadRouter, args = (Exit, 'C'))
        D = threading.Thread(target = ThreadRouter, args = (Exit, 'D'))
        E = threading.Thread(target = ThreadRouter, args = (Exit, 'E'))
        F = threading.Thread(target = ThreadRouter, args = (Exit, 'F'))
        G = threading.Thread(target = ThreadRouter, args = (Exit, 'G'))
        L = threading.Thread(target = ThreadRouter, args = (Exit, 'L'))
        H = threading.Thread(target = ThreadRouter, args = (Exit, 'H'))

        A.start()
        B.start()
        C.start()
        D.start()
        E.start()
        F.start()
        G.start()
        L.start()
        H.start()
    except:
        print ("Error: Unable to Start Routers.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        Exit.set()

        A.join()
        B.join()
        C.join()
        D.join()
        E.join()
        F.join()
        G.join()
        L.join() 
        H.join()
                
        sys.exit()
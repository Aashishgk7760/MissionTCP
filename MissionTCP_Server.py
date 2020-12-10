#Nikhil Kamichetty (1001679614)
#Aashish Geeshpathy Krishnamurthy (1001715288)

import sys
import time
import socket
import pickle
import random
import datetime
import threading

from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler

Mapping = { 'A': 4010, 'B': 4020, 'C': 4030, 'D': 4040, 'E': 4050, 'F': 4060, 'G': 4070, 'L': 4080, 'H': 4090, 'Ann': 2010, 'Jan': 2020, 'Chan': 2030 }

localHost = "127.0.0.1"

def Dijkstra_Algo(Layout_Graph, Src, Dest, Visited = [], Dist = {}, Pred = {}):
    
    if Src == Dest:
        
        Path = []
        Temp_Pred = Dest
        
        while Temp_Pred != None:
            Path.append(Temp_Pred)
            Temp_Pred = Pred.get(Temp_Pred, None)
        
        return Path
    
    else :     
        
        if not Visited: 
            Dist[Src] = 0

        for Neighbor in Layout_Graph[Src] :
            
            if Neighbor not in Visited:

                Updated_Dist = Dist[Src] + Layout_Graph[Src][Neighbor]
                if Updated_Dist < Dist.get(Neighbor, float('inf')):
                    Dist[Neighbor] = Updated_Dist
                    Pred[Neighbor] = Src
        
        Visited.append(Src)

        Not_Visited = {}
        for N in Layout_Graph:
            if N not in Visited:
                Not_Visited[N] = Dist.get(N, float('inf'))        
        
        Temp = min(Not_Visited, key = Not_Visited.get)
        Path = Dijkstra_Algo(Layout_Graph, Temp, Dest, Visited, Dist, Pred)
        return Path

def NewTCPPacket(Src_ID, Dest_ID, Ack_Num, Seq_Num, Data, Priority_Pointer, Syn_Bit, Fin_Bit, Reset_Bit, Terminate_Bit):
    
    Packet = {}
    
    CSum = CheckSum(Data)

    Header_Len = len(str(Src_ID)) + len(str(Dest_ID)) + len(str(Ack_Num)) + len(str(Seq_Num)) + len(str(Priority_Pointer)) + len(str(Syn_Bit)) + len(str(Fin_Bit)) + len(str(Reset_Bit)) + len(str(Terminate_Bit))
                   
    Packet.update({'Source ID': Src_ID})
    Packet.update({'Destination ID': Dest_ID})
    Packet.update({'Sequence Number': Seq_Num})
    Packet.update({'Acknowledgement Number': Ack_Num})
    Packet.update({'Data': Data})
    Packet.update({'CheckSum': CheckSum})
    Packet.update({'Urgent Pointer': Priority_Pointer})
    Packet.update({'Syn Bit': Syn_Bit})
    Packet.update({'Fin Bit': Fin_Bit})
    Packet.update({'Rst Bit': Reset_Bit})
    Packet.update({'Ter Bit': Terminate_Bit})
    Packet.update({'Header Length': Header_Len})

    return Packet

def SerializeAndSendPacket(Response_Packet, Resp_Port):
    Resp_Packet_Encode = pickle.dumps(Response_Packet)
            
    try:
        S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S.connect((localHost, Resp_Port))
        S.sendall(Resp_Packet_Encode)
    finally:
        S.close()

def PassPacket(Shortest_Path, Router_Name, Packet_Tx):

    NextRouter_In = Shortest_Path.index(Router_Name) + 1

    if NextRouter_In < len(Shortest_Path):
        
        NextRouter_Name = Shortest_Path[NextRouter_In]
        NextRouter_Port = Mapping.get(NextRouter_Name)  

        try:
            S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            S.connect((localHost, NextRouter_Port))
            S.sendall(Packet_Tx)
        
        except ConnectionRefusedError:
            print(NextRouter_Name + " is offline.")

        finally:
            S.close()

def CheckSum(Msg):
    
    S = 0
    
    for i in range(0, len(Msg), 2):
        try:
            W = ord(Msg[i]) + (ord(Msg[i+1]) << 8)

        except IndexError:
            W = ord(Msg[i]) + (0 << 8)

        S = CarryOver(S, W)
    return ~S & 0xffff

def CarryOver(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def ReadFile(Path):
    with open(Path, 'r') as File:
        Content = File.readlines()
    
    return Content

if __name__ == '__main__':
    print(ReadFile('./Files/Ann/Ann-Chan.txt'))

def LogWrite(Path, Mode, Data):
    with open(Path, Mode) as File:
        File.write(Data)

def GetKey(Value):
    for Key in Mapping:
        if Mapping.get(Key) == Value:
            return Key
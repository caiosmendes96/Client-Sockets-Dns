#!/usr/bin/env python3

import argparse
import socket
import struct
import sys
import random

mapClass = {
    1: 'IN',   
    2: 'CS',   
    3: 'CH',   
    4: 'HS',    
    255: 'ANY'  
}
def buildDnsQuery(qname, qtype):
 
    transactionId = random.randint(0, 65535) 
    flags = 0x0100  
    qdcount = 1  
    ancount = 0  
    nscount = 0  
    arcount = 0  

    header = struct.pack('!HHHHHH', transactionId, flags, qdcount, ancount, nscount, arcount)

    qnameParts = qname.split('.')
    qnameEncoded = b''.join(len(part).to_bytes(1, 'big') + part.encode() for part in qnameParts) + b'\x00'

    qtypeMap = {'A': 1, 'AAAA': 28}
    qtypeValue = qtypeMap[qtype]
    qclass = 1 

    question = qnameEncoded + struct.pack('!HH', qtypeValue, qclass)

    return header + question, transactionId


def parseDnsResponse(response, expected_tid):
    transactionId, flags, qdcount, ancount, nscount, arcount = struct.unpack('!HHHHHH', response[:12])
    if transactionId != expected_tid:
        print("Erro: ID da transação não corresponde.")
        return

    print(f"Message ID: {transactionId}")
    print(f"Counts: Query {qdcount}, Answers {ancount}, Authority {nscount}, Additional {arcount}")
    offset = 12


    for i in range(qdcount):
        qname = []
        while response[offset] != 0:
            length = response[offset]
            offset += 1
            qname.append(response[offset:offset + length].decode())
            offset += length
        offset += 1  
        qtype, qclass = struct.unpack('!HH', response[offset:offset + 4])
        offset += 4
        print(f"Question {i + 1}:")
        print(f"    Name: {'.'.join(qname)}")
        print(f"    Type: {qtype}")
        print(f"    Class: {mapClass.get(qclass)}")


    for i in range(ancount):
        name = response[offset:offset + 2]
        nameResponseHex = ' '.join(f'0x{b:02x}' for b in name)
        offset += 2
        responseType, responseClass, responseTtl, rdlength = struct.unpack('!HHIH', response[offset:offset + 10])
        responseClass = mapClass.get(responseClass); 
        offset += 10
        rdata = response[offset:offset + rdlength]
        offset += rdlength

        print(f"Answer {i + 1}:")
        print(f"    Name: {nameResponseHex}")
        print(f"    Type: {responseType}, Class: {responseClass}, TTL: {responseTtl}")
        print(f"    RDLength: {rdlength} bytes")
        if responseType == 1:  
            ip = ".".join(map(str, rdata))
            print(f"    Addr: {ip} (IPv4)")
        elif responseType == 28:  
            ip = ":".join(format(int.from_bytes(rdata[i:i + 2], 'big'), 'x') for i in range(0, 16, 2))
            print(f"    Addr: {ip} (IPv6)")
        else:
            print(f"    Addr: Addr format not IPv4 or IPv6")

def main():
    parser = argparse.ArgumentParser(description='DNS Client via UDP')
    parser.add_argument('--type', required=True, dest='qtype',
                        help='Query Type (A or AAAA)')
    parser.add_argument('--name', required=True, dest='qname',
                        help='Query Name')
    parser.add_argument('--server', required=True, dest='serverIp',
                        help='DNS Server IP')

    args = parser.parse_args()
    qtype = args.qtype.upper()
    qname = args.qname
    serverIp = args.serverIp
    port = 53

    if qtype not in {"A", "AAAA"}:
        print("Erro: Query Type deve ser 'A' (IPv4) ou 'AAAA' (IPv6)")
        sys.exit(1)


    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(5)

            query, transaction_id = buildDnsQuery(qname, qtype)

            sock.sendto(query, (serverIp, port))

            response, _ = sock.recvfrom(512)  
            
            print("Server response")
            print("-----------------")
            parseDnsResponse(response, transaction_id)

    except socket.timeout:
        print("Erro: Tempo limite excedido ao aguardar resposta do servidor DNS.")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    sys.exit(main())

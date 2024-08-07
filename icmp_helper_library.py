import socket
import struct
import time

class IcmpHelperLibrary:
    def __init__(self):
        self.icmp_socket = None

    def checksum(self, data):
        if len(data) % 2:
            data += b'\0'
        s = sum(struct.unpack('!%dH' % (len(data) // 2), data))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        return ~s & 0xffff

    def build_icmp_packet(self, packet_id, packet_seq):
        header = struct.pack('bbHHh', 8, 0, 0, packet_id, packet_seq)
        checksum = self.checksum(header)
        header = struct.pack('bbHHh', 8, 0, checksum, packet_id, packet_seq)
        return header

    def _sendIcmpEchoRequest(self, host):
        print("sendIcmpEchoRequest Started...")
        try:
            self.icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            print("ICMP socket created.")
        except socket.error as e:
            print(f"Socket error: {e}")
            return

        packet_id = 1  # Use a fixed ID for simplicity
        for i in range(4):
            packet = self.build_icmp_packet(packet_id, i)
            self.icmp_socket.sendto(packet, (host, 0))
            print(f"Sent packet {i} to {host}")
            start_time = time.time()
            try:
                self.icmp_socket.settimeout(1)  # 1 second timeout
                response, _ = self.icmp_socket.recvfrom(1024)
                end_time = time.time()
                rtt = (end_time - start_time) * 1000

                print(f"Received response in {rtt:.2f} ms")
            except socket.timeout:
                print("Request timed out")

        self.icmp_socket.close()
        print("sendIcmpEchoRequest Completed.")

    def traceRoute(self, host):
        print("Starting traceroute...")
        self._sendIcmpTraceRoute(host)

    def _sendIcmpTraceRoute(self, host):
        print("sendIcmpTraceRoute Started...")
        try:
            self.icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            print("ICMP socket created for traceroute.")
        except socket.error as e:
            print(f"Socket error: {e}")
            return

        max_ttl = 30  # Maximum number of hops
        for ttl in range(1, max_ttl + 1):
            self.icmp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            print(f"TTL={ttl}")

            packet_id = ttl  # Use TTL as packet ID
            packet_seq = ttl  # Use TTL as sequence number for simplicity
            packet = self.build_icmp_packet(packet_id, packet_seq)
            self.icmp_socket.sendto(packet, (host, 0))
            print(f"Sent packet with TTL={ttl}")

            try:
                self.icmp_socket.settimeout(2)  # 2 seconds timeout for receiving
                response, addr = self.icmp_socket.recvfrom(1024)
                print(f"Received response from {addr[0]}")
                if addr[0] == host:
                    print(f"Traceroute completed. Reached destination {host}")
                    break
            except socket.timeout:
                print("Request timed out")

        self.icmp_socket.close()
        print("sendIcmpTraceRoute Completed.")

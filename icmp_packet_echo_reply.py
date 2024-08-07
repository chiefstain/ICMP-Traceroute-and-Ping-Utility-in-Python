import struct

class IcmpPacket_EchoReply:
    def __init__(self, packet_data):
        self.packet_data = packet_data
        self.is_valid = False
        self.icmp_identifier = None
        self.icmp_sequence = None
        self.parse_packet()

    def parse_packet(self):
        header = self.packet_data[20:28]  # ICMP header is 20 bytes into IP header
        type, code, checksum, identifier, sequence = struct.unpack('bbHHh', header)
        self.icmp_identifier = identifier
        self.icmp_sequence = sequence

        # Simple validation (extend as needed)
        self.is_valid = (type == 0)  # Echo Reply

    def getIcmpIdentifier(self):
        return self.icmp_identifier

    def getIcmpSequence(self):
        return self.icmp_sequence

    def isValid(self):
        return self.is_valid

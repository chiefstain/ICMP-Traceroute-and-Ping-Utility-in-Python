class IcmpPacket_EchoReply:
    def __init__(self, data):
        self.data = data
        self.valid_data = False
        self.icmp_identifier = None
        self.icmp_identifier_is_valid = False

    def validate_with_original_ping_data(self, original_ping_data):
        # Validate that received packet matches the sent packet
        if (self.data['sequence_number'] == original_ping_data['sequence_number'] and
                self.data['identifier'] == original_ping_data['identifier']):
            self.valid_data = True
            self.icmp_identifier_is_valid = True
        else:
            self.valid_data = False
            self.icmp_identifier_is_valid = False

    def get_icmp_identifier_is_valid(self):
        return self.icmp_identifier_is_valid

    def set_icmp_identifier_is_valid(self, value):
        self.icmp_identifier_is_valid = value

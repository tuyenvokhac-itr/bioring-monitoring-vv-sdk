from fastcrc import crc32

def cy_checksum_packet(packet_buffer, data_len):
    PACKET_DATA_IDX = 0x04
    sum = 0
    size = data_len + PACKET_DATA_IDX  # 4 bytes before data in Cypress DFU packet

    while size > 0:
        size = size - 1
        sum = sum + packet_buffer[size]

    return ((1 + ~sum) & 0xFFFF)

def cy_checksum_data(data):
    return crc32.iscsi(data)
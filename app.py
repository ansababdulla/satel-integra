import socket as socket
from satel_integra.satel_integra import verify_and_strip, output_bytes, AsyncSatel
import asyncio



#method to convert byte array to hex
def convertResponseToHex(data):
    hex_msg = ""
    for c in data:
        hex_msg += "\\x" + format(c, "02x")
        # print(c, format(c, "02x"), hex_msg)
    return hex_msg

##We are calculating the checksum as per satel manual
def checksum(command):
    crc = 0x147A
    for b in command:
        # rotate (crc 1 bit left)
        crc = ((crc << 1) & 0xFFFF) | (crc & 0x8000) >> 15
        crc = crc ^ 0xFFFF
        crc = (crc + (crc >> 8) + b) & 0xFFFF
    return crc

#Here query is generating by adding the header as 0xFE, 0xFE, then append the command
#checksum and footer as 0xFE, 0x0D
def generate_query(command):
    """Add header, checksum and footer to command data."""
    data = bytearray(command)
    c = checksum(data)
    data.append(c >> 8)
    data.append(c & 0xFF)
    ##If any 0xFE byte is send as command, as per the manual we are adding 0xFE and 0xF0
    data.replace(b'\xFE', b'\xFE\xF0')
    data = bytearray.fromhex("FEFE") + data + bytearray.fromhex("FE0D")
    return data

def verify_and_strip(resp):
    """Verify checksum and strip header and footer of received frame."""
    if resp[0:2] != b'\xFE\xFE':
        print("Houston, we got problem:")
        # print(convertResponseToHex(resp))
        raise Exception("Wrong header - got %X%X" % (resp[0], resp[1]))
    if resp[-2:] != b'\xFE\x0D':
        raise Exception("Wrong footer - got %X%X" % (resp[-2], resp[-1]))
    output = resp[2:-2].replace(b'\xFE\xF0', b'\xFE')

    c = checksum(bytearray(output[0:-2]))

    if (256 * output[-2:-1][0] + output[-1:][0]) != c:
        raise Exception("Wrong checksum - got %d expected %d" % (
            (256 * output[-2:-1][0] + output[-1:][0]), c))

    return output[0:-2]

# def checkReturnCommand(responseCommand):
#     if responseCommand == "":

    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect()
#0xFE, 0xFE,command, data1,data2,....,checksum,0xFE, 0x0D is the frame structure, first two frames and last 
#frames are headers and footers.
# command1 = generate_query([0x00])
# command2 = bytearray([0xFE,0xFE,0x00,0xD7,0xE2,0xFE,0x0D])
# response = s.recv(1024)
# s.send(response)

async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(())
    server.listen(8)
    server.setblocking(False)

    loop = asyncio.get_event_loop()


# loop = asyncio.get_event_loop()
# satel = AsyncSatel("",
#                 7090,
#                 loop)
# loop.run_until_complete(satel.connect())
# loop.create_task(satel.arm("80", (1,)))
# loop.create_task(satel.disarm("84", (1,)))
# loop.create_task(satel.keep_alive())
# loop.create_task(satel.monitor_status())
# loop.run_forever()
# loop.close()





# response = b'\xf7\xb3&\xa2\xb0\xd9!):"!\x15vIm\xc6'
# responseHex = convertResponseToHex(bytearray(response))
# print(responseHex)
# commandFromtheResponse = verify_and_strip(command)
# print(convertResponseToHex(command))
# print(command1, command2)
# print(response)











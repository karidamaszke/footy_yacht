import socket

MOVE = {
    "RUDDER_UP": 1,
    "RUDDER_DOWN": 2,
    "SAIL_UP": 3,
    "SAIL_DOWN": 4,
    "END": 5
}

SERVER_PORT = 5555


class Client:
    def __init__(self, ip):
        self.address = (ip, SERVER_PORT)
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def send_order(self, order):
        try:
            if order == "RUDDER_UP":
                self.socket.sendto(int.to_bytes(MOVE["RUDDER_UP"], byteorder='little', length=1), self.address)
            elif order == "RUDDER_DOWN":
                self.socket.sendto(int.to_bytes(MOVE["RUDDER_DOWN"], byteorder='little', length=1), self.address)

            elif order == "SAIL_UP":
                self.socket.sendto(int.to_bytes(MOVE["SAIL_UP"], byteorder='little', length=1), self.address)
            elif order == "SAIL_DOWN":
                self.socket.sendto(int.to_bytes(MOVE["SAIL_DOWN"], byteorder='little', length=1), self.address)

            elif order == "END":
                self.socket.sendto(int.to_bytes(MOVE["END"], byteorder='little', length=1), self.address)
                self.socket.close()

        except socket.error as err:
            raise socket.error(err)

import socket


class TcpFileSenderClient:
    def __init__(self):
        self.host = 'localhost'
        self.port = 7777

    def sendFile(self, fname):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        data_transferred = 0
        try:
            sock.connect((self.host, self.port))
            with open(fname, 'rb') as f:
                try:
                    data = f.read(1024)  # 파일을 1024바이트 읽음
                    while data:  # 파일이 빈 문자열일때까지 반복
                        data_transferred += sock.send(data)
                        data = f.read(1024)
                except Exception as e:
                    print(e)

        finally:
            sock.close()


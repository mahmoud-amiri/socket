import socket
import json
import signal
import sys
from math import ceil

CHUNK_SIZE = 4096
class Server:
    def __init__(self, port):
        self.host = socket.gethostname()
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.client_socket = None
        print(f"Server initialized and listening on port {self.port}")

        # Handle signals for graceful shutdown
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def handle_signal(self, sig, frame):
        self.stop()
        print(f"Server stopped by signal {sig}")
        sys.exit(0)

    def start(self):
        try:
            print("Waiting for a connection...")
            self.client_socket, addr = self.server_socket.accept()
            print(f"Got a connection from {addr}")
            if self.handshake():
                print("Handshake successful, connection is OK")
                #self.communicate()
            else:
                print("Handshake failed")
        except Exception as e:
            print(f"An error occurred: {e}")
        # finally:
        #     self.stop()

    def handshake(self):
        try:
            data = self.client_socket.recv(CHUNK_SIZE).decode('utf-8')
            if data == "HELLO SERVER":
                self.client_socket.send("HELLO CLIENT".encode('utf-8'))
                data = self.client_socket.recv(CHUNK_SIZE).decode('utf-8')
                if data == "OK":
                    return True
            return False
        except Exception as e:
            print(f"An error occurred during handshake: {e}")
            return False

    def communicate(self):
        try:
            while True:
                data = self.receive_data()
                if data:
                    print(f"Received JSON from client: {data}")
                    response = {"message": "Data received", "received_data": data}
                    self.send_data(response)
        except Exception as e:
            print(f"An error occurred during communication: {e}")
        finally:
            self.stop()

    def send_data(self, data):
        try:
            serialized_data = json.dumps(data) + '\n'
            self.client_socket.send(serialized_data.encode('utf-8'))
        except Exception as e:
            print(f"An error occurred while sending data: {e}")
            self.stop()

    def receive_data(self):
        try:
            data = self.client_socket.recv(CHUNK_SIZE).decode('utf-8')
            print(f"receive_data = {data}")
            return json.loads(data)
        except Exception as e:
            print(f"An error occurred while receiving data: {e}")
            self.stop()
            return None

    def stop(self):
        if self.client_socket:
            self.client_socket.close()
        self.server_socket.close()
        print("Server has stopped")
        sys.exit()

    def send_large_data(self, data):
        serialized_data = json.dumps(data)
        print(f"len(serialized_data) = {len(serialized_data)}")
        num_chunks = ceil(len(serialized_data) / CHUNK_SIZE)
        print(f"num_chunks = {num_chunks}")
        for i in range(num_chunks):
            chunk = serialized_data[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE]
            self.send_data({"chunk": chunk, "index": i, "total": num_chunks})
            print(f"chunk number {i} is sent")
            data = self.receive_data()
            print(f"server answered : {data}")


    def receive_large_data(self, max_attempts=100000):
        partial_data = ""
        attempts = 0

        while attempts < max_attempts:
            print(f"attempts = {attempts}")
            chunk = self.receive_data()
            if chunk:
                chunk_data = chunk.get("chunk", "")
                index = chunk.get("index", 0)
                total = chunk.get("total", 0)
                self.send_data({"data": f" chunk {index}/{total-1} received successfully"}) 
                print(f"index = {index} / total = {total-1}")
                partial_data += chunk_data

                if index + 1 == total:
                    print("Last chunk received")
                    # Last chunk received
                    try:
                        return json.loads(partial_data)
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse complete data: {e}")
                        return None
            attempts += 1

        raise TimeoutError("Failed to receive all chunks within the maximum number of attempts")

if __name__ == "__main__":
    port = int(input("Enter the port for the server: "))
    server = Server(port)
    try:
        server.start()
        server.communicate()
    except KeyboardInterrupt:
        server.stop()
        print("Server stopped by user")

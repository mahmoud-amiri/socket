import socket
import json
import sys
from math import ceil

CHUNK_SIZE = 4096
class Client:
    def __init__(self, port):
        self.host = socket.gethostname()
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Client initialized to connect to port {self.port}")

    def start(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server on port {self.port}")
            if self.handshake():
                print("Handshake successful, connection is OK")
                return True
            else:
                print("Handshake failed")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def handshake(self):
        try:
            self.client_socket.send("HELLO SERVER".encode('utf-8'))
            data = self.client_socket.recv(CHUNK_SIZE).decode('utf-8')
            print(f"returned data = {data}")
            if data == "HELLO CLIENT":
                self.client_socket.send("OK".encode('utf-8'))    
                return True
        except Exception as e:
            print(f"An error occurred during handshake: {e}")
            return False

    def communicate(self):
        try:
            while True:
                message = input("Enter JSON data to send to server (or type 'exit' to quit): ")
                if message.lower() == 'exit':
                    break
                try:
                    json_data = json.loads(message)  # Parse input to ensure it's valid JSON
                    self.send_data(json_data)
                    response = self.receive_data()
                    if response:
                        print(f"Received from server: {response}")
                except json.JSONDecodeError:
                    print("Invalid JSON format. Please try again.")
        except Exception as e:
            print(f"An error occurred during communication: {e}")

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
            return json.loads(data)
        except Exception as e:
            print(f"An error occurred while receiving data: {e}")
            self.stop()
            return None

    def stop(self):
        self.client_socket.close()
        print("Client has stopped")
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
    port = int(input("Enter the port for the client: "))
    client = Client(port)
    try:
        client.start()
        client.communicate()
    except KeyboardInterrupt:
        client.stop()
        print("Client stopped by user")

import socket
import json

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
                self.communicate()
            else:
                print("Handshake failed")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.stop()

    def handshake(self):
        try:
            self.client_socket.send("HELLO SERVER".encode('utf-8'))
            data = self.client_socket.recv(1024).decode('utf-8')
            return data == "HELLO CLIENT"
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
            serialized_data = json.dumps(data)
            self.client_socket.send(serialized_data.encode('utf-8'))
        except Exception as e:
            print(f"An error occurred while sending data: {e}")

    def receive_data(self):
        try:
            data = self.client_socket.recv(1024).decode('utf-8')
            return json.loads(data)
        except Exception as e:
            print(f"An error occurred while receiving data: {e}")
            return None

    def stop(self):
        self.client_socket.close()
        print("Client has stopped")

if __name__ == "__main__":
    port = int(input("Enter the port for the client: "))
    client = Client(port)
    try:
        client.start()
    except KeyboardInterrupt:
        client.stop()
        print("Client stopped by user")

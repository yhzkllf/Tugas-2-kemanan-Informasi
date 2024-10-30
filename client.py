import socket
from algoritmaDES import decryption, str_to_bin

def chunk_message(message, chunk_size=8):
    return [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]

def client_program():
    host = 'localhost'
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))
    print("Connected to server")

    while True:
        # Receive encrypted message
        encrypted_message = client_socket.recv(1024).decode()
        
        if encrypted_message == 'quit':
            break

        print(f"\nReceived encrypted message: {encrypted_message}")

        # Split encrypted message into chunks and decrypt
        chunks = chunk_message(encrypted_message)
        decrypted_message = ''

        for chunk in chunks:
            # Convert chunk to binary and decrypt
            chunk_binary = str_to_bin(chunk)
            decrypted_chunk = decryption(chunk_binary)
            decrypted_message += decrypted_chunk

        print(f"Decrypted message: {decrypted_message}")

    client_socket.close()

if __name__ == '__main__':
    client_program()

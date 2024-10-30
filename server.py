import socket
from algoritmaDES import encryption, str_to_bin, binary_to_ascii

def chunk_message(message, chunk_size=8):
    return [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]

def server_program():
    host = 'localhost'
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening...")

    conn, address = server_socket.accept()
    print(f"Connection from: {address}")

    while True:
        # Get message from user
        message = input("Enter message to encrypt (or 'quit' to exit): ")
        if message.lower() == 'quit':
            conn.send('quit'.encode())
            break

        # Split message into 8-character chunks and encrypt each chunk
        chunks = chunk_message(message)
        encrypted_message = ''
        
        for chunk in chunks:
            # Encrypt each chunk
            encrypted_chunk = encryption(chunk)
            encrypted_message += encrypted_chunk

        # Send encrypted message
        conn.send(encrypted_message.encode())
        print(f"Encrypted message sent: {encrypted_message}")

    conn.close()
    server_socket.close()

if __name__ == '__main__':
    server_program()

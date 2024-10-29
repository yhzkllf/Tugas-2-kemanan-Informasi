import socket
import threading


key = b'abcdefgh'  
host = 'localhost'
port = 12345


def xor(data, key):
    return bytes([a ^ b for a, b in zip(data, key)])

def encrypt_des(message, key):
    encrypted_message = bytearray()

    while message:
        block = message[:8].ljust(8).encode()  
        encrypted_message.extend(xor(block, key))
        message = message[8:] 
    return bytes(encrypted_message)

def decrypt_des(encrypted_message, key):
    decrypted_message = bytearray()
    for i in range(0, len(encrypted_message), 8):
        block = encrypted_message[i:i+8]
        decrypted_message.extend(xor(block, key))
    return decrypted_message.decode().rstrip()  

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    while True:
        try:
            encrypted_message = conn.recv(1024)
            if not encrypted_message:
                break
            print(f"Encrypted message received: {encrypted_message}")

            decrypted_message = decrypt_des(encrypted_message, key)
            print(f"Decrypted message: {decrypted_message}")
        except Exception as e:
            print(f"Client {addr} encountered an error: {e}")
            break
    conn.close()
    print(f"Connection with {addr} closed.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening for a connection...")
    
    conn, addr = server_socket.accept()
    handle_client(conn, addr)
    server_socket.close()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    while True:
        message = input("Enter a message to send (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        encrypted_message = encrypt_des(message, key)
        print(f"Encrypted message to send: {encrypted_message}")

        client_socket.send(encrypted_message)
        print("Encrypted message sent")

    client_socket.close()

def main():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    start_client()

    server_thread.join()

if __name__ == "__main__":
    main()

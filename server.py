import socket
from algoritmaDES import DES

algoritma = DES()
key = "gasin"
print(f"Key: {key}")
key_bin = algoritma.ascii_to_bin(key)
rkb, rk = algoritma.generate_keys(key_bin)
rkb_rev = rkb[::-1]
rk_rev = rk[::-1]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))
server_socket.listen(5)

print("Server started and waiting for a connection...")
client_socket, addr = server_socket.accept()
print(f"Connection established with {addr}")

try:
    while True:

        msg = client_socket.recv(1024).decode("utf-8")
        if msg.lower() == 'quit':
            print("Client ended the connection.")
            break
        else:
            decrypted_msg = algoritma.bin_to_ascii(algoritma.decrypt(msg, rkb_rev, rk_rev))
            print("B:", decrypted_msg)
        
        # Get and encrypt response message
        res = input("A: ")
        res_bin = algoritma.ascii_to_bin(res)
        encrypted_res = algoritma.encrypt(res_bin, rkb, rk)
        
        # Send the encrypted response
        client_socket.send(encrypted_res.encode("utf-8"))

except (KeyboardInterrupt, EOFError):
    print("\nConnection closed by server.")
finally:
    client_socket.close()
    server_socket.close()
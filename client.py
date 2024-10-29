import socket
from algoritmaDES import DES


algoritma = DES()
key = "gasin"
print(f"Key: {key}")
key_bin = algoritma.ascii_to_bin(key)
rkb, rk = algoritma.generate_keys(key_bin)
rkb_rev = rkb[::-1]
rk_rev = rk[::-1]


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 1234))
print("Connected to the server.")

try:
    while True:
        msg = input("B: ")
        
        msg_bin = algoritma.ascii_to_bin(msg)
        encrypted_msg = algoritma.encrypt(msg_bin, rkb, rk)
        
        client_socket.send(encrypted_msg.encode("utf-8"))
        
        encrypted_res = client_socket.recv(1024).decode("utf-8")
        if encrypted_res.lower() == 'quit':
            print("Server ended the connection.")
            break
        else:
            decrypted_res = algoritma.bin_to_ascii(algoritma.decrypt(encrypted_res, rkb_rev, rk_rev))
            print("A:", decrypted_res)

except (KeyboardInterrupt, EOFError):
    print("\nConnection closed by user.")
finally:
    client_socket.close()
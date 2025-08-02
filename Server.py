import socket
import threading
import HandlingClient

def get_local_ipv4_address():
    try:
        # Get the hostname of the local machine
        hostname = socket.gethostname()
        # Get the IPv4 address corresponding to the hostname
        ipv4_address = socket.gethostbyname(hostname)
        return ipv4_address
    except socket.gaierror as e:
        return f"Could not resolve hostname: {e}"

if __name__ == "__main__":
    ip_address = get_local_ipv4_address()
    print(f"The local IPv4 address is: {ip_address}")

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.25.193', 9812))
server.listen(2)
print("Server waiting for 2 players...")

players = []
while len(players) < 2:
    conn, addr = server.accept()
    print(f"Player connected: {addr}")
    players.append(conn)

threading.Thread(target=HandlingClient.handle_client, args=(players[0], 'X')).start()
threading.Thread(target=HandlingClient.handle_client, args=(players[1], 'O')).start()

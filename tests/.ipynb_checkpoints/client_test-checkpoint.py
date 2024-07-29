"""
    This a test of the server api

    by Dimaunahan, Isiah Jordan (NoobAtem)
"""
import socket
import yaml
import logging

def read_yaml(filepath: str) -> dict:
    with open(filepath, "rb") as yml:
        return yaml.safe_load(yml)

def send_audio(filename: str) -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    config = read_yaml("configs/network_config.yaml")
    try:
        # Connect the socket to the server's port
        client_socket.connect((config['ip'], config['port']))
        print(f"Connected to server at {config['ip']}:{config['port']}")
    
        # Open the file and send its contents
        with open(filename, 'rb') as f:
            while True:
                # Read the file in chunks
                data = f.read(config["chunk"])
                if not data:
                    break
                client_socket.sendall(data)

        # Properly signal the end of the file transfer
        client_socket.shutdown(socket.SHUT_WR)
        print("Audio file sent successfully.")
    
        # Wait for the response from the server
        response = client_socket.recv(config["chunk"])
        print("Response from server:", response.decode())
    
    finally:
        # Clean up the connection
        client_socket.close()

if __name__ == "__main__":
    audio_to_send = 'data/raw/door/door-4.wav'  # Replace with your WAV file path
    send_audio(audio_to_send)

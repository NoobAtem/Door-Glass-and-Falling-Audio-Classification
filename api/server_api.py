"""
    If you want to use the model,
    this is the one that handles
    the model and request

    by Dimaunahan, Isiah Jordan (NoobAtem)
"""
    
"""
    If you want to use the model,
    this is the one that handles
    the model and request

    by Dimaunahan, Isiah Jordan (NoobAtem)
"""
    
import socket
import threading
import logging
from api.utils import read_yaml
import api.model_api as model_api
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api.server_api")

class Server:
    def __init__(self) -> None:
        logger.info("Initializing server class")
        self.config: dict = read_yaml(os.path.join("configs", "network_config.yaml"))
        self.host: str = self.config["ip"]
        self.port: int = int(self.config["port"])
        self.stop_event = threading.Event()  # Event to signal stopping
        self.initialize()

    def initialize(self) -> None:
        self.socket: object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        if not os.path.exists(self.config["destination"]):
            os.mkdir(self.config["destination"])

    def run(self) -> None:
        logger.info("Currently running the server")
        self.socket.listen(self.config["listen"])
        while not self.stop_event.is_set():
            logger.info("Waiting for a connection...")
            conn, addr = self.socket.accept()
            threading.Thread(target=self.handleClient, args=(conn, addr)).start()

    def handleClient(self, conn: object, addr: str) -> None:
        logger.info(f"Connected by {addr}")
        try:
            count: int = len(list(filter(lambda x: x.endswith(".wav"), os.listdir(self.config["destination"]))))
            filename: str = os.path.join(self.config["destination"], f"rec-audio-{count}.wav")
            with open(filename, "wb") as f:
                logger.info("Receiving an audio file")
                while True:
                    data: object = conn.recv(self.config["chunk"])
                    if not data:
                        break
                    f.write(data)
            logger.info("Audio file received successfully.")

            response: str = model_api.fetch_model_api(filename)
            conn.sendall(response.encode())

        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            conn.close()
            logger.info(f"Connection with {addr} closed.")

    def stop(self) -> None:
        logger.info("Stopping server...")
        self.stop_event.set()
        self.socket.close()
        logger.info("Server stopped.")

def entry() -> None:
    logger.info("==== Running a Server ====")
    server: object = Server()
    try:
        server.run()
    except KeyboardInterrupt:
        server.stop()
    logger.info("==== Shutdown Server ====")

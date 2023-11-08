import sys, os
import numpy as np
import socket as sc
import asyncio

from logger import logging
from dotenv import load_dotenv
from pathlib import Path

#указание виртуального окружения
dotenv_path = Path(__file__).parent.absolute() / ".env"
if os.path.exists(dotenv_path): load_dotenv(dotenv_path)

#Указание хоста/порта из .env
HOST = os.getenv('IP')
PORT = int(os.getenv('PORT'))
COUNT_RECV_BYTES = 1024     #число принятых байт
STOP_SIGNAL = 'СТОП' # стоп сигнал


def parse_data(request) -> str:
    """
        Парсишь данные здесь
    """
    logging.info(request)
    request = request.decode('utf-8')
    return str(request).encode('utf-8')
        
        
async def client_handle(connect:object):
    """
        Обрабатываем клиента
    """
    loop = asyncio.get_event_loop()
    request = None
    while request != 'quit':
        request = (await loop.sock_recv(connect, COUNT_RECV_BYTES))
        logging.info('Посылка принята')
        
        response = parse_data(request)
        
        if str(request) == STOP_SIGNAL:
            connect.close()
        
        await loop.sock_sendall(connect, response)
    connect.close()

async def start_server():
    server = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
    server.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    server.setblocking(False)
    loop = asyncio.get_event_loop()
    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(client_handle(connect=client))
        
if __name__ == '__main__':
    logging.info('Сервер запущен')
    asyncio.run(start_server())

    
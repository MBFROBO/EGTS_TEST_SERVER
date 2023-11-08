import sys, os
import numpy as np
import socket as sc
import asyncio, threading

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
STOP_SIGNAL = 'СТОП' #


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
    logging.warning('Новое присоединение')
    request = None
    while True:
        request = (await loop.sock_recv(connect, COUNT_RECV_BYTES))
        
        if request == b'':
            break
        
        logging.info('Посылка принята')
        response = parse_data(request)
        
        if os.environ['SIGNAL'] == '0':
            logging.info('Закрываю соединение')
        
            # await loop.sock_sendall(connect, None)
        else:
            await loop.sock_sendall(connect, response)
    logging.warning('Отключение')
    connect.close()

def console_input():
    while True:
        inp = str(input('Введи сигнал >> '))
        if inp != '0' and inp != '1':
            print('Ввёл не то число, сломаешь!')
        else:
            os.environ['SIGNAL'] = inp
            

async def start_server():
    os.environ['SIGNAL'] = '1'
    
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
    constole_thr = threading.Thread(target=console_input)
    constole_thr.start()
    
    logging.info('Сервер запущен')
    asyncio.run(start_server())
    constole_thr.join()

    
import json
import asyncio
import socket
import re
from urllib.parse import parse_qs
# from Databases import *

from colorlog import ColoredFormatter
import logging

def Logger(name):
    formatter = ColoredFormatter(
    "%(name)s - %(log_color)s%(levelname)s - %(white)s%(asctime)s: %(log_color)s%(message)-10s ",
    datefmt=None,
    reset=True,
    log_colors={
    'DEBUG':    'cyan',
    'INFO':     'white',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'red',
    },
    style='%'
    )
    if name:
        name = name
    else:
        name = "Default"
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    return logger

class Server_one_process:
    def __init__(self, job_queue, output_queue):
        self.task = None
        self.current_functions = ["/add_user", "/small_zombie"]
        self.loop = asyncio.get_event_loop()
        self.job_queue = job_queue
        self.output_queue = output_queue
        self.logger = Logger("Server")
        self.logger.setLevel(logging.DEBUG)
        self.identifier = 0

    async def debug_(self, text):
        self.logger.debug(text)
    async def critical_(self, text):
        self.logger.critical(text)
    async def error(self, text):
        self.logger.error(text)

    async def generate_http_response(self, status_code, message, body=None):
        status_code = status_code
        status_line = f"HTTP/1.1 {status_code} OK Request\r\n"
        headers = "Content-Type: application/json\r\n"
        response_data = {'Message': body}
        response_body = json.dumps(response_data)
        headers += f"Content-Length: {len(response_body)}\r\n"
        response = status_line + headers + "\r\n" + response_body
        await self.debug_("Response Generated.")
        return response

    async def message_sending(self, client_socket, results):
        # 401 data error
        # 403 data buffer, large request over 4000 bytes
        # Deleted for security reasons.
        if isinstance(results, int):
            if results == x:
            try:
                await self.debug_(f"Sending: Bad Request.{results}")
                await self.loop.sock_sendall(client_socket, response.encode())
                client_socket.close()
            except:
                client_socket.close()

        elif isinstance(results, list):
            if signal == 200:
                response_data = {"signal": signal,
                                'Loading_Strategy:': "xpath_found",
                                 "timer" : timer,
                                 'html': html
                                 }
            elif signal == 201:
                response_data = {"signal": signal,
                    'Loading_Strategy': "websocket idle.",
                                 "timer": timer,
                                 'html': html
                                 }
            elif signal == 202:
                response_data = {"signal": signal,
                    'Loading_Strategy': "Connection timer",
                                 "timer": timer,
                                 'html': html
                                 }
            elif signal == 400:
                response_data = {"signal": 400,
                                 'Loading_Strategy': "Error",
                                 "timer": timer,
                                 'html': html
                                 }
            else:
                await self.error(f"not designed signal {signal}\n{html}")
                response_data = {"signal": 400,
                                'Loading_Strategy': "Error",
                                 "timer": timer,
                                 'html': html
                                 }
            response = await self.generate_http_response(signal,"OK", response_data)

            # Handling socket connection closed as not expected
            try:
                await self.debug_("Sending back: List")
                await self.loop.sock_sendall(client_socket, response.encode())
                client_socket.close()
            except:
                client_socket.close()

    async def route_small_zombie(self, approved_message):
        # message = [call_method, route, headers, body]
        body = approved_message[3]
        username = body.get('Username')
        url = body.get("url")
        steps = body.get('Functions')
        proxy_config = body.get('proxy_config')

        if self.identifier == 5000:
            self.identifier = 1
        else:
            self.identifier += 1
        current_identifier = self.identifier
        # quest = [current_identifier, username, url]
        self.job_queue.put(quest)
        while True:
            if not self.output_queue.empty():
                results_list = self.output_queue.get()
                # results_list = [idenfier, [results]]
                if results_list[0] != current_identifier:
                    self.output_queue.put(results_list)
                else:
                    await self.debug_("output receivedm small zombie")
                    return results_list[1]
            else:
                await asyncio.sleep(0.1)

    async def data_control(self, client_socket, data_buffer):
        # Only return delivery or false
        try:
            message = data_buffer.decode()
            header_raw, body = message.split('\r\n\r\n', 1)
            body = json.loads(body)
            headers_raw = header_raw.split('\r\n')
            call_method, route, aaa = headers_raw[0].split(" ")
            headers = headers_raw[1:]
        except json.JSONDecodeError as json_e:
            await self.debug_(f"Error decoding JSON body {json_e}")
            return 401
        except Exception as E:
            await self.debug_(f"Parsing message error {E}")
            return 401

        message = [call_method, route, headers, body]
        # function >>>>
        # Deleted for security reasons.
            route == "/small_zombie":
            results_list = await self.route_small_zombie(message)
            # can be delivery or false
            await self.debug_("message_exam, ouput return")
            return results_list
        else:
            return 404

    async def client_control(self, client_socket, address):
            # results = await checking_if_blocked(address)
            # if results:
            #     await self.false_message_return(client_socket)
            #     return
            data_buffer = b""
            content_length = None
            while True:
                data = await self.loop.sock_recv(client_socket, 2000)
                data_buffer += data
                # await self.debug_(data_buffer.decode())
                if content_length is None:
                    content_length_match = re.search(b'Content-Length: (\d+)', data_buffer)
                    if content_length_match:
                        content_length = int(content_length_match.group(1))
                if content_length is not None and len(data_buffer) >= content_length:
                    break
                # In my imagination this is how to handle a single request, and prevent "unecessary" huge requests' data incoming. 
                # The sokcet will automated closed with a fuck you error when you send over 4000 bytes of data.
                if len(data_buffer) > 4000:
                    await self.error(f"Over 4000 buffer: {data_buffer}")
                    await self.message_sending(client_socket, 403)
                    return
            results = await self.data_control(client_socket, data_buffer)
            # Clean data buffer but i know Python will clean it anyway
            data_buffer = None
            await self.message_sending(client_socket,results)

    async def start_server (self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 3999))
        server_socket.listen(1000)
        server_socket.setblocking(False)
        await self.debug_("Server started.")
        while True:
            client_socket, address = await self.loop.sock_accept(server_socket)
            asyncio.create_task(self.client_control(client_socket, address))


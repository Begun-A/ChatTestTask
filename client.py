#!/usr/bin/env python

from threading import Thread
import argparse

import websocket
import tornado.escape


SERVER_URL = "ws://127.0.0.1:8888/chatsocket"


def format_message(message):
    return '\n{}\n> '.format(message)


def print_message(message):
    print(format_message(message), end='')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('username',
                        help='choose a username (John, Bob or Susan)')
    args = parser.parse_args()

    try:
        ws = websocket.create_connection (SERVER_URL)
    except ConnectionRefusedError:
        print('Failed to connect to server')
        return

    ws.send(tornado.escape.json_encode(
        {'type': 'auth', 'username': args.username}))

    ###################################################################
    def receive():
        while True:
            try:
                message = ws.recv()
            except websocket._exceptions.WebSocketConnectionClosedException:
                print('Connection closed by server (press Enter to exit)')
                return

            print_message(message)

    # Start a receiver thread
    t = Thread(target=receive, daemon=True)
    t.start()
    ###################################################################

    # Prompt user for messages and send them to the server
    message = None
    while 1:
        message = input('> ')

        # Quit message received or server closed the connection and
        # receiver is dead
        if message == 'q' or not t.is_alive():
            ws.close()
            break

        if not message:
            print('Use q to close the client')
            continue

        ws.send(message)
    else:
        ws.close()


if __name__ == "__main__":
    main()

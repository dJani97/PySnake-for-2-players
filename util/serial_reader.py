from threading import Thread
from time import sleep
from typing import Optional, Callable, Any, Iterable, Mapping

import serial
from constants import *

PORT = "COM6"
BAUDRATE = 115200


def get_dir_from_string(serial_string):
    serial_string = serial_string .strip()
    if serial_string == 'RIGHT':
        return Dir.right
    elif serial_string == 'LEFT':
        return Dir.left
    elif serial_string == 'UP':
        return Dir.up
    elif serial_string == 'DOWN':
        return Dir.down


class SerialReader(Thread):
    s = serial.Serial(PORT, baudrate=BAUDRATE)
    player1_last_dir = None
    player2_last_dir = None
    running = True

    def run(self) -> None:
        print("SerialReader run()")
        self.read_loop()

    def player2_get_last_dir(self):
        values = self.s.read_all().split()
        if (len(values)) > 0:
            serial_direction = values[-1].decode("utf-8")
            if serial_direction == 'P1:RIGHT':
                return Dir.right
            elif serial_direction == 'P1:LEFT':
                return Dir.left
            elif serial_direction == 'P1:UP':
                return Dir.up
            elif serial_direction == 'P1:DOWN':
                return Dir.down

    def read_loop(self):
        print("SerialReader read_loop()")
        while self.running:
            try:
                sleep(serial_read_loop_delay)
                print("SerialReader read_loop() looping...")
                command = self.s.readline().decode("utf-8")
                print(command)
                if 'P1' in command:
                    print('P1!!')
                    command = command.split(':')[1]
                    print(command)
                    self.player1_last_dir = get_dir_from_string(command)

                if 'P2' in command:
                    print('P2!!')
                    command = command.split(':')[1]
                    print(command)
                    self.player2_last_dir = get_dir_from_string(command)

            except Exception as ex:
                print(ex)

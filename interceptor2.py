import keyboard
import pyautogui
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import time
from character import MagmaBoy, HydroGirl
import cv2
import numpy as np
from datetime import datetime
import os
import csv

class Interceptor:
    def __init__(self):
        model = Model('vosk-model-small-en-us-0.15')  # Adjust path if needed
        self.recognizer = KaldiRecognizer(model, 16000)
        self.queue = queue.Queue()
        self.latest_text = ''
        self.magma_boy = None
        self.hydro_girl = None
        self.level_queue = queue.Queue()
        self.cv2_window_name = 'Voice Command Display (ESC to quit)'
        self.running = True
        self.used_commands = []
        self.last_command_time = 0
        self.command_cooldown = 0.6  # seconds
        self.width, self.height = 600, 200
        self.update_display()

    def start(self):
        try:
            with sd.RawInputStream(samplerate=16000, blocksize=256, dtype='int16', channels=1, latency=0.02, callback=self.update_queue):
                while self.running:
                    data = self.queue.get()
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        self.latest_text = result.get('text', '').lower()
                        self.handle_command(self.latest_text)
                    else:
                        partial_result = json.loads(self.recognizer.PartialResult())
                        partial_text = partial_result.get('partial', '').lower()
                        self.latest_text = partial_text
                        self.handle_command(partial_text, partial=True)

                    self.update_display()
        except Exception as e:
            print(f'Error occurred: {e}')
            cv2.destroyWindow(self.cv2_window_name)

    def update_queue(self, indata, frames, time_info, status):
        self.queue.put(bytes(indata))

    def update_players(self, magma_boy: MagmaBoy, hydro_girl: HydroGirl):
        self.magma_boy = magma_boy
        self.hydro_girl = hydro_girl

    def handle_command(self, text, partial=False):
        now = time.time()
        if now - self.last_command_time < self.command_cooldown:
            return

        valid_commands = {
            'select': 'enter',
            'begin': 'enter',
            'start': 'enter',
            'enter': 'enter',
            'exit': 'escape',
            'down': 'down',
            'up': 'up',
            'op': 'up',
            'jump': 'jump',
            'boy': 'jump',
            'girl': 'girl',
            'hi': 'girl',
            'high': 'girl',
            'fly': 'girl',
            'flight': 'girl',
            'level one': 1, 'level 1': 1,
            'level two': 2, 'level to': 2, 'level too': 2, 'level 2': 2,
            'level three': 3, 'level tree': 3, 'level 3': 3,
            'level four': 4, 'level for': 4, 'level 4': 4,
            'level five': 5, 'level 5': 5
        }

        if text in valid_commands:
            self.last_command_time = now
            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text))

            cmd = valid_commands[text]

            if cmd == 'enter':
                keyboard.press_and_release('enter')
            elif cmd == 'escape':
                keyboard.press_and_release('escape')
            elif cmd == 'down':
                pyautogui.press('down')
            elif cmd == 'up':
                pyautogui.press('up')
                if self.magma_boy:
                    self.magma_boy.jumping = True
                    time.sleep(0.1)
                    self.magma_boy.jumping = False
            elif cmd == 'jump':
                if self.magma_boy:
                    self.magma_boy.jumping = True
                    time.sleep(0.1)
                    self.magma_boy.jumping = False
            elif cmd == 'girl':
                if self.hydro_girl:
                    self.hydro_girl.jumping = True
                    time.sleep(0.1)
                    self.hydro_girl.jumping = False
            elif isinstance(cmd, int):
                self.level_queue.put(cmd)

    def update_display(self):
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, self.latest_text, (50, 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow(self.cv2_window_name, img)
        if cv2.waitKey(1) & 0xFF == 27:
            cv2.destroyWindow(self.cv2_window_name)
            self.running = False

    def get_queued_level(self):
        if not self.level_queue.empty():
            return self.level_queue.get()
        return None

    def stop(self):
        cv2.destroyWindow(self.cv2_window_name)
        self.running = False

        if len(self.used_commands) > 0:
            os.makedirs("voice_commands", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"voice_commands/commands_{timestamp}.csv"

            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Command"])
                writer.writerows(self.used_commands)

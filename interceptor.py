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
import pygame
from datetime import datetime
import os
import csv

class Interceptor:
    def __init__(self):
        # Initialize the recognizer, queue and model for the class
        # For the model use the model we downloaded from the Vosk website in data folder, or adjust the path accordingly
        # model = Model(model_path)
        # Load the model
        model = Model('vosk-model-small-en-us-0.15')
        self.recognizer = KaldiRecognizer(model, 16000)
        self.queue = queue.Queue()
        self.latest_text = ''
        self.magma_boy = None
        self.hydro_girl = None
        self.level_queue = queue.Queue()
        self.cv2_window_name = 'Voice Command Display (ESC to quit)'
        self.running = True
        self.used_commands = []  # Store recognized commands

        # OpenCV window setup
        self.width, self.height = 600, 200
        self.update_display()

    def start(self):
        # Start the stream to listen to the microphone and process the audio data
        try:
            with sd.RawInputStream(samplerate=16000, blocksize=1000, dtype='int16', channels=1, latency=0.1, callback=self.update_queue):
                while self.running:
                    data = self.queue.get()
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        self.latest_text = result.get('text', '').lower()
                        if self.latest_text == 'select' or self.latest_text == 'begin' or self.latest_text == 'start' or self.latest_text == 'enter':
                            # Append a tuple of time - text for each command
                            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.latest_text))
                            keyboard.press_and_release('enter')
                        elif self.latest_text == 'exit':
                            # Append a tuple of time - text for each command
                            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.latest_text))
                            keyboard.press_and_release('escape')
                        elif self.latest_text == 'down':
                            # Append a tuple of time - text for each command
                            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.latest_text))
                            pyautogui.press('down')
                        elif self.latest_text == 'up':
                            # Append a tuple of time - text for each command
                            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.latest_text))
                            pyautogui.press('up') 
                            if (self.magma_boy):
                                self.magma_boy.jumping = True
                                time.sleep(0.1)
                                self.magma_boy.jumping = False
                        elif self.latest_text == 'boy' or self.latest_text == 'jump' or  self.latest_text == 'up':
                            # Append a tuple of time - text for each command
                            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.latest_text))
                            if (self.magma_boy):
                                self.magma_boy.jumping = True
                                time.sleep(0.1)
                                self.magma_boy.jumping = False
                        elif self.latest_text == 'girl' or self.latest_text == 'hi' or self.latest_text == 'high' or self.latest_text == 'fly' or self.latest_text == 'flight':
                            # Append a tuple of time - text for each command
                            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.latest_text))
                            if (self.hydro_girl):
                                self.hydro_girl.jumping = True
                                time.sleep(0.1)
                                self.hydro_girl.jumping = False
                        elif self.latest_text == 'level one' or self.latest_text == 'level 1':
                            # Append a tuple of time - text for each command
                            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.latest_text))
                            self.level_queue.put(1)
                        elif self.latest_text == 'level two' or self.latest_text == 'level to' or self.latest_text == 'level too' or self.latest_text == 'level 2':
                            # Append a tuple of time - text for each command
                            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.latest_text))
                            self.level_queue.put(2)
                        elif self.latest_text == 'level three' or self.latest_text == 'level tree' or self.latest_text == 'level 3':
                            # Append a tuple of time - text for each command
                            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.latest_text))
                            self.level_queue.put(3)
                        elif self.latest_text == 'level four' or self.latest_text == 'level for' or self.latest_text == 'level 4':
                            # Append a tuple of time - text for each command
                            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.latest_text))
                            self.level_queue.put(4)
                        elif self.latest_text == 'level five' or self.latest_text == 'level 5':
                            # Append a tuple of time - text for each command
                            self.used_commands.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.latest_text))
                            self.level_queue.put(5)
                    self.update_display()
        except Exception as e:
            print(f'Error occurred: {e}')
            cv2.destroyWindow(self.cv2_window_name)

    def update_queue(self, indata, frames, time, status):
        self.queue.put(bytes(indata))

    def update_players(self, magma_boy: MagmaBoy, hydro_girl: HydroGirl):
        self.magma_boy = magma_boy
        self.hydro_girl = hydro_girl

    def update_display(self):
        """Updates the OpenCV window with the latest recognized text."""
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)  # Black background
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, self.latest_text, (50, 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)  # White text
        cv2.imshow(self.cv2_window_name, img)
        # Allow manual closing of OpenCV window
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

        """Save used commands to a uniquely named CSV file."""
        os.makedirs("voice_commands", exist_ok=True)  # Ensure directory exists
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"voice_commands/commands_{timestamp}.csv"

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Command"])  # Header
            writer.writerows(self.used_commands)

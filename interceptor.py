import keyboard
import pyautogui
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import time
from character import MagmaBoy, HydroGirl

class Interceptor:
    def __init__(self):
        # Initialize the recognizer, queue and model for the class
        # For the model use the model we downloaded from the Vosk website in data folder, or adjust the path accordingly
        # model = Model(model_path)
        # Load the model
        model = Model('vosk-model-small-en-us-0.15')
        self.recognizer = KaldiRecognizer(model, 16000)
        self.queue = queue.Queue()

    def start(self):
        # Start the stream to listen to the microphone and process the audio data
        with sd.RawInputStream(samplerate=16000, blocksize=1000, dtype='int16', channels=1, latency=0.1, callback=self.update_queue):
            while True:
                data = self.queue.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '').lower()
                    print(text)
                    if text == 'select' or text == 'begin' or text == 'start' or text == 'enter':
                        print('enter pressed')
                        keyboard.press_and_release('enter')
                    if text == 'exit':
                        print('escape pressed')
                        keyboard.press_and_release('escape')
                    elif text == 'down':
                        print('down pressed')
                        pyautogui.press('down')
                    elif text == 'up': 
                        print('up pressed')
                        pyautogui.press('up') 
                        if (self.magma_boy):
                            self.magma_boy.jumping = True
                            time.sleep(0.1)
                            self.magma_boy.jumping = False
        
                    elif text == 'boy' or text == 'jump' or  text == 'up':
                        print('up pressed')
                        if (self.magma_boy):
                            self.magma_boy.jumping = True
                            time.sleep(0.1)
                            self.magma_boy.jumping = False

                    elif text == 'girl' or text == 'hi' or text == 'high' or text == 'fly' or text == 'flight':
                        print('w pressed')
                        if (self.hydro_girl):
                            self.hydro_girl.jumping = True
                            time.sleep(0.1)
                            self.hydro_girl.jumping = False

    def update_queue(self, indata, frames, time, status):
        self.queue.put(bytes(indata))

    def update_players(self, magma_boy: MagmaBoy, hydro_girl: HydroGirl):
        self.magma_boy = magma_boy
        self.hydro_girl = hydro_girl

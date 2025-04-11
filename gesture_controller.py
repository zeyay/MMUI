import cv2
import mediapipe as mp
import threading
from gesture_visualizer import GestureVisualizer

class GestureController:
    NEUTRAL_LOW = 0.45
    NEUTRAL_HIGH = 0.55

    def __init__(self):
        self.hand1_x = 0.5  # Left player (HydroGirl)
        self.hand2_x = 0.5  # Right player (MagmaBoy)
        self.running = True
        self.visualizer = GestureVisualizer(self.NEUTRAL_LOW, self.NEUTRAL_HIGH)

        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.start()

    def _capture_loop(self):
        self.cap = cv2.VideoCapture(0)
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)
        mp_drawing = mp.solutions.drawing_utils

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            height, width, _ = frame.shape
            mid_x = width // 2

            self.hand1_x = 0.5
            self.hand2_x = 0.5

            if results.multi_hand_landmarks:
                for hand_landmarks, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    x_pixel = int(wrist.x * width)

                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    if x_pixel < mid_x:
                        self.hand1_x = x_pixel / mid_x
                        cv2.circle(frame, (x_pixel, int(wrist.y * height)), 8, (255, 0, 0), -1)
                    else:
                        self.hand2_x = (x_pixel - mid_x) / mid_x
                        cv2.circle(frame, (x_pixel, int(wrist.y * height)), 8, (0, 0, 255), -1)

            # Draw UI and handle display
            frame = self.visualizer.draw_ui(frame, self.hand1_x, self.hand2_x)
            if self.visualizer.show(frame) & 0xFF == 27:  # ESC key
                self.running = False
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def get_controls(self):
        def interpret(x):
            if x < self.NEUTRAL_LOW:
                return False, True  # move right
            elif x > self.NEUTRAL_HIGH:
                return True, False  # move left
            else:
                return False, False  # neutral

        magma_controls = interpret(self.hand2_x)
        hydro_controls = interpret(self.hand1_x)
        return magma_controls, hydro_controls

    def stop(self):
        self.running = False
        if hasattr(self, "cap"):
            self.cap.release()
        self.capture_thread.join(timeout=1)

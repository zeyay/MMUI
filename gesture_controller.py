import cv2
import mediapipe as mp
import threading
from gesture_visualizer import GestureVisualizer

class GestureController:
    def __init__(self):
        self.hand1_x = 0.5  # Left player (HydroGirl)
        self.hand2_x = 0.5  # Right player (MagmaBoy)
        self.hand1_fist = False
        self.hand2_fist = False
        self.running = True
        self.visualizer = GestureVisualizer(0.5, 0.5)

        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.start()

    def is_fist(self, hand_landmarks):
        tips_ids = [4, 8, 12, 16, 20]
        for tip_id in tips_ids[1:]:
            tip = hand_landmarks.landmark[tip_id]
            base = hand_landmarks.landmark[tip_id - 2]
            if tip.y < base.y:
                return False
        return True

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
            height, width, _ = frame.shape
            mid_x = width // 2

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            self.hand1_x = 0.5
            self.hand2_x = 0.5
            self.hand1_fist = False
            self.hand2_fist = False

            if results.multi_hand_landmarks:
                for hand_landmarks, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    x_pixel = int(wrist.x * width)

                    is_fist_gesture = self.is_fist(hand_landmarks)

                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    if x_pixel < mid_x:
                        # Left side (HydroGirl)
                        self.hand1_x = x_pixel / mid_x
                        self.hand1_fist = is_fist_gesture
                        self._draw_hand(frame, x_pixel, int(wrist.y * height), (255, 0, 0), "Hydro", self.hand1_x)
                    else:
                        # Right side (MagmaBoy)
                        self.hand2_x = (x_pixel - mid_x) / mid_x
                        self.hand2_fist = is_fist_gesture
                        self._draw_hand(frame, x_pixel, int(wrist.y * height), (0, 0, 255), "Magma", self.hand2_x)

            # Draw the visual UI elements (left and right split lines, etc.)
            frame = self.visualizer.draw_ui(frame, self.hand1_x, self.hand2_x)

            # Show frame with the UI
            if self.visualizer.show(frame) & 0xFF == 27:
                self.running = False
                break

        self.cap.release()
        cv2.destroyWindow(self.visualizer.cv2_window_name)

    def _draw_hand(self, frame, x_pixel, y_pixel, color, label, hand_x):
        # Draw a circle at the hand position
        cv2.circle(frame, (x_pixel, y_pixel), 12, color, -1)
        
        # Draw the state text
        state_text = "Stop" if (label == "Hydro" and self.hand1_fist) or (label == "Magma" and self.hand2_fist) else "Run"
        cv2.putText(frame, f"{label}: {state_text}", (x_pixel - 40, y_pixel + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Draw the X coordinate for Hydro and Magma
        coord_text = f"X: {hand_x:.2f}"
        cv2.putText(frame, coord_text, (x_pixel - 40, y_pixel + 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def get_controls(self):
        def interpret(x, is_fist):
            if is_fist:
                return False, False  # Stop
            if x < 0.50:
                return False, True  # Move left
            elif x > 0.50:
                return True, False  # Move right
            else:
                return False, False  # Neutral zone

        magma_controls = interpret(self.hand2_x, self.hand2_fist)
        hydro_controls = interpret(self.hand1_x, self.hand1_fist)
        return magma_controls, hydro_controls

    def stop(self):
        self.running = False
        if hasattr(self, "cap"):
            self.cap.release()
        self.capture_thread.join(timeout=1)

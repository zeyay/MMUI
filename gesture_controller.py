import cv2
import threading
import warnings
from ultralytics import YOLO

warnings.filterwarnings("ignore", category=FutureWarning)

class GestureController:
    def __init__(self):
        self.hand1_x = 0.5  # HydroGirl (left)
        self.hand2_x = 0.5  # MagmaBoy (right)
        self.running = True

        # Load the YOLO11 model
        self.model = YOLO("yolo11n.pt")  # Ensure you have the 'yolo11n.pt' model file
        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.start()

    def _capture_loop(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print("❌ Webcam not accessible.")
            return

        while self.running:
            success, img = self.cap.read()
            if not success or not self.running:
                break

            # Resize and optionally flip the image for better speed and alignment
            img = cv2.resize(img, (640, 360))
            img = cv2.flip(img, 1)              # Flip horizontally

            height, width = img.shape[:2]
            mid_x = width // 2

            # Run YOLOv11 detection in stream mode
            results = self.model(img, stream=True, verbose=False)

            left_hand = None
            right_hand = None
            left_dist = float('inf')
            right_dist = float('inf')

            for result in results:
                detections = result.boxes.xyxy.cpu().numpy()

                for box in detections:
                    x_min, y_min, x_max, y_max = box[:4]
                    x_center = (x_min + x_max) / 2

                    # Draw bounding box
                    cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 1)

                    if x_center < mid_x:
                        dist = abs(x_center - (mid_x / 2))
                        if dist < left_dist:
                            left_hand = x_center
                            left_dist = dist
                    else:
                        dist = abs(x_center - (mid_x + (mid_x / 2)))
                        if dist < right_dist:
                            right_hand = x_center
                            right_dist = dist

            # Normalize X for HydroGirl (left)
            if left_hand is not None:
                self.hand1_x = left_hand / mid_x
                cv2.line(img, (int(left_hand), 0), (int(left_hand), height), (255, 0, 0), 2)
            else:
                self.hand1_x = 0.5

            # Normalize X for MagmaBoy (right)
            if right_hand is not None:
                self.hand2_x = (right_hand - mid_x) / mid_x
                cv2.line(img, (int(right_hand), 0), (int(right_hand), height), (0, 0, 255), 2)
            else:
                self.hand2_x = 0.5

            # Draw center split line
            cv2.line(img, (mid_x, 0), (mid_x, height), (128, 128, 128), 1)

            # Show X values
            cv2.putText(img, f"HydroGirl X: {self.hand1_x:.2f}", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
            cv2.putText(img, f"MagmaBoy X: {self.hand2_x:.2f}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

            # Show the window
            cv2.imshow("Gesture Tracking (ESC to quit)", img)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC key to quit
                self.running = False
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def get_controls(self):
        """
        Return control states for both players based on their hand positions.
        Returns:
            (magma_right, magma_left), (hydro_right, hydro_left)
        """
        def interpret(x):
            if x < 0.48:
                return False, True  # move right 
            elif x > 0.52:
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

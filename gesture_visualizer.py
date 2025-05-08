import cv2

class GestureVisualizer:
    def __init__(self, neutral_low, neutral_high):
        self.neutral_low = neutral_low
        self.neutral_high = neutral_high
        self.cv2_window_name = "Gesture Control (ESC for exit)"

    def draw_ui(self, frame, hand1_x, hand2_x):
        height, width, _ = frame.shape
        mid_x = width // 2
        left_split = mid_x // 2
        right_split = mid_x + (mid_x // 2)

        # Draw neutral and center lines for both zones
        cv2.line(frame, (left_split, 0), (left_split, height), (255, 0, 0), 1)  # HydroGirl left line
        cv2.line(frame, (right_split, 0), (right_split, height), (0, 0, 255), 1)  # MagmaBoy right line
        cv2.line(frame, (mid_x, 0), (mid_x, height), (100, 100, 100), 2)  # Center line

        return frame

    def _draw_label(self, frame, label, color, side_split):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, label, (side_split - 40, 25), font, 0.7, color, 2)

    def show(self, frame):
        cv2.imshow(self.cv2_window_name, frame)
        return cv2.waitKey(1)

import cv2

class GestureVisualizer:
    def __init__(self, neutral_low, neutral_high):
        self.neutral_low = neutral_low
        self.neutral_high = neutral_high

    def draw_ui(self, frame, hand1_x, hand2_x):
        height, width, _ = frame.shape
        mid_x = width // 2

        # Neutral zone line coordinates
        left_neutral_start = int(mid_x * self.neutral_low)
        left_neutral_end   = int(mid_x * self.neutral_high)
        right_neutral_start = mid_x + int(mid_x * self.neutral_low)
        right_neutral_end   = mid_x + int(mid_x * self.neutral_high)

        # Draw divider
        cv2.line(frame, (mid_x, 0), (mid_x, height), (128, 128, 128), 3)

        # Hydro neutral zone
        cv2.line(frame, (left_neutral_start, 0), (left_neutral_start, height), (255, 0, 0), 1)
        cv2.line(frame, (left_neutral_end, 0), (left_neutral_end, height), (255, 0, 0), 1)

        # Magma neutral zone
        cv2.line(frame, (right_neutral_start, 0), (right_neutral_start, height), (0, 0, 255), 1)
        cv2.line(frame, (right_neutral_end, 0), (right_neutral_end, height), (0, 0, 255), 1)

        # Text
        font = cv2.FONT_HERSHEY_DUPLEX
        scale = 0.7
        thickness = 2

        color_hydro = (255, 0, 0)
        color_magma = (0, 0, 255)

        # HydroGirl
        cv2.putText(frame, "HydroGirl", (10, 25), font, scale, color_hydro, thickness)
        cv2.putText(frame, f"X: {hand1_x:.2f}", (10, 50), font, scale, color_hydro, thickness)

        # MagmaBoy (right side, aligned)
        magma_label = "MagmaBoy"
        magma_x = f"X: {hand2_x:.2f}"
        label_w = cv2.getTextSize(magma_label, font, scale, thickness)[0][0]
        value_w = cv2.getTextSize(magma_x, font, scale, thickness)[0][0]

        label_x = width - label_w - 10
        value_x = width - value_w - 10

        cv2.putText(frame, magma_label, (label_x, 25), font, scale, color_magma, thickness)
        cv2.putText(frame, magma_x, (value_x, 50), font, scale, color_magma, thickness)

        return frame
    
    def show(self, frame, window_name="MediaPipe Gesture Control (ESC for exit)"):
        cv2.imshow(window_name, frame)
        return cv2.waitKey(1)

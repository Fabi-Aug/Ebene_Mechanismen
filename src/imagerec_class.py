import cv2
import numpy as np

# 1. Bild laden
image = cv2.imread("skizze.png")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 2. Masken für Rot, Blau und Schwarz
lower_red1 = np.array([0, 70, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 70, 50])
upper_red2 = np.array([180, 255, 255])
mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask_red = cv2.bitwise_or(mask_red1, mask_red2)

lower_blue = np.array([100, 100, 50])
upper_blue = np.array([130, 255, 255])
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 50])
mask_black = cv2.inRange(hsv, lower_black, upper_black)

# 3. Konturen für Rot und Blau
def get_centers(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    points = []
    for cnt in contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            points.append((cx, cy))
    return points

red_points = get_centers(mask_red)
blue_points = get_centers(mask_blue)

print("Rote Punkte:", red_points)
print("Blaue Punkte:", blue_points)

# 4. Linien erkennen (Variante Hough-Transform auf Graustufen)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=20, maxLineGap=10)

# 5. Linien-Endpunkte zuordnen
def distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])*2 + (p1[1]-p2[1])*2)

connection_list = []
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        start_pt = (x1, y1)
        end_pt   = (x2, y2)

        # Finde den nächsten roten oder blauen Punkt zum Start
        candidates = red_points + blue_points
        distances_start = [distance(start_pt, c) for c in candidates]
        min_dist_start = min(distances_start) if distances_start else 999999
        idx_start = np.argmin(distances_start) if distances_start else None
        
        # Finde den nächsten roten oder blauen Punkt zum Ende
        distances_end = [distance(end_pt, c) for c in candidates]
        min_dist_end = min(distances_end) if distances_end else 999999
        idx_end = np.argmin(distances_end) if distances_end else None
        
        # Schwellwert, damit man nur "wirklich" verbundene Punkte nimmt
        threshold = 20  # je nach Bildgröße anpassen
        
        if min_dist_start < threshold and min_dist_end < threshold:
            pt1 = candidates[idx_start]
            pt2 = candidates[idx_end]
            connection_list.append((pt1, pt2))

print("Verbindungen gefunden:")
for conn in connection_list:
    print(conn)
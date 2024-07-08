import cv2

cap = cv2.VideoCapture(0)
print(cap)

frame = cap.read()
print(frame)

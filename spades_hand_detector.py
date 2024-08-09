from ultralytics import YOLO
import cv2
import cvzone
import math
import spades_hands_methods
 
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

model = YOLO("playingCards.pt") # Pre-trained model
# model = YOLO("../Yolo-Weights/yolov8n.pt")

class_names = ['10C', '10D', '10H', '10S',
              '2C', '2D', '2H', '2S',
              '3C', '3D', '3H', '3S',
              '4C', '4D', '4H', '4S',
              '5C', '5D', '5H', '5S',
              '6C', '6D', '6H', '6S',
              '7C', '7D', '7H', '7S',
              '8C', '8D', '8H', '8S',
              '9C', '9D', '9H', '9S',
              'AC', 'AD', 'AH', 'AS',
              'JC', 'JD', 'JH', 'JS',
              'KC', 'KD', 'KH', 'KS',
              'QC', 'QD', 'QH', 'QS']

while True:
    success, img = cap.read()
    results = model(img, stream=True)
    hand = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2) 

            w, h = x2-x1, y2-y1
            cvzone.cornerRect(img, (x1,y1,w,h))

            confidence = math.ceil((box.conf[0]*100))/100  # Confidence
            cls = int(box.cls[0]) # Class Name

            cvzone.putTextRect(img, f"{class_names[cls]} {confidence}", (max(0,x1),max(35,y1)), scale=1, thickness=1, colorR = (0,0,0))

            hand.append(class_names[cls])

    hand = list(set(hand)) # Removes any potential duplicates from 2 bounding boxes on the same card
    # print(hand)
    if len(hand) == 13:
        score = spades_hands_methods.calculate_score(hand)
        # print(score)
        cvzone.putTextRect(img, f'Your Hand Score: {score}/10', (300, 75), scale=3, thickness=5, colorR = (0,0,0))
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)

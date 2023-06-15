from ultralytics import YOLO
import cv2

def detectJany(video):
    model = YOLO('/home/dezs/Projects/Scientific research/test/processing/jany.pt')
    cap = cv2.VideoCapture(video)
    # cap.set(3, 640)
    # cap.set(4, 480)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model.predict(img)
        for r in results:
            for box in r.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow('YOLO V8 Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def detectJany(image):
    model = YOLO('/home/dezs/Projects/Scientific research/test/processing/jany.pt')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model.predict(image)
    return results, image
    
def workOnResults(results,image, filename):
    for r in results:
        for box, conf in zip(r.boxes.xyxy, r.boxes.conf):
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            print(conf)
    # cv2.imshow('YOLO V8 Detection', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite(filename, image)
    
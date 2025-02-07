import cv2
from ultralytics import YOLO
import math

model = YOLO("yolov5n.pt")
def get_center(x1, y1, x2, y2):
    x = int((x1 + x2) // 2)
    y = int((y1 + y2) // 2)
    return (x, y)


def analiz_car(file_path):
    detected_cars = 0
    detected_trucks = 0
    tracking_objects = {}
    center_point_prev_frame = []
    track_id = 0
    video = cv2.VideoCapture(file_path)
    frame_count = 0
    frame_skip = 5 

    while True:
        ret, frame = video.read()

        if not ret:
            break

        frame_count += 1
        center_point = []

        if frame_count % frame_skip == 0:
            frame = cv2.resize(frame, (1920, 1080))
            results = model(frame)

            for result in results[0].boxes.data:
                x1, y1, x2, y2, confidence, class_id = result
                label = model.names[int(class_id)]
                if (label == "car" or label == "truck") and confidence >= 0.5:
                     cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
                     cv2.putText(frame, f"{label} ({confidence:.2f})", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                 0.5, (36, 255, 12), 1)

                     if (label == "car"):
                        detected_cars += 1

                     if (label == "truck"):
                         detected_trucks += 1

                     center_x, center_y = get_center(x1, y1, x2, y2)
                     center_point.append((center_x, center_y))

            if frame_count <= 2:
                for pt in center_point:
                    for pt2 in center_point_prev_frame:
                        distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                        if distance < 150:
                            tracking_objects[track_id] = pt
                            track_id += 1

            else:

                tracking_objects_copy = tracking_objects.copy()
                center_point_copy = center_point.copy()

                for object_id, pt2 in tracking_objects_copy.items():
                    objects_exists = False
                    for pt in center_point_copy:
                        distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                        if distance < 150:
                            tracking_objects[object_id] = pt
                            objects_exists = True
                            if pt in center_point:
                                center_point.remove(pt)
                            continue

                    # Remove id
                    if not objects_exists:
                        tracking_objects.pop(object_id)


                for pt in center_point:
                    tracking_objects[track_id] = pt
                    track_id += 1

                for object_id, pt in tracking_objects.items():
                    cv2.circle(frame, pt, 5, (0, 255, 0), -1)
                    cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 1)



            cv2.putText(frame, f"Unique cars: {track_id}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("Object Detection", frame)
            center_point_prev_frame = center_point.copy()

        if cv2.waitKey(1) & 0xFF == 27:
            break

    
    video.release()
    cv2.destroyAllWindows()

    return detected_cars, detected_trucks




""" file = "video/d.mp4"
car, truck = analiz_car(file)
print("сars =", car)
print("trucks =", truck) """
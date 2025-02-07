import cv2
import math


def faceBox(faceNet, frame):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (227, 227), [104, 117, 123], swapRB=False)
    faceNet.setInput(blob)
    detection = faceNet.forward()
    bboxs = []
    for i in range(detection.shape[2]):
        confidence = detection[0, 0, i, 2]
        if confidence > 0.7:
            x1 = int(detection[0, 0, i, 3] * frameWidth)
            y1 = int(detection[0, 0, i, 4] * frameHeight)
            x2 = int(detection[0, 0, i, 5] * frameWidth)
            y2 = int(detection[0, 0, i, 6] * frameHeight)
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            bboxs.append([x1, y1, x2, y2, center_x, center_y])
    return frame, bboxs


def detect_gender_age(frame, x1, y1, x2, y2, male, female):
    blob = cv2.dnn.blobFromImage(frame, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
    genderNet.setInput(blob)
    genderPreds = genderNet.forward()
    gender = genderList[genderPreds[0].argmax()]
    ageNet.setInput(blob)
    agePreds = ageNet.forward()
    age_index = agePreds[0].argmax()

    if age_index < len(ageList):
        age = ageList[age_index]
    else:
        age = "Unknown"

    label = f"{gender}, {age}"

    if (gender == 'Male'):
        male += 1

    if (gender == 'Female'):
        female += 1

    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
    return frame, male, female

facePhoto = "model/opencv_face_detector.pbtxt"
faceModel = "model/opencv_face_detector_uint8.pb"
ageProto = "model/age_deploy.prototxt"
ageModel = "model/age_net.caffemodel"
genderPhoto = "model/gender_deploy.prototxt"
genderModel = "model/gender_net.caffemodel"
faceNet = cv2.dnn.readNet(faceModel, facePhoto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderPhoto)
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-15)', '(16-25)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']


def analiz():
    unique_people_count = 0
    prev_people_positions = {}
    track_id = 0
    video = cv2.VideoCapture(0)
    frame_count = 0
    frame_skip = 3
    male_count = 0
    female_count = 0

    while True:
        ret, frame = video.read()

        if not ret:
            break

        frame, bboxs = faceBox(faceNet, frame)
        frame_count += 1
        center_point = []

        if frame_count %frame_skip == 0:
            for bbox in bboxs:
                x1, y1, x2, y2, center_x, center_y = bbox
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                center_point.append((center_x, center_y))
                frame, male_count, female_count = detect_gender_age(frame, x1, y1, x2, y2, male_count, female_count)

            # Проверяем, является ли человек новым
            for i, current_position in enumerate(center_point):
                is_new = True
                for track_id, prev_position in prev_people_positions.items():
                    distance = math.hypot(prev_position[0] - current_position[0], prev_position[1] - current_position[1])
                    
                    if distance < 220: 
                        is_new = False
                        prev_people_positions[track_id] = current_position
                        break
                if is_new:
                    prev_people_positions[track_id] = current_position
                    unique_people_count += 1
                    track_id += 1

            cv2.putText(frame, f"Unique People: {unique_people_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("Face Detection", frame)

            if cv2.waitKey(1) & 0xFF == 27:  
                break
    video.release()
    cv2.destroyAllWindows()

    return male_count, female_count, unique_people_count



#analiz()
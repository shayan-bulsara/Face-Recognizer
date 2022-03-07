from os import times
from time import time
import face_recognition
import cv2
import winsound
from datetime import datetime
import encd

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

known_face_encodings = []
known_face_names = []
encd.get_encoded_faces('Faces', known_face_names, known_face_encodings)
# Create arrays of known face encodings and their names
x = 0
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
faces_recognized = []
def run(Folder, Arlam):
    encd.get_encoded_faces(Folder, known_face_names, known_face_encodings)
    x = 0
    while True:
        Time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Times = datetime.now().strftime('%Y %m %d    %H %M %S')
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding, 0.5)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face

            face_names.append(name)
            if name not in faces_recognized:
                faces_recognized.append(name)
        if Arlam == 'yes':
            if 'Unknown' in face_names:
                ret, frame = video_capture.read()
                winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
                cv2.imwrite(f'Intuder.jpg', frame)
                if x != 1:
                    print(f"Intruder {Time}")
                    cv2.imwrite(f'Intuder {Times}.jpg', frame)
                    x = 1
            else:
                if x == 1:
                    print(f'Intruder might have left at: {Time}')
                    x = 0

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 5
            right *= 5
            bottom *= 5
            left *= 5

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                        (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, str(name), (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(f'The faces recognized were: {faces_recognized}')
            break

        if cv2.waitKey(1) & 0xFF == ord('r'):
            print(f'The faces recognized were: {faces_recognized}')

    video_capture.release()
    cv2.destroyAllWindows()

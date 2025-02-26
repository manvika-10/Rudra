import cv2
import face_recognition
import numpy as np
import os


# haar_cascade = cv2.CascadeClassifier('haar_face.xml')
# capture = cv2.VideoCapture(0)
# while True:
#     isTrue, frame = capture.read()
#     faces_rect1 = haar_cascade.detectMultiScale(
#         frame, scaleFactor=1.5, minNeighbors=3)
#     for(x, y, w, h) in faces_rect1:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)
#     cv2.imshow('Detected Faces', frame)
#     if cv2.waitKey(20) & 0xFF == ord('d'):
#         break
# capture.release()
# cv2.destroyAllWindows
# cv2.waitKey(0)
KNOWN_FACES_DIR = os.path.join(os.path.join(os.getcwd(), 'faces'), 'TH.jpg')
MAX_FRAMES = 60

def encode_faces():
        # Each subfolder's name becomes our label (name)
        known_faces = []
        known_names = []
    
        # Next we load every file of faces of known person
        # Load an image
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}')

        # Get 128-dimension face encoding
        # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
        encoding = face_recognition.face_encodings(image)[0]

        # Append encodings and name
        known_faces.append(encoding)
        known_names.append('Tom Holland')
        return known_faces, known_names


def find_faces(small_frames, known_face_encodings, known_face_names):
    is_known_face = False
    face_names = set()
    for rgb_small_frame in small_frames:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                face_names.add(name)
                is_known_face = True
    return face_names, face_locations

def process_video():
        frame = cv2.imread(os.path.join(os.getcwd(), 'GP.jpg'))
        known_face_encodings, known_face_names = encode_faces()
        # Initialize some variables
        frames = []
        small_frames = []
    
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        small_frames.append(rgb_small_frame)

        people, locations = find_faces(small_frames, known_face_encodings, known_face_names)

            # Display the results
        for (top, right, bottom, left), name in zip(locations, people):
            # Draw a box around the face
            cv2.rectangle(small_frame, (left - 5, top - 7), (right + 5, bottom + 5), (0, 0, 255), 2)

            # Draw a label with a name below the face
            #cv2.rectangle(small_frame, (left, bottom - 35), (right, bottom), (0, 0, 255))
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(small_frame, name, (left - 10, bottom + 10), font, 0.75, (255, 255, 255), 1)

        while True:
            cv2.imshow('Image', small_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        
        #print(people)
        # Display the resulting image
        
        # Hit 'q' on the keyboard to quit!
       
    

process_video()
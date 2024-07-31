from flask import Flask, render_template, request, redirect, url_for, Response
import os
import cv2
import numpy as np
import face_recognition
from twilio.rest import Client
import geocoder
from geopy.geocoders import Nominatim

app = Flask(__name__)

known_face_encodings = []
known_face_names = []

# Preload known faces
known_face_names = ["riya"]
for name in known_face_names:
    image = face_recognition.load_image_file(f"uploads/{name}.jpg")
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)

DATA_DIR = "data"

def create_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

# Function to extract face encodings
def extract_face_encodings(image_path):
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
    return face_locations, face_encodings

# Function to compare face encodings
def compare_face_encodings(known_face_encoding, unknown_face_encoding):
    return face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)

# Function to send SMS using Twilio
def send_sms(message, recipient):
    account_sid = 'xyz'
    auth_token = 'xyz'
    twilio_number = 'xyz'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=recipient
    )

def get_live_location():
    try:
        g = geocoder.ip('me')
        if g.latlng:
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.reverse(g.latlng, language='en')
            if location:
                return location.address
    except Exception as e:
        print(f"Error getting live location: {e}")
    return "Unknown location"

def detect_faces(frame):
    known_face_encodings = []
    known_face_names = []

    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith(".txt"):
            with open(os.path.join(DATA_DIR, file_name), "r") as file:
                details = file.readlines()
                face_encoding_str = details[4].split(":")[1].strip()
                face_encoding = np.fromstring(face_encoding_str, sep=',')
                known_face_encodings.append(face_encoding)
                known_face_names.append(details[0].split(":")[1].strip())

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            location = get_live_location()
            message = f"The missing person {name} has been found! Location: {location}. Contact the nearest help for further assistance."
            send_sms(message, '#enteryourmobilenumber')

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
    return frame

def gen_frames():
    camera = cv2.VideoCapture(0)
    frame_count = 0
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame_count += 1
            frame = detect_faces(frame)
            if frame_count % 100 == 0:
                location = get_live_location()
                send_sms(f"This is a test message. Current location: {location}", '+1234567890')
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        phone_number = request.form['phone_number']
        image = request.files['image']

        image_filename = f"{name}.jpg"
        image_path = os.path.join(DATA_DIR, image_filename)
        image.save(image_path)

        face_locations, face_encodings = extract_face_encodings(image_path)

        if face_encodings:
            with open(os.path.join(DATA_DIR, f"{name}.txt"), "w") as file:
                file.write(f"Name: {name}\n")
                file.write(f"Location: {location}\n")
                file.write(f"Phone Number: {phone_number}\n")
                file.write(f"Image: {image_filename}\n")
                file.write(f"Face Encoding: {','.join(str(x) for x in face_encodings[0])}\n")

        return redirect(url_for('home', success='true'))

    return render_template('register.html')

@app.route('/find_missing_person')
def find_missing_person():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    create_data_dir()
    app.run(debug=True)

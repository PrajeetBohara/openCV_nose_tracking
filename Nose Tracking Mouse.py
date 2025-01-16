#Python Noise Tracking Mouse


from pynput.mouse import Controller
import cv2
import pyautogui

mouse = Controller()

# Load Haar cascades for face and nose detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
nose_cascade = cv2.CascadeClassifier('C:/Users/Prajeet/haarcascade_mcs_nose.xml')

cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

center_x, center_y = None, None
sensitivity = 2.0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_roi_gray = gray[y:y+h, x:x+w]
        noses = nose_cascade.detectMultiScale(face_roi_gray, 1.3, 5)

        for (nx, ny, nw, nh) in noses:
            nose_x = x + nx + nw // 2
            nose_y = y + ny + nh // 2

            cv2.circle(frame, (nose_x, nose_y), 5, (0, 255, 0), -1)

            if center_x is None and center_y is None:
                center_x, center_y = nose_x, nose_y

            delta_x = nose_x - center_x
            delta_y = nose_y - center_y

            move_x = delta_x * sensitivity
            move_y = delta_y * sensitivity

            current_mouse_x, current_mouse_y = mouse.position

            new_mouse_x = max(0, min(current_mouse_x + move_x, screen_width - 1))
            new_mouse_y = max(0, min(current_mouse_y + move_y, screen_height - 1))

            mouse.position = (new_mouse_x, new_mouse_y)

            break

    cv2.imshow('Head Movement Mouse Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()






















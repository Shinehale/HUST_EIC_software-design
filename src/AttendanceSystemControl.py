import cv2
import os
import time, datetime
import customtkinter as cstk
import shutil
from collections import defaultdict
import numpy as np

from src.AttendanceSystemData import Data


class Control:
    # define the password to check the user or administrator
    password = '123456'
    images_path = './captured_images/'
    data_path = './data/'
    gray_images_path = './gray_images/'
    password_file_path = './data/pwd.file'


    def __init__(self):
        self.toplevel_window = None
        self.key = 10

    @staticmethod
    def validate_password(input_pwd: str):
        Control.read_password()
        if input_pwd == Control.password:
            return True
        else:
            return False

    @staticmethod
    def fetch_image_by_id(index):
        files_and_folders = os.listdir(Control.images_path)
        for item in files_and_folders:
            if not item == str(index):
                continue
            item_path = os.path.join(Control.images_path, item)
            for file in os.listdir(item_path):
                return os.path.join(item_path, file)


    @staticmethod
    def delete_image_by_id(index):
        files_and_folders = os.listdir(Control.images_path)
        for item in files_and_folders:
            if not item == str(index):
                continue
            item_path = os.path.join(Control.images_path, item)
            shutil.rmtree(item_path)
        files_and_folders = os.listdir(Control.gray_images_path)
        for item in files_and_folders:
            if not item == str(index):
                continue
            item_path = os.path.join(Control.gray_images_path, item)
            shutil.rmtree(item_path)

    @staticmethod
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        cstk.set_widget_scaling(new_scaling_float)

    @staticmethod
    def sidebar_button_event():
        print("sidebar_button click")

    @staticmethod
    def get_current_time():
        mont = {'01': 'January',
                '02': 'February',
                '03': 'March',
                '04': 'April',
                '05': 'May',
                '06': 'June',
                '07': 'July',
                '08': 'August',
                '09': 'September',
                '10': 'October',
                '11': 'November',
                '12': 'December'
                }
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        day, month, year = date.split("-")
        return f"{day}-{mont[month]}-{year}"

    @staticmethod
    def get_total_register_number():
        return len(Data.keymap_label)

    @staticmethod
    def take_photos(id, name):
        print('take the photos', id, name)
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        output_path = os.path.join(Control.images_path, '{0}'.format(id))

        # Check if the folder exists, if not, create it
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        count = 0

        while count < 10:
            ret, frame = cap.read()
            face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                if w * h < 150 * 150:
                    continue
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Crop the face region and save
                face_roi = frame[y:y + h, x:x + w]
                file_name = os.path.join(output_path, "{}_{}.png".format(name, count))
                cv2.imwrite(file_name, face_roi)
                print("Captured face {} saved.".format(count))

            # show the frame
            cv2.imshow('Capture', frame)

            capture_interval = 1
            if time.time() % capture_interval < 0.1:
                # add the counter
                count += 1
            # wait for a second
            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()


    @staticmethod
    def encrypt(pwd, key):
        data_list = [int(d) for d in pwd]
        encrypted_data = [str(int(d) ^ key) for d in data_list]
        return encrypted_data

    @staticmethod
    def train_images():
        Control.convert_gray_faces()
        faces, labels = [], []
        label = 0
        for index in os.listdir(Control.gray_images_path):
            index_path = os.path.join(Control.gray_images_path, index)
            for each in os.listdir(index_path):
                each_path = os.path.join(index_path, each)
                gray_np = np.array(cv2.imread(each_path, 0), 'uint16')
                name = each.split('_')[0]
                labels.append(label)
                faces.append(gray_np)
            print(index, label)
            label += 1

        data_path = os.path.join(Control.data_path, 'train.yml')
        if not os.path.exists(Control.data_path):
            os.makedirs(Control.data_path)
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # 初始化LBPH识别器
        recognizer.train(faces, np.array(labels))
        recognizer.save(data_path)
        Data.update_info_table()


    @staticmethod
    def convert_gray_faces():
        if not os.path.exists(Control.gray_images_path):
            os.makedirs(Control.gray_images_path)

        files_and_folders = os.listdir(Control.images_path)
        for item in files_and_folders:
            gray_folder = os.path.join(Control.gray_images_path, item)
            if not os.path.exists(gray_folder):
                os.makedirs(gray_folder)
            for each in os.listdir(os.path.join(Control.images_path, item)):
                each_path = os.path.join(gray_folder, each)
                if not os.path.exists(each_path):
                    ori_path = os.path.join(Control.images_path, item, each)
                    img = cv2.imread(ori_path)
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(each_path, gray_img)

    @staticmethod
    def recognise_face():
        # check the model data exists and load the data
        yml_data = os.path.join(Control.data_path, 'train.yml')
        if not os.path.exists(yml_data):
            Control.train_images()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(yml_data)
        face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')

        confirmation_interval = 10
        last_confirmation_time = time.time()
        cap = cv2.VideoCapture(0)
        times = defaultdict(int)
        flag = True
        while flag:
            ret, frame = cap.read()
            cv2.imshow('Taking Attendance', frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=5)
            for (x, y, w, h) in faces:
                if w * h < 150 * 150:
                    continue
                cv2.rectangle(frame, (x, y), (x + w, y + h), (225, 0, 0), 2)
                label, score = recognizer.predict(gray[y:y + h, x:x + w])
                if score < 50:
                    times[label] += 1
                    if times[label] > 20:
                        flag = False
            cv2.imshow('Taking Attendance', frame)
            cur_time = time.time()
            if cur_time - last_confirmation_time > confirmation_interval:
                break

            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        index, max_value = -1, 0
        for key, value in times.items():
            if value > 20 and value > max_value:
                index = key
                max_value = value
        return index

    @staticmethod
    def change_password(ori: str, new: str):
        if not Control.validate_password(ori):
            return False
        else:
            Control.password = new
            Control.write_password()
        return True

    @staticmethod
    def read_password():
        with open(Control.password_file_path, 'r') as file:
            pwd = file.readline()
            Control.password = pwd

    @staticmethod
    def write_password():
        if not os.path.exists(Control.password_file_path):
            open(Control.password_file_path, 'w')
        with open(Control.password_file_path, 'w') as file:
            file.write(Control.password)








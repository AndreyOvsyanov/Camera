import threading
import time

import cv2
import customtkinter as ctk
from customtkinter import CTkComboBox
from PIL import Image, ImageTk

from constant import AUDI
from model import count_people_on_audit
from analytics import get_employment
from rightech import mqttclient
from information.plugins import init_security, get_current_datetime


class MainWindow:

    def __init__(self, window: ctk.CTk):
        self._window = window
        self._window.title("Главное окно")
        self._window.config(background="#000000")
        self._window.iconbitmap("content/imgs/brain.ico")
        self.cap = None
        self.current_frame = None

        # Создание виртуального окружения
        self.create_environment()


    def create_environment(self):

        self._container = ctk.CTkFrame(self._window)
        self._container.pack(side=ctk.LEFT, expand=True)

        # Выбрать аудиторию
        self.auditoriums = CTkComboBox(master=self._container, values=list(AUDI.keys()), font=("Courier", 20, "bold"))
        self.auditoriums.pack(pady=10)

        # Действие для обработки
        # Бесконечное функция на подсчёт людей
        self.action = False
        threading.Thread(target=self.click_people).start()

        # Передать видеопоток в окошко по конкретной аудитории
        self.button_check = ctk.CTkButton(master=self._container, text="Посмотреть", command=self.click_audi)
        self.button_check.pack(pady=5)

        # Окончание работы подсчёта
        self.button_post = ctk.CTkButton(master=self._container, text="Закончить", command=self.click_end)
        self.button_post.pack(pady=5)

        # Получить статистику по насчитанным данным
        self.button_stat = ctk.CTkButton(master=self._container, text="Получить статистику", command=self.add_statistic)
        self.button_stat.pack(pady=5)

        self.camera_stream = ctk.CTkFrame(master=self._window)
        self.camera_stream.pack(padx=5, pady=5)
        self.labelmain = ctk.CTkLabel(master=self.camera_stream, text="", width=480, height=480)
        self.labelmain.grid()


    def get_imgtk(self, frame):
        #frame = cv2.resize(frame, (640, 640))
        normal_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(normal_frame)
        imgtk = ImageTk.PhotoImage(image=img)

        return imgtk


    def show_stream(self):
        _success, frame = self.cap.read()
        if _success:
            self.current_frame = frame
            imgtk = self.get_imgtk(frame)
            self.labelmain.imgtk = imgtk
            self.labelmain.configure(image=imgtk)

            if self._flag:
                self.labelmain.after(25, self.show_stream)
            else:
                self.cap.release()


    def click_audi(self):
        self._flag = False
        self.auditorium = self.auditoriums.get()

        path = "content/videos/"
        cmr = AUDI.get(self.auditorium)

        if not cmr:
            self.cap = cv2.VideoCapture(cmr)
            print("Connection success, please show your camera device >> ".format(self.auditorium))
        else:
            self.cap = cv2.VideoCapture(path + cmr)
            print("Connection success, please show {} auditorium >> ".format(self.auditorium))

        self.action = True
        self._flag = True

        self.show_stream()


    def click_people(self):
        while self.action:
            if not self.current_frame is None:
                cnt_people = count_people_on_audit(self.current_frame)

                current_date = get_current_datetime()
                if self.auditorium == "Камера устройства":
                    audit = 217
                else:
                    audit = self.auditorium

                object = {
                    'base/state/datetime': current_date,
                    'base/state/audit': audit,
                    'base/state/numperson': cnt_people
                }

                mqttclient.publish_msg(object)

                print("Количество людей в аудитории: {}".format(cnt_people))

            time.sleep(2)

        time.sleep(0.125)
        self.click_people()


    def click_end(self):
        self.action = False


    def add_statistic(self):
        employment = get_employment()
        employment.to_csv('employment.csv', mode='a', index=False, header=False)


    def mainloop(self):
        self._window.mainloop()




init_security()
root = ctk.CTk()
root.geometry("720x500")
root.grid()
mainwindow = MainWindow(window=root)
mainwindow.mainloop()
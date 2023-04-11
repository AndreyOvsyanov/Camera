import cv2
import customtkinter as ctk
from customtkinter import CTkComboBox
from PIL import Image, ImageTk

from constant import AUDI, CASCADE_FACE_PATH


cascade = cv2.CascadeClassifier(CASCADE_FACE_PATH)


class MainWindow:

    def __init__(self, window: ctk.CTk):
        self._window = window
        self._window.title("Главное окно")
        self._window.config(background="#" + "0"*6)
        self._window.iconbitmap("content/imgs/brain.ico")
        self.caps = []
        self.current_frames = [0]*2

        self.create_environment()


    def create_environment(self):

        self._container = ctk.CTkFrame(self._window)
        self._container.pack(side=ctk.LEFT, expand=True)

        self.auditoriums = CTkComboBox(master=self._container, values=list(AUDI.keys()), font=("Courier", 20, "bold"))
        self.auditoriums.pack(pady=10)

        self.button_check = ctk.CTkButton(master=self._container, text="Посмотреть", command=self.click_audi)
        self.button_check.pack(pady=10)

        self.button_post = ctk.CTkButton(master=self._container, text="Получить людей", command=self.click_people)
        self.button_post.pack(pady=10)

        self.camera_streams = []
        self.labelsmain = []
        for iter in range(2):
            self.camera_streams.append(ctk.CTkFrame(master=self._window))
            self.camera_streams[iter].pack(padx=10, pady=10)
            self.labelsmain.append(ctk.CTkLabel(master=self.camera_streams[iter], text="", width=515, height=290))
            self.labelsmain[iter].grid()


    def get_imgtk(self, frame):
        frame = cv2.resize(frame, (640, 360))
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        return imgtk


    def show_stream(self):
        (_o, one_frame), (_t, two_frame) = (self.caps[idx].read() for idx in range(len(self.caps)))
        if all((_o, _t)):
            self.current_frames[0] = one_frame
            imgtk = self.get_imgtk(one_frame)
            self.labelsmain[0].imgtk = imgtk
            self.labelsmain[0].configure(image=imgtk)

            self.current_frames[1] = two_frame
            imgtk = self.get_imgtk(two_frame)
            self.labelsmain[1].imgtk = imgtk
            self.labelsmain[1].configure(image=imgtk)

            if all(self._flags):
                self.labelsmain[0].after(25, lambda: self.show_stream())
            else:
                (cap.release for cap in self.caps)



    def click_audi(self):
        self._flags = (False for _ in range(2))
        auditorium = self.auditoriums.get()
        path = "content/videos/"

        cmrs = AUDI.get(auditorium)

        self.caps = (cv2.VideoCapture(path + cmrs[0]), cv2.VideoCapture(path + cmrs[1]))
        print("Connection success, please show {} auditorium >> ".format(auditorium))
        self._flags = (True for _ in range(2))
        self.show_stream()


    def click_people(self):
        (one, two) = (cascade.detectMultiScale(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)) for fr in self.current_frames)
        print("One: {}, Two: {}".format(len(one), len(two)))


    def mainloop(self):
        self._window.mainloop()


root = ctk.CTk()
root.geometry("720x640")
root.grid()
mainwindow = MainWindow(window=root)
mainwindow.mainloop()
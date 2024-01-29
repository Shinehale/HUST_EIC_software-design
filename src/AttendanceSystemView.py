import time

import customtkinter
import customtkinter as cstk
import tkinter as tk
from tkinter import ttk

import cv2

from src.AttendanceSystemControl import Control as ctrl
from src.CustomDialog import ToplevelWindow, SecondTimeCheck, ChangePasswordDialog
from src.AttendanceSystemData import Data


class AttendanceSystemView(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = None
        self.attend_info = None
        self.initialize_GUI()

        self.toplevel_window = None
        self.image_window = None

    def run(self):
        self.mainloop()

    def initialize_GUI(self):
        cstk.set_appearance_mode('dark')
        cstk.set_default_color_theme('blue')

        # configure the window
        self.title('Facial Recognition Attendance System')
        self.geometry('1100x580')
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create the labels in the UI view
        self.create_sidebar_frame()
        self.create_attendance_frame()
        self.create_time_frame()
        self.create_option_frame()
        self.create_register_frame()

    # create sidebar frame with widgets
    def create_sidebar_frame(self):
        sidebar_frame = cstk.CTkFrame(self, width=140)
        sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        sidebar_frame.grid_rowconfigure(5, weight=1)
        logo_label = cstk.CTkLabel(sidebar_frame, text="Main Menu", font=cstk.CTkFont(size=24, weight="bold"))
        logo_label.grid(row=0, column=0, padx=5, pady=(20, 10))
        sidebar_label = cstk.CTkLabel(sidebar_frame, text="Enter ID", font=cstk.CTkFont(size=15, weight="bold"))
        sidebar_label.grid(row=1, column=0, padx=20)
        sidebar_entry_ID = cstk.CTkEntry(sidebar_frame, placeholder_text="001")
        sidebar_entry_ID.grid(row=2, column=0, padx=20, pady=(10, 10))
        sidebar_button_1 = cstk.CTkButton(sidebar_frame,
                                          command=lambda: self.view_face(sidebar_entry_ID.get()),
                                          text="View Face")
        sidebar_button_1.grid(row=3, column=0, padx=20, pady=(10, 10))
        sidebar_button_2 = cstk.CTkButton(sidebar_frame,
                                          command=lambda: self.delete_face(sidebar_entry_ID.get()),
                                          text="Delete Faces")
        sidebar_button_2.grid(row=4, column=0, padx=20, pady=(10, 10))
        sidebar_button_3 = cstk.CTkButton(sidebar_frame,
                                          command=self.change_password,
                                          text="Change PassWord")
        sidebar_button_3.grid(row=5, column=0, padx=20, pady=(160, 10))
        scaling_label = cstk.CTkLabel(sidebar_frame, text="UI Scaling:", anchor="w")
        sidebar_button_4 = cstk.CTkButton(sidebar_frame,
                                          command=self.pulse_detect,
                                          text='Pulse Detect')
        sidebar_button_4.grid(row=6, column=0, padx=20, pady=10)
        scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        scaling_option_menu = cstk.CTkOptionMenu(sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                 command=ctrl.change_scaling_event)
        scaling_option_menu.grid(row=8, column=0, padx=20, pady=(10, 20))
        scaling_option_menu.set("100%")

    # create attendance frame with widgets
    def create_attendance_frame(self):
        attendance_frame = cstk.CTkScrollableFrame(self, label_text="ATTENDANCE LIST",
                                                   label_font=cstk.CTkFont(size=24, weight="bold"))
        attendance_frame.grid(row=0, column=1, padx=(30, 20), pady=(0, 0), sticky="nsew")
        attendance_frame.grid_columnconfigure(0, weight=1)
        self.attend_info = ttk.Treeview(attendance_frame, show="headings",
                                        columns=('ID', 'name', 'date', 'check_in', 'check_out'),
                                        height=10)
        self.attend_info.column('ID', width=100, anchor=tk.CENTER)
        self.attend_info.column('name', width=100, anchor=tk.CENTER)
        self.attend_info.column('date', width=100, anchor=tk.CENTER)
        self.attend_info.column('check_in', width=150, anchor=tk.CENTER)
        self.attend_info.column('check_out', width=150, anchor=tk.CENTER)
        self.attend_info.heading('ID', text='ID')
        self.attend_info.heading('name', text='NAME')
        self.attend_info.heading('date', text='DATE')
        self.attend_info.heading('check_in', text='CHECK_IN')
        self.attend_info.heading('check_out', text='CHECK_OUT')
        ttk.Style().configure("Treeview", rowheight=50, font=('Arial', 18, 'bold'))
        ttk.Style().configure('Treeview.Heading', font=('Arial', 20, 'bold'))
        self.attend_info.grid(row=1, column=0, padx=(10, 10), pady=(5, 5), sticky='nsew')

    # create register frame with widgets
    def create_register_frame(self):
        register_frame = cstk.CTkFrame(self, width=300)
        register_frame.grid(row=0, column=2, padx=(10, 20), pady=(10, 10), sticky="nsew")
        register_label_1 = cstk.CTkLabel(register_frame, text="For New Registrations",
                                         font=cstk.CTkFont(size=20, weight="bold"))
        register_label_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        register_label_2 = cstk.CTkLabel(register_frame, text="Enter ID",
                                         font=cstk.CTkFont(size=16, weight="bold"))
        register_label_2.grid(row=1, column=0, padx=20, pady=(20, 10))
        register_entry_ID = cstk.CTkEntry(register_frame, placeholder_text="001")
        register_entry_ID.grid(row=2, column=0, padx=20, pady=(20, 10))
        register_label_3 = cstk.CTkLabel(register_frame, text="Enter Name",
                                         font=cstk.CTkFont(size=16, weight="bold"))
        register_label_3.grid(row=3, column=0, padx=20, pady=(20, 10))
        register_entry_name = cstk.CTkEntry(register_frame, placeholder_text="Mike")
        register_entry_name.grid(row=4, column=0, padx=20, pady=(20, 10))
        register_button = cstk.CTkButton(register_frame,
                                         command=lambda: self.register_new_figure(register_entry_ID.get(),
                                                                                  register_entry_name.get()),
                                         text="Add Faces",
                                         font=cstk.CTkFont(size=16, weight="bold"))
        register_button.grid(row=5, column=0, padx=20, pady=(40, 10))
        self.message = cstk.CTkLabel(register_frame, font=cstk.CTkFont(size=12, weight="bold"))
        self.message.grid(row=6, column=0, padx=20, pady=(20, 10))
        self.message.configure(text='Total Registrations till now  : {}'.format(ctrl.get_total_register_number()))

    # create option frame with widgets
    def create_option_frame(self):
        option_frame = cstk.CTkFrame(self)
        option_frame.grid(row=1, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        option_button_1 = cstk.CTkButton(option_frame,
                                         command=self.make_attendance,
                                         text="Take  Attendance",
                                         font=cstk.CTkFont(size=20, weight="bold"), width=300)
        option_button_1.grid(row=0, column=0, padx=20, pady=40)
        option_button_2 = cstk.CTkButton(option_frame,
                                         command=self.clear_history,
                                         text="Clear  History",
                                         font=cstk.CTkFont(size=20, weight="bold"), width=300)
        option_button_2.grid(row=0, column=1, padx=20, pady=40)
        option_frame.grid_columnconfigure(0, weight=1)
        option_frame.grid_columnconfigure(1, weight=1)
        option_frame.grid_columnconfigure(0, weight=1)

    # create time frame with widgets
    def create_time_frame(self):
        time_frame = cstk.CTkFrame(self)
        time_frame.grid(row=1, column=2, padx=(20, 20), pady=(10, 10), sticky="nsew")
        date_frame = cstk.CTkLabel(time_frame, text=ctrl.get_current_time(),
                                   font=cstk.CTkFont('times', 22, 'bold'))
        date_frame.grid(row=0, column=0, padx=45, pady=(20, 10))
        clock = cstk.CTkLabel(time_frame, font=cstk.CTkFont('times', 22, 'bold'))
        clock.grid(row=1, column=0, padx=45, pady=(10, 10))

        def tick():
            time_string = time.strftime('%H:%M:%S')
            clock.configure(text=time_string)
            clock.after(200, tick)

        tick()

    def validate_password_window(self):
        dialog = customtkinter.CTkInputDialog(text="Type in the administrative password:", title="validation")
        pwd = dialog.get_input()

        # the password is not correct
        if not ctrl.validate_password(pwd):
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()  # if window exists focus it
            return False
        else:
            return True

    def register_new_figure(self, id, name):
        # validate the password
        if not self.validate_password_window():
            return

        # add the new tuple(id, name) and figure into the resources
        ctrl.take_photos(id, name)
        ctrl.train_images()
        self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        self.toplevel_window.change_text('\n\nSuccessful add \n {0} \ninformation!!! '
                                             .format(Data.fetch_name_by_id(id)))

        self.message.configure(text='Total Registrations till now  : {}'.format(ctrl.get_total_register_number()))

    def view_face(self, index):
        # validate the password
        if not self.validate_password_window():
            return
        image_path = ctrl.fetch_image_by_id(index)
        image = cv2.imread(image_path)
        if image is None:
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.change_text('\n\nDon\'t have \nid: {0}\n information!!!'.format(index))
        else:
            cv2.imshow('{0}'.format(index), image)

    def delete_face(self, index):
        # validate the password
        if not self.validate_password_window():
            return
        image_path = ctrl.fetch_image_by_id(index)
        image = cv2.imread(image_path)
        if image is None:
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.change_text('\n\nDon\'t have \nid: {0}\n information!!!'.format(index))
        else:
            dialog = customtkinter.CTkInputDialog(text="Are you sure delete {0} information?\n"
                                                       "This operation is irreversible\n"
                                                       "Input 'yes' to confirm".format(Data.fetch_name_by_id(index)),
                                                  title="confirm",
                                                  font=cstk.CTkFont('times', 20, 'bold'))
            response = dialog.get_input()
            if response == 'yes':
                ctrl.delete_image_by_id(index)
        ctrl.train_images()

    def make_attendance(self):
        def handler_data(func):
            id, name, pwd = func()
            self.toplevel_window.destroy()
            if not ctrl.validate_password(pwd):
                self.toplevel_window = ToplevelWindow(self)
            elif Data.fetch_name_by_id(id) != name:
                self.toplevel_window = ToplevelWindow(self)
                self.toplevel_window.change_text('\n\nDon\'t have \nname: {0}\n information!!!', name)
            else:
                status, id, name = Data.make_records(Data.fetch_label_by_id(id))
                string = '\n\n{0}({1})\n check in \n successfully'.format(name, id)
                if not status:
                    string = '\n\n{0}({1})\n check out \n successfully'.format(name, id)
                self.toplevel_window = ToplevelWindow(self)
                self.toplevel_window.change_text(string)
            self.toplevel_window.lift()
            self.render_list_data()

        label = ctrl.recognise_face()
        if label == -1:
            self.toplevel_window = SecondTimeCheck(handler_data, self)  # create window if its None or destroyed
            self.toplevel_window.lift()
        else:
            status, id, name = Data.make_records(label)
            string = '\n\n{0}({1})\n check in \n successfully'.format(name, id)
            if not status:
                string = '\n\n{0}({1})\n check out \n successfully'.format(name, id)
            if self.toplevel_window is not None:
                self.toplevel_window.destroy()
            self.toplevel_window = ToplevelWindow(self)
            self.toplevel_window.change_text(string)
        self.toplevel_window.lift()
        self.render_list_data()

    def clear_history(self):
        Data.update_records_table()
        self.render_list_data()

    def render_list_data(self):
        data = Data.render_data()
        for row in self.attend_info.get_children():
            self.attend_info.delete(row)
        for row_data in data:
            self.attend_info.insert("", "end", values=row_data, tags=("Arial", 16))

    def change_password(self):
        def handle_data(func):
            ori, new = func()
            if self.toplevel_window is not None:
                self.toplevel_window.destroy()
                self.toplevel_window = None
            status = ctrl.change_password(ori, new)
            if status:
                self.toplevel_window = ToplevelWindow(self)
                self.toplevel_window.change_text('\n\nChange Password\n Successfully!!!\n')
            else:
                self.toplevel_window = ToplevelWindow(self)
                self.toplevel_window.change_text('\n\nOriginal Password\n is Wrong!!!\n')
            self.toplevel_window.lift()
        self.toplevel_window = ChangePasswordDialog(handle_data, self)

    def pulse_detect(self):
        Data.run_detect()






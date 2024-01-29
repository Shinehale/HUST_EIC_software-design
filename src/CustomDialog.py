import customtkinter as cstk
import customtkinter


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x200")
        self.title('Notification')

        self.label = customtkinter.CTkLabel(self, text="\n\nInvalid \nadministrator\n password",
                                            font=cstk.CTkFont('times', 22, 'bold'))
        self.label.pack(padx=20, pady=20)

    def change_text(self, text: str):
        self.label.configure(text=text)


class SecondTimeCheck(cstk.CTkToplevel):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title('Second time check')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # 创建Label和Entry部件
        self.create_label("Unable to identify\nMaybe use password?", row=0)
        self.create_label_and_entry("Enter ID", row=1, placeholder="001")
        self.create_label_and_entry("Enter Name", row=2, placeholder="Mike")
        self.create_label_and_entry("Enter Password", row=3, placeholder="XXXXXX")

        # create a button
        submit_button = cstk.CTkButton(self, text="Submit",
                                       command=lambda: callback(self.submit_data))
        submit_button.grid(row=4, column=0, columnspan=2, pady=(10, 10), padx=(100, 100), sticky='ew')

    def submit_data(self):
        # 获取输入的数据
        id_value = self.get_entry_value(1)
        name_value = self.get_entry_value(2)
        password_value = self.get_entry_value(3)
        return id_value, name_value, password_value

    def get_entry_value(self, row):
        # 获取指定行的Entry部件的值
        entry = self.winfo_children()[row * 2]
        return entry.get()

    def create_label_and_entry(self, label_text, row, placeholder=None):
        label = cstk.CTkLabel(self, text=label_text, font=cstk.CTkFont(size=16, weight="bold"))
        entry = cstk.CTkEntry(self, placeholder_text=placeholder)

        label.grid(row=row, column=0, padx=(20, 10), pady=(10, 10), sticky="w")
        entry.grid(row=row, column=1, padx=(10, 20), pady=(10, 10), sticky="e")

    def create_label(self, label_text, row):
        label = cstk.CTkLabel(self, text=label_text, font=cstk.CTkFont(size=20, weight="bold"))
        label.grid(row=row, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")


class ChangePasswordDialog(cstk.CTkToplevel):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry('400x300')
        self.title('Change Password')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # 创建Label和Entry部件
        self.create_label('Change Administrator Password', row=0)
        self.create_label_and_entry("Enter Original", row=1, placeholder="XXXX")
        self.create_label_and_entry("Enter Updated", row=2, placeholder="XXXX")

        # create a button
        submit_button = cstk.CTkButton(self, text="Submit",
                                       command=lambda: callback(self.submit_data))
        submit_button.grid(row=3, column=0, columnspan=2, pady=(10, 10), padx=(100, 100), sticky='ew')

    def submit_data(self):
        # 获取输入的数据
        ori_value = self.get_entry_value(1)
        new_value = self.get_entry_value(2)
        return ori_value, new_value

    def get_entry_value(self, row):
        # 获取指定行的Entry部件的值
        entry = self.winfo_children()[row * 2]
        return entry.get()
    def create_label(self, label_text, row):
        label = cstk.CTkLabel(self, text=label_text, font=cstk.CTkFont(size=20, weight="bold"))
        label.grid(row=row, column=0, columnspan=2, padx=20, pady=(20, 40), sticky="ew")

    def create_label_and_entry(self, label_text, row, placeholder=None):
        label = cstk.CTkLabel(self, text=label_text, font=cstk.CTkFont(size=16, weight="bold"))
        entry = cstk.CTkEntry(self, placeholder_text=placeholder)

        label.grid(row=row, column=0, padx=(20, 10), pady=(10, 10), sticky="w")
        entry.grid(row=row, column=1, padx=(10, 20), pady=(10, 10), sticky="e")




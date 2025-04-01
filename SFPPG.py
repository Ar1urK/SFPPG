import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from dateutil.relativedelta import relativedelta
from SFPPG_Database import SFPPG_Database as db


def main():
    app = SFPPG_GUI()
    print("All good!")

# The class of an app
class SFPPG_GUI():
    def __init__(self):
        self.database = db()
        self.login_screen = login_screen()
        self.login_screen.resizable(False, False)
        
        self.login_screen.mainloop()
        user_id = self.login_screen.get_user_id()


        # if app is colsed befor user logs in second window will not open
        if self.login_screen.get_user_in() == False:
            return None
        
        self.root = Main_screen(user_id)
        self.root.resizable(False, False)
        self.root.mainloop()

# A class that creates a main window with all functionality of an app
class Main_screen(tk.Tk):
    def __init__(self, user_id):
        super().__init__()
        self.title("SFPPG")
        self.geometry("600x300")
        nb = ttk.Notebook(self)
        profile = User_profile(nb, user_id)
        nb.add(profile, text = "Profile")
        spendings = Past_spendings(nb, user_id)
        nb.add(spendings, text = "Spendings")
        plans = Plan_spendings(nb, user_id)
        nb.add(plans, text = "Plan")
        

        nb.pack(fill= tk.BOTH, expand=True)
        

class User_profile(ttk.Frame):
    def __init__(self, nb, user_id):
        super().__init__(nb)
        self.database = db()


        self.user_info = User_frame(self, user_id)
        self.user_info.grid(row=0, column=0, padx=5, pady=5)

        self.error_txt = ttk.Label(self, text="Error", foreground="red")

    
        self.user_points = User_points_frame(self, user_id)
        self.user_points.grid(row=0, column=1, padx=5, pady=5)
        left_inc = self.user_points.get_left_inc()

        user_point_sistem = Points(user_id, left_inc)
        user_point_sistem.set_game_gole()
        user_point_sistem.montly_points()

        self.pack(fill= tk.BOTH, expand=True)

        

class Past_spendings(ttk.Frame):
    def __init__(self, nb, user_id):
        super().__init__(nb)

        self.table = Table_frame(self, user_id, "past")
        self.table.grid(row=0, column=1, columnspan=2)
        table = self.table.get_table()

        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, padx=5, pady=5)

        self.btn_input = Input_Data(frame, user_id, "past", btn_text="Add new", output_table=table)
        self.btn_input.grid(row=0, column=0)

        self.btn_edit = Edit_Data(frame, user_id, "past", table)
        self.btn_edit.grid(row=1, column=0)

        self.delete_ = Delete_Data(frame, user_id, "past", table)
        self.delete_.grid(row=2, column=0)

        self.pack(fill= tk.BOTH, expand=False)

class Plan_spendings(ttk.Frame):
    def __init__(self, nb, user_id):
        super().__init__(nb)

        self.table = Table_frame(self, user_id, "plan")
        self.table.grid(row=0, column=1, columnspan=2)
        table = self.table.get_table()

        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, padx=5, pady=5)

        self.btn_input = Input_Data(frame, user_id, "plan", btn_text="Add new", output_table=table)
        self.btn_input.grid(row=0, column=0)

        self.btn_edit = Edit_Data(frame, user_id, "plan", table)
        self.btn_edit.grid(row=1, column=0)

        self.delete_ = Delete_Data(frame, user_id, "plan", table)
        self.delete_.grid(row=2, column=0)

        self.move = Move_data(frame, user_id, "plan", table)
        self.move.grid(row=3, column=0)
        
        self.pack(fill= tk.BOTH, expand=False)

# A class for creaitikg a login window, that will be destroid after user is in
class login_screen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SFPPG")
        
        self.start()
        self.geometry("230x70")

        # self.btn_input = Input_Data_btn(self, "Input your spendings")
        # self.btn_input.pack()

    def start(self):
        fraim = ttk.Frame(self)
        fraim.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.btn_login = Log_in(fraim, "Log in", main_perent=self)
        self.btn_login.pack()
        self.btn_signin = Sign_in(fraim, "Sign in", main_perent=self)
        self.btn_signin.pack()

    def get_user_in (self):
        if self.btn_login.get_user_in() == True or self.btn_signin.get_user_in() == True:
            return True
        else:
            return False
        
    def get_user_id(self):
        if self.btn_login.get_user_id() != 0:
            return self.btn_login.get_user_id()
        elif self.btn_signin.get_user_id() != 0:
            return self.btn_signin.get_user_id()
        

class User_frame(ttk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.user_id = user_id
        self.database = db()

        txt = self.database.get_user_info(user_id)
        first_name = ttk.Label(self, text=f"First name: {txt[0]}")
        first_name.grid(row=0, column=0)
        last_name = ttk.Label(self, text=f"Last name: {txt[1]}")
        last_name.grid(row=1, column=0)
        income_txt = self.database.get_income(user_id)
        income = ttk.Label(self, text=f"Income: {income_txt[1]}")
        income.grid(row=2, column=0)

        edit_btn = Edit_User(self, user_id, "Edit", txt_1=first_name, txt_2=last_name, txt_3=income)
        edit_btn.grid(row=3, column=0)

class User_points_frame (ttk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.user_id = user_id
        self.database = db()
        
        points = self.database.get_points(user_id)
        self.user_gole_txt = ttk.Label(self, text=f"User goal: {points[1]}")
        self.user_gole_txt.grid(row=0, column=0)
        self.game_gole_txt = ttk.Label(self, text=f"Game goal: {points[2]}")
        self.game_gole_txt.grid(row=1, column=0)
        self.left_inc = self.left_income()
        self.left_inc_txt = ttk.Label(self, text=f"Left income: {self.left_inc}")
        self.left_inc_txt.grid(row=2, column=0)
        self.points_txt = ttk.Label(self, text=f"Points: {points[0]}")
        self.points_txt.grid(row=3, column=0)

        refresh_btn = ttk.Button(self, text="Refresh", command=self.refresh)
        refresh_btn.grid(row=4, column=0)

        set_goles_btn = Set_Gole(self, self.user_id, "Set Gole")
        set_goles_btn.grid(row=5, column=0)

    def refresh (self):
        points_ = Points(self.user_id, self.left_inc)
        points_.set_game_gole()
        points = self.database.get_points(self.user_id)
        self.user_gole_txt.configure(text=f"User goal: {points[1]}")
        self.game_gole_txt.configure(text=f"Game goal: {points[2]}")
        left_inc = self.left_income()
        self.left_inc_txt.configure(text=f"Left income: {left_inc}")
        self.points_txt.configure(text=f"Points: {points[0]}")

    def left_income (self):
        left_inc = self.database.get_income(self.user_id)[1]
        income_date = self.database.get_income(self.user_id)[0]
        income_date = datetime.strptime(income_date, "%d-%m-%Y")
        max_date = income_date + relativedelta(months=1)
        spendings = self.database.get_all_spendings(self.user_id)

        for spending in spendings:
            if income_date < datetime.strptime(spending[0], "%d-%m-%Y") < max_date:
                left_inc -= spending[1]
        return left_inc
    def get_left_inc (self):
        return self.left_inc
        
            
class Table_frame(ttk.Frame):
    def __init__(self, parent, user_id, tipe, colum1="Date", colum2="Price", colum3="Tipe", colum4="Description"):
        super().__init__(parent)
        self.table = ttk.Treeview(self)
        self.database = db()
        self.sort_order = {}
        
        self.table['columns'] = ("Date", colum2, colum3, colum4)

        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.column(colum1, anchor=tk.W, width=80)
        self.table.column(colum2, anchor=tk.W, width=80)
        self.table.column(colum3, anchor=tk.W, width=120)
        self.table.column(colum4, anchor=tk.W, width=180)

        self.table.heading("#0", text="", anchor=tk.W)
        self.table.heading(colum1, text=colum1, anchor=tk.W, command=lambda: self.sort_table(colum1))
        self.table.heading(colum2, text=colum2, anchor=tk.W, command=lambda: self.sort_table(colum2))
        self.table.heading(colum3, text=colum3, anchor=tk.W, command=lambda: self.sort_table(colum3))
        self.table.heading(colum4, text=colum4, anchor=tk.W)

        if tipe == "past":
            data = self.database.get_all_spendings(user_id)
        elif tipe == "plan":
            data = self.database.get_all_plans(user_id)

        for row in data:
            self.table.insert("", tk.END, values=row)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.table.yview)

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)


    def sort_table(self, column):
        if column not in self.sort_order:
            self.sort_order[column] = 'asc'

        # Check the current sorting order
        if self.sort_order[column] == 'asc':
            # Sort date in the column in ascending order
            if column == 'Date':
                dates = []
                for item in self.table.get_children(''):
                    date_str = self.table.item(item, 'values')[0]
                    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
                    dates.append((date_obj, item))

                dates.sort(key=lambda x: x[0])

                for index, (date_obj, item) in enumerate(dates):
                    self.table.move(item, '', index)
            # Sort other data in the column in ascending order
            else:
                l = [(self.table.set(k, column), k) for k in self.table.get_children('')]
                l.sort(key=lambda t: t[0])

                for index, (val, k) in enumerate(l):
                    self.table.move(k, '', index)

            self.sort_order[column] = 'desc'

        else:
            # Sort date in the column in descending order
            if column == 'Date':
                dates = []
                for item in self.table.get_children(''):
                    date_str = self.table.item(item, 'values')[0]
                    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
                    dates.append((date_obj, item))

                dates.sort(key=lambda x: x[0], reverse=True)

                for index, (date_obj, item) in enumerate(dates):
                    self.table.move(item, '', index)
            # Sort other data in the column in descending order
            else:
                l = [(self.table.set(k, column), k) for k in self.table.get_children('')]
                l.sort(key=lambda t: t[0], reverse=True)

                for index, (val, k) in enumerate(l):
                    self.table.move(k, '', index)

            self.sort_order[column] = 'asc'

    def get_table(self):
        return self.table

# A class that creates a window. It will be a peret for others classes that will make seperat window for user inputs
class Imput_Window_btn(ttk.Button):
    def __init__(self, parent, btn_text, perent2 = None , window_title = "Welcom", table = None):
        super().__init__(parent, text=btn_text, command=self.window)
        self.perent = parent
        self.window_title = window_title
        self.main_perent = perent2
        self.user_in = False
        self.user_id = 0
        self.output_table = table

        self.database = db()

    def get_user_in(self):
        return self.user_in
    
    def get_user_id(self):
        return self.user_id

    def window(self):
        self.window_ = tk.Toplevel(self.perent)
        self.window_.title(self.window_title)
        self.window_.resizable(False, False)

    # A function to check is there enithing in input text or ther is only spaises
    def check_input(self, input_txt):
        input_txt = input_txt.strip()
        if input_txt:
            return True
        else:
            return False
        
    def chech_num(self, input_txt):
        input_txt = input_txt.replace(" ", "").replace(",", "").replace(".", "")
        try:
            int(input_txt)
            return True
        except ValueError:
            return False
        
    def chech_int(self, input_txt):
        input_txt = input_txt.replace(" ", "").replace(",", ".")
        try:
            int(input_txt)
            return True
        except ValueError:
            return False
        
    def refresh_data_table(self, new_data):
        for itme in self.output_table.get_children():
            self.output_table.delete(itme)

        for i, row in enumerate(new_data):
            self.output_table.insert('', 'end', values=row)

    def chech_date(self, input_txt):
        try:
            datetime.strptime(input_txt, '%d-%m-%Y')
            return True
        except ValueError:
            return False
        

class Sign_in(Imput_Window_btn):
    def __init__(self, parent, btn_text, main_perent = None):
        super().__init__(parent, btn_text, perent2=main_perent, window_title="Sign in")

    def window(self):
        super().window()
        self.window_layout()
        
    def window_layout(self):
        ### Fraims for window
        # Frame for entering username and password
        self.frame1 = ttk.Frame(self.window_)
        self.frame1.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        lbl1 = ttk.Label(self.frame1, text="Enter your password and username")
        lbl1.grid(row=0, column=0, columnspan=2)
        # Frame for entering user info (forst_name, last_name)
        self.frame2 = ttk.Frame(self.window_)
        self.frame2.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        lbl2 = ttk.Label(self.frame2, text="Enter your First and Last name (optional)")
        lbl2.grid(row=0, column=0, columnspan=2)

        ### Username entery
        username_lbl = ttk.Label(self.frame1, text="Your username:")
        username_lbl.grid(row=1, column=0)
        self.username_ent = ttk.Entry(self.frame1)
        self.username_ent.grid(row=1, column=1)

        ### Passwor entery
        # User enters password
        pass1_lbl = ttk.Label(self.frame1, text="Your password:")
        pass1_lbl.grid(row=2, column=0)
        self.pass1_ent = ttk.Entry(self.frame1, show="*")
        self.pass1_ent.grid(row=2, column=1)
        # User agein enters a passwort to confirm it
        pass2_lbl = ttk.Label(self.frame1, text="Repeat password:")
        pass2_lbl.grid(row=3, column=0)
        self.pass2_ent = ttk.Entry(self.frame1, show="*")
        self.pass2_ent.grid(row=3, column=1)
        # Option to see the password
        self.var = tk.BooleanVar()
        show_pass = ttk.Checkbutton(self.frame1, text="Show password", variable=self.var, command=self.show_password)
        show_pass.grid(row=4, column=1)

        rueals_txt1 = ttk.Label(self.frame1, text="Usernmae have to be unique.", font=("Arial", 7))
        rueals_txt2 = ttk.Label(self.frame1, text="Repeat the password to confirm it.", font=("Arial", 7))
        rueals_txt1.grid(row=5, column=0, columnspan=2)
        rueals_txt2.grid(row=6, column=0, columnspan=2)

        ### First name entery
        firstname_lbl = ttk.Label(self.frame2, text="Your First name:")
        firstname_lbl.grid(row=1, column=0)
        self.firstname_ent = ttk.Entry(self.frame2)
        self.firstname_ent.grid(row=1, column=1)
        ### Lats name entery
        lastname_lbl = ttk.Label(self.frame2, text="Your Last name:")
        lastname_lbl.grid(row=2, column=0)
        self.lastname_ent = ttk.Entry(self.frame2)
        self.lastname_ent.grid(row=2, column=1)

        # Creating error text that will be displeid if somthing goes wrong
        self.error_txt = ttk.Label(self.window_, text="Error", foreground="red")

        ### Buttons for submiting or canceling
        cancel_btn = ttk.Button(self.window_, text="Cancel", command=self.window_.destroy)
        cancel_btn.grid(row=4, column=0, sticky="e")

        submint_btn = ttk.Button(self.window_, text="Submit", command=self.submit)
        submint_btn.grid(row=4, column=1)

    # Function that will return True if entered username does not exsist in databeis.
    def check_username(self):
        all_user = self.database.all_users()
        for user in all_user:
            if user[0] == self.username_ent.get():
                return False
            
        return True
    
    # Function that will return True if bouth passwords are the same.
    def check_password(self):
        if self.pass1_ent.get() == self.pass2_ent.get():
            return True
        return False
    
    # Function that conteins in it what will hape afeter submit button pres
    def submit(self):
        # Geting all veribals that was entered by user
        username = self.username_ent.get()
        password = self.pass1_ent.get()
        first_name = self.firstname_ent.get()
        last_name = self.lastname_ent.get()

        self.error_txt.grid_forget()

        # If/Elif staitments that check whaether user inputed important data (password, username)
        if self.check_input(username) == False or self.check_input(password) == False:
            self.error_txt.configure(text="Username or password can not be empty")
            self.error_txt.grid(row=3, column=0, columnspan=2)
        elif self.check_password() == True and self.check_username() == True:
            self.database.add_user(username, password, first_name, last_name, status="in")
            self.user_id = self.database.get_user_id(username)
            self.database.add_income(self.user_id, "1-01-2020", 0)
            self.database.add_points(self.user_id, 0, 0, None)
            self.user_in = True
            self.window_.destroy()
            self.main_perent.destroy()
        elif self.check_password() == False and self.check_username() == False:
            self.error_txt.configure(text="Passwords are not the same.\n   Username already exists.")
            self.error_txt.grid(row=3, column=0, columnspan=2)
        elif self.check_password() == False:
            self.error_txt.configure(text="Passwords are not the same.")
            self.error_txt.grid(row=3, column=0, columnspan=2)
            print('Password got wrong!')
        elif self.check_username() == False:
            self.error_txt.configure(text="Username already exists.")
            self.error_txt.grid(row=3, column=0, columnspan=2)

    # Function to toggl password visability
    def show_password(self):
        if self.var.get():
            self.pass1_ent.config(show="")
            self.pass2_ent.config(show="")
        else:
            self.pass1_ent.config(show="*")
            self.pass2_ent.config(show="*")


# A calss for log in button, tha crieits seperet window for inputs
class Log_in(Imput_Window_btn):
    def __init__(self, parent, btn_text, main_perent = None):
        super().__init__(parent, btn_text, perent2=main_perent, window_title="Log in")
        
    def window(self):
        super().window()
        self.window_layout()
        
    def window_layout(self):
        self.login_frame = ttk.Frame(self.window_)
        self.login_frame.grid(row=0, column=0, padx=5, pady=5)

        username_lbl = ttk.Label(self.login_frame, text="Username:")
        username_lbl.grid(row=0, column=0)
        self.username_ent = ttk.Entry(self.login_frame)
        self.username_ent.grid(row=0, column=1)

        pass_lbl = ttk.Label(self.login_frame, text="Password:")
        pass_lbl.grid(row=1, column=0)
        self.pass_ent = ttk.Entry(self.login_frame, show="*")
        self.pass_ent.grid(row=1, column=1)

        self.var = tk.BooleanVar()
        show_pass = ttk.Checkbutton(self.login_frame, text="Show password", variable=self.var, command=self.show_password)
        show_pass.grid(row=1, column=2)

        self.error_txt = ttk.Label(self.login_frame, text="Error!", foreground="red")

        cancel_btn = ttk.Button(self.login_frame, text="Cancel", command=self.window_.destroy)
        cancel_btn.grid(row=3, column=1)

        submint_btn = ttk.Button(self.login_frame, text="Submit", command=self.submit)
        submint_btn.grid(row=3, column=2)

    def submit(self):
        all_user = self.database.all_users()
        self.error_txt.grid_forget()

        if self.check_input(self.username_ent.get()) == True and self.check_input(self.pass_ent.get()):
            count = 0
            for user in all_user:
                if user[0] == self.username_ent.get() and user[1] == self.pass_ent.get():
                    self.user_in = True
                    self.user_id = self.database.get_user_id(self.username_ent.get())
                    self.window_.destroy()
                    self.main_perent.destroy()
                    break
                else:
                    count += 1
            if count == len(all_user):
                self.error_txt.configure(text="Wrong username or password")
                self.error_txt.grid(row=2, column=0, columnspan=3)
                print("Wrong username or password")
        else:
            self.error_txt.configure(text="Username or password can not be empty")
            self.error_txt.grid(row=2, column=0, columnspan=3)



    def show_password(self):
        if self.var.get():
            self.pass_ent.config(show="")
        else:
            self.pass_ent.config(show="*")

class Edit_User(Imput_Window_btn):
    def __init__(self, parent, user_id, btn_text, title="Editing", txt_1=None, txt_2=None, txt_3=None):
        super().__init__(parent, btn_text, window_title=title)
        self.user_id = user_id
        self.txt_1 = txt_1
        self.txt_2 = txt_2
        self.txt_3 = txt_3

    def window(self):
        super().window()
        self.window_layout()

    def window_layout (self):
        frame = ttk.Frame(self.window_)
        frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        rules_lbl = ttk.Label(frame, text="Change your user information. \nIf you don't want to change anything, leave the field blank.")
        rules_lbl.grid(row=0, column=0, columnspan=2)
        # First name entery
        firstname_lbl = ttk.Label(frame, text="First name:")
        firstname_lbl.grid(row=1, column=0)
        self.firstname_ent = ttk.Entry(frame)
        self.firstname_ent.grid(row=1, column=1)
        # Lats name entery
        lastname_lbl = ttk.Label(frame, text="Last name:")
        lastname_lbl.grid(row=2, column=0)
        self.lastname_ent = ttk.Entry(frame)
        self.lastname_ent.grid(row=2, column=1)

        # Change income
        income_lbl = ttk.Label(frame, text="Income:")
        income_lbl.grid(row=3, column=0)
        self.income_ent = ttk.Entry(frame)
        self.income_ent.grid(row=3, column=1)
        # Change income date
        income_day_lbl = ttk.Label(frame, text="Day of an incom:")
        income_day_lbl.grid(row=4, column=0)
        self.income_day_ent = ttk.Entry(frame)
        self.income_day_ent.grid(row=4, column=1)

        ## Submit and cancel buttons
        frame_2 = ttk.Frame(self.window_)
        frame_2.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.error_txt = ttk.Label(frame_2, text="Error!", foreground="red")

        cancel_btn = ttk.Button(frame_2, text="Cancel", command=self.window_.destroy)
        cancel_btn.grid(row=3, column=1)

        submint_btn = ttk.Button(frame_2, text="Submit", command=self.submit)
        submint_btn.grid(row=3, column=2)

    def submit (self):
        now = datetime.now()
        current_date = now.strftime("%m-%Y")
        full_now = now.strftime("%d-%m-%Y")
        day = self.income_day_ent.get()
        curent_income_date = day + "-" + current_date
        if self.chech_date(curent_income_date) == False and self.check_input(day) == True:
            self.error_txt.configure(text="Invalid date")
            self.error_txt.grid(row=2, column=0, columnspan=3)
        else:
            if curent_income_date > full_now:
                curent_income_date = datetime.strptime(curent_income_date, "%d-%m-%Y") + relativedelta(months=-1)
                curent_income_date = datetime.strftime(curent_income_date, "%d-%m-%Y")
            data = {"first_name": self.firstname_ent.get(),"last_name": self.lastname_ent.get(), "income": self.income_ent.get(),"incom_date": curent_income_date}
            for key, value in data.items():
                if value == "":
                    data[key] = None
                elif key == "incom_date":
                    if self.check_input(day) == False:
                        data["incom_date"] = None
                if key == "first_name":
                    self.database.change_user(self.user_id, first_name=data[key])
                elif key == "last_name":
                    self.database.change_user(self.user_id, last_name=data[key])
                elif key == "income":
                    self.database.change_income(self.user_id, income=data[key])
                elif key == "incom_date":
                    self.database.change_income(self.user_id, incom_date=data[key])

            txt = self.database.get_user_info(self.user_id)
            income_txt = self.database.get_income(self.user_id)
            self.txt_1.configure(text=f"First name: {txt[0]}")
            self.txt_2.configure(text=f"Last name: {txt[1]}")
            self.txt_3.configure(text=f"Income: {income_txt[1]}")
            self.window_.destroy()
                        


class Editing_btn(Imput_Window_btn):
    def __init__(self, parent, user_id, tipe, btn_text = "Edit", title = "Edit", output_table = None):
        super().__init__(parent, btn_text, window_title=title, table=output_table)
        self.perent = parent
        self.tipe = tipe
        self.user_id = user_id
        self.edit_data = []
        self.date = ""

    def window(self):
        super().window()
        self.window_layout()

    def window_layout(self):
        frame = ttk.Frame(self.window_)
        frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Date input label
        label_date = ttk.Label(frame, text="Enter date of a spending you want to deleat")
        label_date.grid(row=0, column=1)

        # Day, month, year labels
        label_day = ttk.Label(frame, text="Day")
        label_day.grid(row=1, column=0)

        label_month = ttk.Label(frame, text="Month")
        label_month.grid(row=1, column=1)

        label_year = ttk.Label(frame, text="Year")
        label_year.grid(row=1, column=2)

        # Day, month, year inputs 
        self.enter_day = ttk.Entry(frame)
        self.enter_day.grid(row=2, column=0)

        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.enter_month = ttk.Combobox(frame, values = months)
        self.enter_month.set("January")
        self.enter_month.grid(row=2, column=1)

        self.enter_year = tk.Spinbox(frame, from_=2020, to=2050)
        self.enter_year.grid(row=2, column=2)

        # Button for searching data with spesific date.
        search_btn = ttk.Button(frame, text="Search", command=self.search)
        search_btn.grid(row=3, column=1)

        ## Table with all date with cosen date.
        self.frame_2 = ttk.Frame(self.window_)
        self.del_table = ttk.Treeview(self.frame_2)
        
        self.del_table['columns'] = ("ID", "Date", "Price", "Tipe", "Description")

        self.del_table.column("#0", width=0, stretch=tk.NO)
        self.del_table.column("ID", anchor=tk.W, width=50)
        self.del_table.column("Date", anchor=tk.W, width=80)
        self.del_table.column("Price", anchor=tk.W, width=80)
        self.del_table.column("Tipe", anchor=tk.W, width=80)
        self.del_table.column("Description", anchor=tk.W, width=120)


        self.del_table.heading("#0", text="", anchor=tk.W)
        self.del_table.heading("ID", text="ID", anchor=tk.W)
        self.del_table.heading("Date", text="Date", anchor=tk.W)
        self.del_table.heading("Price", text="Price", anchor=tk.W)
        self.del_table.heading("Tipe", text="Tipe", anchor=tk.W)
        self.del_table.heading("Description", text="Description", anchor=tk.W)

        for row in self.edit_data:
            self.del_table.insert("", tk.END, values=row)

        scrollbar = tk.Scrollbar(self.frame_2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.del_table.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.del_table.yview)

        self.del_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.frame_2.grid(row=1, column=0, columnspan=2)

        self.error_txt = ttk.Label(self.window_, text="", foreground="red")

    def search(self):
        self.date = f"{self.enter_day.get().replace(',', '.').replace(" ", "")}-{self.monthnum(self.enter_month.get())}-{self.enter_year.get()}"
        self.error_txt.grid_forget()

        if self.chech_date( self.date) == False:
            self.error_txt.configure(text="Date is not valid.")
            self.error_txt.grid(row=3, column=0, columnspan=2)
        else:
            # select in wich table to add spending (past or plan)
            if self.tipe == "past":
                self.edit_data = self.database.get_spending(self.user_id,  self.date)
            elif self.tipe == "plan":
                self.edit_data = self.database.get_plan(self.user_id,  self.date)

            for item in self.del_table.get_children():
                self.del_table.delete(item)

            for i, row in enumerate(self.edit_data):
                self.del_table.insert('', 'end', values=row)
               
    def monthnum (self, month):
        months = {"January": '01', "February": '02', "March": '03', "April": '04', "May": '05', "June": '06', "July": '07', "August": '08', "September": '09', "October": '10', "November": '11', "December": '12'}
        return months[month]

class Delete_Data(Editing_btn):
    def __init__(self, parent, user_id, tipe, table):
        super().__init__(parent, user_id, tipe, btn_text = "Remove", title = "Removing", output_table = table)

    def window_layout(self):
        super().window_layout()
        self.frame_3 = ttk.Frame(self.window_)
        self.frame_3.grid(row=2, column=0, columnspan=2)
        
        label_id = ttk.Label(self.frame_3, text="Enter ID of a spending you want to deleat:")
        label_id.grid(row=0, column=0)

        self.enter_id = ttk.Entry(self.frame_3)
        self.enter_id.grid(row=0, column=1)

        # Buttons to finish or cancel
        cancel_btn = ttk.Button(self.window_, text="Cancel", command=self.window_.destroy)
        cancel_btn.grid(row=4, column=0)

        submint_btn = ttk.Button(self.window_, text="Delete", command=self.delete_)
        submint_btn.grid(row=4, column=1)
        
    def delete_(self):
        if self.check_input(self.enter_id.get()) == False:
            self.error_txt.configure(text="ID can not be empty.")
            self.error_txt.grid(row=3, column=0, columnspan=2)
        elif self.chech_num(self.enter_id.get()) == False and self.chech_int(self.enter_id.get()) == False:
            self.error_txt.configure(text="ID must be a whole number.")
            self.error_txt.grid(row=3, column=0, columnspan=2)
        else:
            if self.tipe == "past":
                self.database.delete_spending(int(self.enter_id.get()))
                new_data = self.database.get_all_spendings(self.user_id)
                self.refresh_data_table(new_data)
                self.window_.destroy()
            elif self.tipe == "plan":
                self.database.delete_plan(int(self.enter_id.get()))
                new_data = self.database.get_all_plans(self.user_id)
                self.refresh_data_table(new_data)
                self.window_.destroy()

class Edit_Data(Editing_btn):
    def __init__(self, parent, user_id, tipe, table):
        super().__init__(parent, user_id, tipe, btn_text = "Edit", title = "Editing", output_table = table)
        self.table = table

    def window_layout(self):
        super().window_layout()

        self.frame_3 = ttk.Frame(self.window_)
        self.frame_3.grid(row=2, column=0, columnspan=2)
        
        label_id = ttk.Label(self.frame_3, text="Enter ID of an item you want to edit:")
        label_id.grid(row=0, column=0)

        self.enter_id = ttk.Entry(self.frame_3)
        self.enter_id.grid(row=0, column=1)

        # Buttons to finish or cancel
        cancel_btn = ttk.Button(self.window_, text="Cancel", command=self.window_.destroy)
        cancel_btn.grid(row=4, column=0)

        submint_btn = ttk.Button(self.window_, text="Edit", command=self.edit_)
        submint_btn.grid(row=4, column=1)

    def edit_ (self):
        if self.check_input(self.enter_id.get()) == False:
            self.error_txt.configure(text="ID can not be empty.")
            self.error_txt.grid(row=3, column=0, columnspan=2)
        elif self.chech_num(self.enter_id.get()) == False and self.chech_int(self.enter_id.get()) == False:
            self.error_txt.configure(text="ID must be a whole number.")
            self.error_txt.grid(row=3, column=0, columnspan=2)
        else:
            if self.tipe == "past":
                self.database.delete_spending(int(self.enter_id.get()))
            elif self.tipe == "plan":
                self.database.delete_plan(int(self.enter_id.get()))
            self.window_.destroy()

            self.enter_window = Input_Data(self.perent, self.user_id, self.tipe, btn_text = "Edit", title = "Editing", output_table = self.table)
            self.enter_window.window()

class Move_data (Editing_btn):
    def __init__(self, parent, user_id, tipe, table):
        super().__init__(parent, user_id, tipe, btn_text = "Mark as Done", title = "Moving", output_table = table)

    def window_layout(self):
        super().window_layout()
        self.frame_3 = ttk.Frame(self.window_)
        self.frame_3.grid(row=2, column=0, columnspan=2)
        
        label_id = ttk.Label(self.frame_3, text="Enter ID of an item you want to mark as done:")
        label_id.grid(row=0, column=0)

        self.enter_id = ttk.Entry(self.frame_3)
        self.enter_id.grid(row=0, column=1)

        # Buttons to finish or cancel
        cancel_btn = ttk.Button(self.window_, text="Cancel", command=self.window_.destroy)
        cancel_btn.grid(row=4, column=0)

        submint_btn = ttk.Button(self.window_, text="Done", command=self.move_)
        submint_btn.grid(row=4, column=1)

    def move_ (self):
        if self.check_input(self.enter_id.get()) == False:
            self.error_txt.configure(text="ID can not be empty.")
            self.error_txt.grid(row=3, column=0, columnspan=2)
        elif self.chech_num(self.enter_id.get()) == False and self.chech_int(self.enter_id.get()) == False:
            self.error_txt.configure(text="ID must be a whole number.")
            self.error_txt.grid(row=3, column=0, columnspan=2)
        else:
            data = self.database.get_plan(self.user_id, self.date)
            print(data)
            self.database.delete_plan(int(self.enter_id.get()))
            self.database.add_spendings(self.user_id, data[0][1], data[0][2], data[0][3], data[0][4])
            new_data = self.database.get_all_plans(self.user_id)
            self.refresh_data_table(new_data)
            self.window_.destroy()

class Input_Data(Imput_Window_btn):
    def __init__(self, parent, user_id, table, btn_text = "Text", title = "Input", output_table = None):
        super().__init__(parent, btn_text, window_title=title, table=output_table)
        self.perent = parent
        self.table = table
        self.user_id = user_id

        # Variables that will be saved in CSV
        self.date = [1, 1, 2000]
        self.spend = 0
        self.tipe = ""
        self.desc = ""

    def window(self): # A function that creates a window for inputing data about spending or planing to spend
        super().window()
        self.window_leyout()

    def window_leyout(self):
        self.frame = ttk.Frame(self.window_)
        self.frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Date input label
        label_date = ttk.Label(self.frame, text="Enter date")
        label_date.grid(row=0, column=1)

        # Day, month, year labels
        label_day = ttk.Label(self.frame, text="Day")
        label_day.grid(row=1, column=0)

        label_month = ttk.Label(self.frame, text="Month")
        label_month.grid(row=1, column=1)

        label_year = ttk.Label(self.frame, text="Year")
        label_year.grid(row=1, column=2)

        # Day, month, year inputs 
        self.enter_day = ttk.Entry(self.frame)
        self.enter_day.grid(row=2, column=0)

        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.enter_month = ttk.Combobox(self.frame, values = months)
        self.enter_month.set("January")
        self.enter_month.grid(row=2, column=1)

        self.enter_year = tk.Spinbox(self.frame, from_=2020, to=2050)
        self.enter_year.grid(row=2, column=2)

        self.frame2 = tk.Frame(self.window_)
        self.frame2.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # input spend money
        label_spend = ttk.Label(self.frame2, text="Enter spend money:")
        label_spend.grid(row=1, column=0)

        self.enter_spend = ttk.Entry(self.frame2)
        self.enter_spend.grid(row=1, column=1, columnspan=2, sticky="ew")

        # input tipe
        label_tipe = ttk.Label(self.frame2, text="Enter tipe:")
        label_tipe.grid(row=2, column=0)

        self.enter_tipe = ttk.Combobox(self.frame2, values = ["Food", "Clothes", "Entertainment", "Other"])
        self.enter_tipe.set("Food")
        self.enter_tipe.grid(row=2, column=1, columnspan=2, sticky="ew")

        # input description
        label_desc = ttk.Label(self.frame2, text="Enter description")
        label_desc.grid(row=3, column=0)

        self.enter_desc = ttk.Entry(self.frame2)
        self.enter_desc.grid(row=3, column=1, columnspan=2, sticky="ew")

        self.error_txt = ttk.Label(self.window_, text="Error", foreground="red")

        # Cancel button
        btn_cancel = ttk.Button(self.window_, text="Cancel", command=self.window_.destroy)
        btn_cancel.grid(row=4, column=0, sticky="e")
        # Submit button
        btn_submit = ttk.Button(self.window_, text="Submit", command=self.submit_input)
        btn_submit.grid(row=4, column=1, sticky="w")

    def submit_input(self):
        date = f"{self.enter_day.get().replace(',', '.').replace(" ", "")}-{self.monthnum(self.enter_month.get())}-{self.enter_year.get()}"
        spend = self.enter_spend.get()
        tipe = self.enter_tipe.get()
        desc = self.enter_desc.get()

        self.error_txt.grid_forget()

        if self.check_input(self.enter_day.get()) == False or self.check_input(spend) == False:
            self.error_txt.configure(text="Date or spending can not be empty.")
            self.error_txt.grid(row=2, column=0, columnspan=2)
        elif self.chech_num(spend) == False:
            self.error_txt.configure(text="Spending must be a number.")
            self.error_txt.grid(row=2, column=0, columnspan=2)
        elif self.chech_date(date) == False:
            self.error_txt.configure(text="Date is not valid.")
            self.error_txt.grid(row=2, column=0, columnspan=2)
        else:
            spend = spend.replace(',', '.').replace(" ", "")
            # select in wich table to add spending (past or plan)
            if self.table == "past":
                self.database.add_spendings(self.user_id, date, spend, tipe, desc)
                new_data = self.database.get_all_spendings(self.user_id)
                self.refresh_data_table(new_data)
                self.window_.destroy()
            elif self.table == "plan":
                self.database.add_plan_spend(self.user_id, date, spend, tipe, desc)
                new_data = self.database.get_all_plans(self.user_id)
                self.refresh_data_table(new_data)
                points_ = self.database.get_points(self.user_id)[0]
                points_ += 5
                self.database.change_points(self.user_id, user_points=points_)
                self.window_.destroy()


    def monthnum (self, month):
        months = {"January": '01', "February": '02', "March": '03', "April": '04', "May": '05', "June": '06', "July": '07', "August": '08', "September": '09', "October": '10', "November": '11', "December": '12'}
        return months[month]
    

class Set_Gole (Imput_Window_btn):
    def __init__ (self, perent, user_id, btn_text):
        super().__init__(perent, btn_text)
        self.user_id = user_id

    def window(self):
        super().window()
        self.window_layout()

    def window_layout(self):
        farame = ttk.Frame(self.window_)
        farame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        enter_gole_lbl = ttk.Label(farame, text="Enter your Gole:")
        enter_gole_lbl.grid(row=0, column=0)
        self.enter_gole = ttk.Entry(farame)
        self.enter_gole.grid(row=0, column=1)

        self.error_txt = ttk.Label(self.window_, text="Error", foreground="red")

        btn_cancel = ttk.Button(farame, text="Cancel", command=self.window_.destroy)
        btn_cancel.grid(row=2, column=0, sticky="e")
        btn_submit = ttk.Button(farame, text="Submit", command=self.submit_input)
        btn_submit.grid(row=2, column=1, sticky="w")
        
    def submit_input(self):
        gole = self.enter_gole.get()
        self.error_txt.grid_forget()

        if self.check_input(gole) == False:
            self.error_txt.configure(text="Gole can not be empty.")
            self.error_txt.grid(row=1, column=0, columnspan=2)
        elif self.chech_num(gole) == False:
            self.error_txt.configure(text="Gole must be a number.")
            self.error_txt.grid(row=1, column=0, columnspan=2)
        else:
            gole = gole.replace(',', '.').replace(" ", "")
            self.database.change_points(self.user_id, user_gole=gole)
            self.window_.destroy()
    
class Points ():
    def __init__(self, user_id, left_inc):
        self.user_id = user_id
        self.left_inc = left_inc
        self.database = db()

        self.income = self.database.get_income(self.user_id)
        self.points = self.database.get_points(self.user_id)[0]
        self.user_gole = self.database.get_points(self.user_id)[1]
        self.game_gloe = self.database.get_points(self.user_id)[2]

    def planing_points (self):
        last_day = datetime.strptime(self.income[0], "%d-%m-%Y") + relativedelta(days=1)
        last_day = datetime.strftime(last_day, "%d-%m-%Y")
        spent_inc = self.income[1] - self.left_inc
        if spent_inc <= self.user_gole:
            self.points += 10
            self.database.change_points(self.user_id, points=self.points)
        elif spent_inc <= self.game_gloe:
            self.points += 20
            self.database.change_points(self.user_id, points=self.points)

        self.points = self.database.get_points(self.user_id)[0]


    def set_game_gole (self):
        self.game_gloe = self.user_gole * 0.7
        self.database.change_points(self.user_id, game_gole=self.game_gloe) 

    def montly_points (self):
        if self.income[0] != None or self.user_gole != None or self.user_gole >= 0:
            now = datetime.now()
            current_date = now.strftime("%d-%m-%Y")
            last_day = datetime.strptime(self.income[0], "%d-%m-%Y") + relativedelta(months=1)
            last_day = datetime.strftime(last_day, "%d-%m-%Y")
            if last_day == current_date:
                spent_inc = self.income[1] - self.left_inc
                if spent_inc <= self.user_gole:
                    self.points += 20
                    self.database.change_points(self.user_id, points=self.points)
                elif spent_inc <= self.game_gloe:
                    self.points += 30
                    self.database.change_points(self.user_id, points=self.points)

                self.points = self.database.get_points(self.user_id)[0]
                self.database.change_income(self.user_id, incom_date=last_day)
       
if __name__ == '__main__':
    main()
import sqlite3
def main ():
    test = SFPPG_Database()

    a = test.get_all_spendings(2)
    print(a)
    
    # a = test.get_all_spendings(1)
    # print(a)

    # b = test.get_all_plans(1)
    # print(b)


class SFPPG_Database:
    def __init__(self):
        self.conn = sqlite3.connect('SFPPGDatabase.db')
        self.cursor = self.conn.cursor()
        # Enabling foreign keys
        self.cursor.execute("PRAGMA foreign_keys = ON")

        # Create tables if they don't exist
        self.cursor.executescript("""--sql
            -- Creating a talbel in sql file for users
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                first_name TEXT,
                last_name TEXT,
                user_status TEXT DEFAULT "out"
            );
            -- Creating a talbel in sql file for user income          
            CREATE TABLE IF NOT EXISTS income (
                incom_user_id INTEGER PRIMARY KEY,
                incom_date TEXT DEFAULT "1-01-2000",
                income INTEGER DEFAULT 0,
                FOREIGN KEY(incom_user_id) REFERENCES user(user_id)
            );
            -- Creating a talbel in sql file for user spendings         
            CREATE TABLE IF NOT EXISTS spendings (
                spendings_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                spend_date TEXT,
                spend_price INTEGER,
                spend_tipe TEXT,
                spend_description TEXT,
                FOREIGN KEY(user_id) REFERENCES user(user_id)
            );
            -- Creating a talbel in sql file for user plans to spend
            CREATE TABLE IF Not EXISTS plans_to_spend (
                plan_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                plan_date TEXT,
                plan_price INTEGER,
                plan_tipe TEXT,
                plan_description TEXT,
                FOREIGN KEY(user_id) REFERENCES user(user_id)
            );
            -- Creating a table on sql file for user points
            CREATE TABLE IF Not EXISTS points (
                points_user_id INTEGER PRIMARY KEY,
                user_points INTEGER DEFAULT 0,
                user_gole INTEGER DEFAULT 0,
                game_gole INTEGER,
                FOREIGN KEY(points_user_id) REFERENCES user(user_id)
            )
        """)

    # Function to add new users to database
    def add_user(self, username, password, first_name, last_name, status="out"):
        self.cursor.execute("INSERT INTO user (username, password, first_name, last_name, user_status) VALUES (?, ?, ?, ?, ?)", (username, password, first_name, last_name, status))
        self.conn.commit()

    # Function to add new income of a user to database
    def add_income(self, user_id, incom_date, income):
        self.cursor.execute("INSERT INTO income (incom_user_id, incom_date, income) VALUES (?, ?, ?)", (user_id, incom_date, income))
        self.conn.commit()

    # Function to add new spendings of a user to database
    def add_spendings(self, user_id, spend_date, spend_price, spend_tipe, spend_description):
        self.cursor.execute("INSERT INTO spendings (user_id, spend_date, spend_price, spend_tipe, spend_description) VALUES (?, ?, ?, ?, ?)", (user_id, spend_date, spend_price, spend_tipe, spend_description))
        self.conn.commit()

    # Function to add new user plans to spend to database
    def add_plan_spend(self, user_id, spend_date, spend_price, spend_tipe, spend_description):
        self.cursor.execute("INSERT INTO plans_to_spend (user_id, plan_date, plan_price, plan_tipe, plan_description) VALUES (?, ?, ?, ?, ?)", (user_id, spend_date, spend_price, spend_tipe, spend_description))
        self.conn.commit()

    def add_points(self, user_id, user_points, user_gole, game_gole):
        self.cursor.execute("INSERT INTO points (points_user_id, user_points, user_gole, game_gole) VALUES (?, ?, ?, ?)", (user_id, user_points, user_gole, game_gole))
        self.conn.commit()

    # Function to show all data of tabele
    def read_all_table (self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()
    
    # Function to get all usrsnmaes and passwors that are in database
    def all_users (self):
        self.cursor.execute("SELECT username, password FROM user")
        return self.cursor.fetchall()

    # Function to change user status from out to in
    def set_user_status (self, username, status):
        self.cursor.execute("UPDATE user SET user_status = ? WHERE username = ?", (status, username))
        self.conn.commit()

    # Function to check all users status
    def check_all_user_status (self):
        self.cursor.execute("SELECT username, user_status FROM user")
        return self.cursor.fetchall()

    # Function to finde a user id from it's username
    def get_user_id (self, username):
        self.cursor.execute("SELECT user_id FROM user WHERE username = ?", (username,)) # because we input only a string, it will not work withaut an aditional coma after a veribal. withaut it, string is seperaited into digets.
        return self.cursor.fetchone()[0]
    
    def get_all_spendings (self, user_id):
        self.cursor.execute("SELECT spend_date, spend_price, spend_tipe, spend_description FROM spendings WHERE user_id = ?", (user_id,))
        all_data = self.cursor.fetchall()
        for i in range(len(all_data)):
            all_data[i] = list(all_data[i])
        return all_data
    
    def get_all_plans (self, user_id):
        self.cursor.execute("SELECT plan_date, plan_price, plan_tipe, plan_description FROM plans_to_spend WHERE user_id = ?", (user_id,))
        all_data = self.cursor.fetchall()
        for i in range(len(all_data)):
            all_data[i] = list(all_data[i])
        return all_data
    
    def get_user_info (self, user_id):
        self.cursor.execute("SELECT first_name, last_name FROM user WHERE user_id = ?", (user_id,))
        all_data = self.cursor.fetchall()
        for i in range(len(all_data)):
            all_data[i] = list(all_data[i])
        return all_data [0]
    
    def get_income (self, user_id):
        self.cursor.execute("SELECT incom_date, income FROM income WHERE incom_user_id = ?", (user_id,))
        all_data = self.cursor.fetchall()
        for i in range(len(all_data)):
            all_data[i] = list(all_data[i])
        return all_data [0]
    
    def get_points (self, user_id):
        self.cursor.execute("SELECT user_points, user_gole, game_gole FROM points WHERE points_user_id = ?", (user_id,))
        all_data = self.cursor.fetchall()
        for i in range(len(all_data)):
            all_data[i] = list(all_data[i])
        return all_data [0]
    
    def get_spending (self, user_id, spend_date):
        self.cursor.execute("SELECT spendings_id, spend_date, spend_price, spend_tipe, spend_description FROM spendings WHERE spend_date = ? AND user_id = ?", (spend_date, user_id))
        all_data = self.cursor.fetchall()
        for i in range(len(all_data)):
            all_data[i] = list(all_data[i])
        return all_data
    
    def get_plan (self, user_id, plan_date):
        self.cursor.execute("SELECT plan_id, plan_date, plan_price, plan_tipe, plan_description FROM plans_to_spend WHERE plan_date = ? AND user_id = ?", (plan_date, user_id))
        all_data = self.cursor.fetchall()
        for i in range(len(all_data)):
            all_data[i] = list(all_data[i])
        return all_data
    
    def delete_spending (self, spendings_id):
        self.cursor.execute("DELETE FROM spendings WHERE spendings_id = ?", (spendings_id,))
        self.conn.commit()

    def delete_plan (self, plan_id):
        self.cursor.execute("DELETE FROM plans_to_spend WHERE plan_id = ?", (plan_id,))
        self.conn.commit()

    def change_income (self, user_id, incom_date = None, income = None):
        if incom_date != None and income != None:
            self.cursor.execute("UPDATE income SET incom_date = ?, income = ? WHERE incom_user_id = ?", (incom_date, income, user_id))
            self.conn.commit()
        elif incom_date != None:
            self.cursor.execute("UPDATE income SET incom_date = ? WHERE incom_user_id = ?", (incom_date, user_id))
            self.conn.commit()
        elif income != None:
            self.cursor.execute("UPDATE income SET income = ? WHERE incom_user_id = ?", (income, user_id))
            self.conn.commit()

    def change_user (self, user_id, first_name = None, last_name = None):
        if first_name != None and last_name != None:
            self.cursor.execute("UPDATE user SET first_name = ?, last_name = ? WHERE user_id = ?", (first_name, last_name, user_id))
            self.conn.commit()
        elif first_name != None:
            self.cursor.execute("UPDATE user SET first_name = ? WHERE user_id = ?", (first_name, user_id))
            self.conn.commit()
        elif last_name != None:
            self.cursor.execute("UPDATE user SET last_name = ? WHERE user_id = ?", (last_name, user_id))
            self.conn.commit()

    def change_points (self, user_id, user_points = None, user_gole = None, game_gole = None):
        if user_points != None:
            self.cursor.execute("UPDATE points SET user_points = ? WHERE points_user_id = ?", (user_points, user_id))
            self.conn.commit()
        if user_gole != None:
            self.cursor.execute("UPDATE points SET user_gole = ? WHERE points_user_id = ?", (user_gole, user_id))
            self.conn.commit()
        if game_gole != None:
            self.cursor.execute("UPDATE points SET game_gole = ? WHERE points_user_id = ?", (game_gole, user_id))
            self.conn.commit()

if __name__ == "__main__":
    main()
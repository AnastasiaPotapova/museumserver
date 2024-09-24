import sqlite3


class DB:
    def __init__(self):
        conn = sqlite3.connect('news.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class PeopleModel:
    def __init__(self, connection):
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     user_name VARCHAR(50),
                                     rfid VARCHAR(50),
                                     number_events INT(100),
                                     duty INT(100)
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, rfid, user_name="none"):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, rfid, number_events, duty) 
                          VALUES (?,?,?,?)''', (user_name, rfid, 0, 0))
        cursor.close()
        self.connection.commit()

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(user_id)))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def getrfid(self, rfid):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE rfid = ?", (rfid,))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, rfid):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE rfid = ?", (rfid))
        except Exception as e:
            print(e)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def use_event(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE users
                SET number_events = number_events + 1,
                    duty = duty + 1
            WHERE id = ?;
        ''', (user_id,))
        cursor.close()
        self.connection.commit()

    def edit(self, user_id, user_name):
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE users
                SET user_name = ?
            WHERE id = ?;
        ''', (user_name, user_id))
        cursor.close()
        self.connection.commit()

    def set_duty(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE users SET duty = 0 WHERE id = ?;
        """, (user_id,))
        cursor.close()
        self.connection.commit()


class EventModel:
    def __init__(self, connection):
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS events 
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     type VARCHAR(100),
                                     date VARCHAR(100),
                                     time VARCHAR(100),
                                     user VARCHAR(100),
                                     grade VARCHAR(100),
                                     pupil_number INT(2),
                                     get_list INT(2),
                                     get_payment INT(2),
                                     comment VARCHAR(1000)
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, etype, date, time, user='', grade='',  pupil_number=0, get_list='', get_payment='', comment=''):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO events 
                          (type, date, time, user, grade,  pupil_number, get_list, get_payment, comment) 
                          VALUES (?,?,?,?,?,?,?,?,?)''', (etype, date, time, user, grade,  pupil_number, get_list, get_payment, comment))
        cursor.close()
        self.connection.commit()

    def exist(self, date, time, etype):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE date = ? and time = ? and type = ?", (date, time, etype))
        row = cursor.fetchone()
        return row

    def edit(self, id, user, grade, pupil_number, get_list, get_payment, comment):
        cursor = self.connection.cursor()
        cursor.execute('''
                    UPDATE events
                        SET user = ?, grade = ?,  pupil_number = ?, get_list = ?, get_payment = ?, comment = ?
                    WHERE id = ?;
                ''', (user, grade, pupil_number, get_list, get_payment, comment, id))
        cursor.close()
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        return rows

    def delete(self, event_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM events WHERE id = ?''', (str(event_id), ))
        cursor.close()
        self.connection.commit()

    def get(self, event_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE id = ?", (str(event_id), ))
        row = cursor.fetchone()
        return row
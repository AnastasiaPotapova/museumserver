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

    def add_column(self, name):
        cursor = self.connection.cursor()
        cursor.execute(f'''ALTER TABLE users ADD COLUMN {name} INT(100)''')
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
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(user_id), ))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id), ))
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

    def edit(self, user_id, user_name, number_events, duty):
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE users
                SET user_name = ?, number_events = ?, duty = ?
            WHERE id = ?;
        ''', (user_name, number_events, duty, user_id))
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

    def add_column(self, name):
        cursor = self.connection.cursor()
        cursor.execute(f'''ALTER TABLE events ADD COLUMN {name} INT(100)''')
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

    def get_by_date(self, event_date):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE date = ?", (str(event_date), ))
        rows = cursor.fetchall()
        return rows


class VoteModel:
    def __init__(self, connection):
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS votes
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     poll_id INT(100),
                                     is_visited INT(100),
                                     user_id INT(100),
                                     event_id INT(100),
                                     vote_id INT(100), 
                                     username VARCHAR(100)
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, poll_id, event_id, vote_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO votes 
                          (poll_id, event_id, is_visited, vote_id) 
                          VALUES (?,?,?,?)''', (poll_id, event_id, 0, vote_id))
        cursor.close()
        self.connection.commit()

    def set_user(self, user_id, username, visit_id):
        cursor = self.connection.cursor()
        cursor.execute('''
                    UPDATE votes
                        SET user_id = ?, username = ?
                    WHERE id = ?;
                ''', (str(user_id), username, str(visit_id)))
        cursor.close()
        self.connection.commit()

    def delete(self, visit_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM votes WHERE id = ?''', (str(visit_id), ))
        cursor.close()
        self.connection.commit()

    def get(self, visit_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM votes WHERE id = ?", (str(visit_id), ))
        row = cursor.fetchone()
        return row

    def get_by_user_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM votes WHERE user_id = ?", (str(user_id), ))
        rows = cursor.fetchall()
        return rows

    def get_by_event_id(self, event_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM votes WHERE event_id = ?", (str(event_id), ))
        rows = cursor.fetchall()
        return rows

    def get_vote(self, poll_id, vote_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM votes WHERE poll_id = ? and vote_id = ?", (str(poll_id), str(vote_id)))
        rows = cursor.fetchone()
        return rows

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM votes")
        rows = cursor.fetchall()
        return rows

    def set_visited(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''
                    UPDATE votes
                        SET is_visited = 1
                    WHERE id = ?;
                ''', (str(id), ))
        cursor.close()
        self.connection.commit()


class VisitModel:
    def __init__(self, connection):
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS visit
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     date VARCHAR(100),
                                     time VARCHAR(100),
                                     user_id INT(100)
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, date, time, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO visit 
                          (date, time, user_id) 
                          VALUES (?,?,?)''', (date, time, user_id))
        cursor.close()
        self.connection.commit()

    def delete(self, visit_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM visit WHERE id = ?''', (str(visit_id), ))
        cursor.close()
        self.connection.commit()

    def get(self, visit_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM visit WHERE id = ?", (str(visit_id), ))
        row = cursor.fetchone()
        return row

    def get_by_user_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM visit WHERE user_id = ?", (str(user_id), ))
        rows = cursor.fetchall()
        return rows

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM visit")
        rows = cursor.fetchall()
        return rows


db = DB()

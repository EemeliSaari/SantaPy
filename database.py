import datetime
import os
import sqlite3


class Database:

    def __init__(self, filepath):

        if not os.path.exists(filepath):
            conn = sqlite3.connect(filepath)
            self.populate(conn.cursor())
            conn.close()

        self.filepath = filepath

    def __enter__(self):

        self.conn = sqlite3.connect(self.filepath)
        self.cursor = self.conn.cursor()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        #TODO add logging if something went wrong.

        print(exc_type, exc_value, traceback)

        if not exc_type:
            self.conn.commit()

        self.conn.close()

    def populate(self, cursor = None):

        if not cursor:
            cursor = self.cursor

        cursor.execute("""CREATE TABLE IF NOT EXISTS events 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, date TEXT,
            added TEXT)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS participants 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE,
            event_id INTEGER REFERENCES events(id))""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS secrets 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, receiver TEXT, sended TEXT, 
            participant_id INTEGER REFERENCES participants(id))""")

    def add_event(self, name = None, date = None):

        self.cursor.execute("INSERT INTO events DEFAULT VALUES")
        self.cursor.execute("SELECT MAX(id) FROM events")
        added_id = self.cursor.fetchone()[0]

        if not name:
            name = 'event_{}'.format(added_id)
        if not date:
            date = ''

        self.cursor.execute("""UPDATE events SET name = ?, date = ?, added = ? 
            WHERE id = ?""", (name, date, self.now, added_id))

    def add_participants(self, event_name, *participants):

        event_id = self.id_by_name(name=event_name, table_name='events')

        content = [tuple(list(x) + [event_id]) for x in participants]
        self.cursor.executemany("""INSERT INTO participants(name, email, event_id) 
            values (?, ?, ?)""", content)

    def add_secret(self, sender, receiver):

        sender_id = self.id_by_name(name=sender, table_name='participants')

        self.cursor.execute('INSERT INTO secrets(receiver, participant_id) VALUES(?, ?)', (receiver, sender_id))

    def update_sended(self):

        now = self.now
        for receiver in self.receivers:
            self.cursor.execute("""UPDATE secrets SET sended = ? 
                WHERE receiver = ?""", (now, receiver[0]))

    def event_exists(self, name):

        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM events WHERE name = ?)", (name, ))

        return self.cursor.fetchone()

    def id_by_name(self, name, table_name):
        self.cursor.execute('SELECT id FROM {} WHERE name = ?'.format(table_name), (name, ))

        result = self.cursor.fetchall()

        if len(result) > 1:
            raise AssertionError('Received a multiple ids for participants')

        print(result)
        return result[0][0]

    def email_content(self, event_name):

        event_id = self.id_by_name(name=event_name, table_name='events')

        self.cursor.execute("""SELECT p.email, s.receiver FROM participants AS p 
            INNER JOIN secrets as s ON p.id = s.participant_id WHERE p.event_id = ?""", (event_id,))

        return self.cursor.fetchall()

    @property
    def receivers(self):
        self.cursor.execute("SELECT receiver FROM secrets")

        return self.cursor.fetchall()

    @property
    def now(self):

        return datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

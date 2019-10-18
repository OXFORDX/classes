import sqlite3
import os


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        # cursor.execute("""CREATE TABLE students(
        #             id integer,
        #             firstname text,
        #             lastname text,
        #             age integer,
        #             faculty text,
        #             groups text,
        #             course integer,
        #             pay integer )""")
        #

    def __del__(self):
        self.connection.close()

    def add_std(self):
        firstname = str(input('FName: '))
        lastname = str(input('LName: '))
        age = int(input('Age: '))
        faculty = str(input('Faculty: '))
        groups = str(input('Group: '))
        course = int(input('Course: '))
        pay = int(input('Pay: '))
        with self.connection:
            self.cursor.execute(
                "INSERT INTO students VALUES (:id, :firstname, :lastname, :age, :faculty, :groups, :course, :pay)",
                {
                    'id': self.__getLastID(),
                    'firstname': firstname,
                    'lastname': lastname,
                    'age': age,
                    'faculty': faculty,
                    'groups': groups,
                    'course': course,
                    'pay': pay
                })
        self.connection.commit()

    def __read_db(self):
        self.cursor.execute("SELECT * FROM students WHERE id=:id", {'id': 1})
        return self.cursor.fetchall()

    def __getLastID(self):
        last_id = 0
        for i in self.__read_db():
            last_id = i['id']
        return last_id + 1


db = Database()
db.add_std()

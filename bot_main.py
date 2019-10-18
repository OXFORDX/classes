import sqlite3
import os


class Database:
    def __init__(self, flname):
        rand = flname.split(' ')
        self.fname = rand[0]
        self.lname = rand[1]
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
        self.cursor.execute(f"""CREATE TABLE std{self.__getLastID()}(
            subject text,
            mark integer
        )""")
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

    def add_marks(self, array):
        with self.connection:
            self.cursor.execute(f"""INSERT INTO std{self.read_id} VALUES (:subject, :mark)""",
                                {'subject': 'Математика', 'mark': 0})

    def read_id(self):
        self.cursor.execute(f"""SELECT * FROM students WHERE firstname=:firstname AND lastname=:lastname""",
                            {'firstname': self.fname, 'lastname': self.lname})
        obj = self.cursor.fetchone()
        return obj['id']

    def read_db(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def __getLastID(self):
        last_id = 0
        for i in self.read_db():
            last_id = i['id']
        return last_id + 1


subj = ['Математика', 'КПЗ', 'Психологія', 'Філософія', 'Веб-програмування']
db = Database('Бебех Олександр')
db.add_marks(subj)

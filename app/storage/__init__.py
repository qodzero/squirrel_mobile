import sqlite3
import hashlib
import os

class Database(object):
    def __init__(self, **kw):
        super().__init__(**kw)

        if not os.path.exists('app/storage/db.sqlite'):
            conn = sqlite3.connect('app/storage/db.sqlite')
            cur = conn.cursor()

            card = '''
                CREATE TABLE cards(
                id integer primary key,
                name text not null,
                type text not null,
                exp text not null,
                balance text not null
                )
            '''
            expenses = '''
                CREATE TABLE expenses(
                id integer primary key,
                card text not null,
                card_num text not null,
                expense_name text not null,
                cost text null,
                paid text not null,
                recurring text not null,
                day_paid text not null,
                expense text not null
                )
            '''

            for sql in [card, expenses]:
                try:
                    cur.execute(sql)
                    conn.commit()
                except Exception as e:
                    print(e)
            conn.close()

    def db_connect(self):
        conn = sqlite3.connect('app/storage/db.sqlite')

        return conn

    def get_cards(self):
        conn = self.db_connect()
        cur = conn.cursor()

        sql = '''SELECT * FROM cards'''

        try:
            cur.execute(sql)
            conn.commit()
            data = cur.fetchall()
            return data
        except Exception as e:
            print(e)
            return []

    def get_expenses(self):
        conn = self.db_connect()
        cur = conn.cursor()

        sql = '''SELECT * FROM expenses'''

        try:
            cur.execute(sql)
            conn.commit()
            data = cur.fetchall()
            return data
        except Exception as e:
            print(e)
            return []

    def delete_card(self, cid: int):
        conn = self.db_connect()
        cur = conn.cursor()

        sql = '''
            DELETE FROM cards
            WHERE id=?
        '''
        try:
            cur.execute(sql, [cid])
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_expense(self, eid: int):
        conn = self.db_connect()
        cur = conn.cursor()

        sql = '''
            DELETE FROM expenses
            WHERE id=?
        '''
        try:
            cur.execute(sql, [eid])
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def add_card(self, card: tuple):
        conn = self.db_connect()
        cur = conn.cursor()

        sql = '''
            INSERT INTO cards(
            name,
            type,
            exp,
            balance
            )
            VALUES(?,?,?,?)
        '''

        try:
            cur.execute(sql, card)
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            print(e)
            return -1

    def add_expense(self, expense: tuple):
        conn = self.db_connect()
        cur = conn.cursor()

        sql = '''
            INSERT INTO expenses(
            card,
            card_num,
            expense_name,
            cost,
            paid,
            recurring,
            day_paid,
            expense
            )
            VALUES(?,?,?,?,?,?,?,?)
        '''

        try:
            cur.execute(sql, expense)
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            print(e)
            return -1

    def update_card(self, card: tuple):
        conn = self.db_connect()
        cur = conn.cursor()
        print(card[1])
        sql = '''
            UPDATE cards
            SET balance=?
            WHERE id=?
        '''

        try:
            cur.execute(sql, card)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

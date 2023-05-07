import sqlite3 as sq


def insert_id(id):
    connect = sq.connect("users_db")
    cursor = connect.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users(
        user_id TEXT
    )"""
    )
    connect.commit()
    user = [id]
    cursor.execute("INSERT INTO users VALUES(?);", user)
    connect.commit()


# db = sq.connect("users_db")
# sq1 = db.cursor()
# for i in sq1.execute("SELECT * FROM users"):
#     print(i)
#
# db.close()

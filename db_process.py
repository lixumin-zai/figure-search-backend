import sqlite3
from exception import UserAlreadyExistsError


# class Database:
#     def __init__(self, db_name):
#         self.conn = sqlite3.connect(db_name)
#         self.cursor = self.conn.cursor()
#         self.create_table()

#     def create_table(self):
#         self.cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY,
#             wechat_id TEXT NOT NULL UNIQUE,
#             phone_number TEXT NOT NULL UNIQUE,
#             verification_code TEXT NOT NULL UNIQUE,
#             usage_count INTEGER NOT NULL DEFAULT 30
#         )
#         ''')
#         self.conn.commit()

#     def create_user(self, wechat_id, phone_number, verification_code):
#         self.cursor.execute('SELECT * FROM users WHERE wechat_id = ? OR phone_number = ? OR verification_code = ?', 
#                         (wechat_id, phone_number, verification_code))
#         if self.cursor.fetchone() is not None:
#             raise UserAlreadyExistsError("该用户已存在")

#         self.cursor.execute('INSERT INTO users (wechat_id, phone_number, verification_code) VALUES (?, ?, ?)', (wechat_id, phone_number, verification_code))
#         self.conn.commit()

#     def get_users(self):
#         self.cursor.execute('SELECT * FROM users')
#         return self.cursor.fetchall()

#     def get_user_info_by_wechat_id(self, wechat_id):
#         self.cursor.execute('SELECT * FROM users WHERE wechat_id = ?', (wechat_id,))
#         return self.cursor.fetchone()

#     def get_user_info_by_phone_number(self, phone_number):
#         self.cursor.execute('SELECT * FROM users WHERE phone_number = ?', (phone_number,))
#         return self.cursor.fetchone()  # 返回匹配的用户信息

#     def get_user_info_by_verification_code(self, verification_code):
#         self.cursor.execute('SELECT * FROM users WHERE verification_code = ?', (verification_code,))
#         return self.cursor.fetchone()  # 返回匹配的用户信息

#     def update_user_wechat_id_by_phone_number(self, wechat_id, phone_number):
#         self.cursor.execute('UPDATE users SET wechat_id = ? WHERE phone_number = ?', (wechat_id, phone_number))
#         self.conn.commit()

#     def reduce_usage_count(self, verification_code):
#         self.cursor.execute('SELECT usage_count FROM users WHERE verification_code = ?', (verification_code,))
#         current_count = self.cursor.fetchone()
#         # print(current_count)
#         if current_count and current_count[0] > 0:
#             self.cursor.execute('UPDATE users SET usage_count = usage_count - 1 WHERE verification_code = ?', (verification_code,))
#             self.conn.commit()
#         return current_count[0] - 1
    
#     def increase_usage_count(self, verification_code, number):
#         self.cursor.execute('SELECT usage_count FROM users WHERE verification_code = ?', (verification_code,))
#         current_count = self.cursor.fetchone()
        
#         if current_count is not None:
#             new_count = current_count[0] + number
#             self.cursor.execute('UPDATE users SET usage_count = ? WHERE verification_code = ?', (new_count, verification_code))
#             self.conn.commit()

#     def close(self):
#         self.cursor.close()
#         self.conn.close()

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            wechat_id TEXT NOT NULL UNIQUE,
            verification_code TEXT NOT NULL UNIQUE,
            usage_count INTEGER NOT NULL DEFAULT 15,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()

    def create_user(self, wechat_id, verification_code):
        self.cursor.execute('SELECT * FROM users WHERE wechat_id = ? OR verification_code = ?', 
                        (wechat_id, verification_code))
        if self.cursor.fetchone() is not None:
            raise UserAlreadyExistsError("该用户已存在")

        self.cursor.execute('INSERT INTO users (wechat_id, verification_code) VALUES (?, ?)', (wechat_id, verification_code))
        self.conn.commit()

    def get_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def get_user_info_by_wechat_id(self, wechat_id):
        self.cursor.execute('SELECT * FROM users WHERE wechat_id = ?', (wechat_id,))
        return self.cursor.fetchone()

    def get_user_info_by_verification_code(self, verification_code):
        self.cursor.execute('SELECT * FROM users WHERE verification_code = ?', (verification_code,))
        return self.cursor.fetchone()  # 返回匹配的用户信息

    def reduce_usage_count(self, verification_code):
        self.cursor.execute('SELECT usage_count FROM users WHERE verification_code = ?', (verification_code,))
        current_count = self.cursor.fetchone()
        # print(current_count)
        if current_count and current_count[0] > 0:
            self.cursor.execute('UPDATE users SET usage_count = usage_count - 1 WHERE verification_code = ?', (verification_code,))
            self.conn.commit()
        return current_count[0] - 1
    
    def increase_usage_count(self, verification_code, number):
        self.cursor.execute('SELECT usage_count FROM users WHERE verification_code = ?', (verification_code,))
        current_count = self.cursor.fetchone()
        
        if current_count is not None:
            new_count = current_count[0] + number
            self.cursor.execute('UPDATE users SET usage_count = ? WHERE verification_code = ?', (new_count, verification_code))
            self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    import uuid
    db = Database('db/test_0928.db')
    db.create_user('Daring1918', str(uuid.uuid4()))
    # db.increase_usage_count("1479bd3e-6343-4ae1-97d5-90e386655118", 1)

    for i in db.get_users():
        print(i)
    import uuid
    # db.create_user('xrkuma', "bini")
    
    # # 查询用户信息
    db.close()



######. 跟新字段默认值
# db.cursor.execute('ALTER TABLE users RENAME TO old_users;')
# db.conn.commit()
# db.cursor.execute('''CREATE TABLE users (
#     id INTEGER PRIMARY KEY,
#     wechat_id TEXT NOT NULL UNIQUE,
#     verification_code TEXT NOT NULL UNIQUE,
#     usage_count INTEGER NOT NULL DEFAULT 15,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
# );''')
# db.conn.commit()

# db.cursor.execute("""INSERT INTO users (id, wechat_id, verification_code, usage_count, created_at)
#     SELECT id, wechat_id, verification_code, usage_count, created_at FROM old_users;""")
# db.conn.commit()
####
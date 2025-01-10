import sqlite3
from exception import UserAlreadyExistsError
import uuid
from datetime import datetime

# class Database2:
#     def __init__(self, db_name):
#         self.conn = sqlite3.connect(db_name)
#         self.cursor = self.conn.cursor()
#         self.create_table()

#     def create_table(self):
#         self.cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY,
#             wechat_id TEXT NOT NULL UNIQUE,
#             verification_code TEXT NOT NULL UNIQUE,
#             usage_count INTEGER NOT NULL DEFAULT 10,
#             invitation_code TEXT UNIQUE, 
#             created_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
        """
        创建用户
        """
        self.cursor.execute('SELECT * FROM users WHERE wechat_id = ? OR verification_code = ?', 
                        (wechat_id, verification_code))
        if self.cursor.fetchone() is not None:
            raise UserAlreadyExistsError("该用户已存在")

        self.cursor.execute('INSERT INTO users (wechat_id, verification_code) VALUES (?, ?)', (wechat_id, verification_code))
        self.conn.commit()

    def get_users(self):
        """
        查看所有用户信息
        """
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def get_user_info_by_wechat_id(self, wechat_id):
        """
        通过wechat_id搜索用户
        """
        self.cursor.execute('SELECT * FROM users WHERE wechat_id = ?', (wechat_id,))
        return self.cursor.fetchone()

    def get_user_info_by_verification_code(self, verification_code):
        """
        通过verification_code 执行码搜索用户
        """
        self.cursor.execute('SELECT * FROM users WHERE verification_code = ?', (verification_code,))
        return self.cursor.fetchone()  # 返回匹配的用户信息

    def reduce_usage_count(self, verification_code):
        """
        通过verification_code 执行码减少用户使用次数 1
        """
        self.cursor.execute('SELECT usage_count FROM users WHERE verification_code = ?', (verification_code,))
        current_count = self.cursor.fetchone()
        # print(current_count)
        if current_count and current_count[0] > 0:
            self.cursor.execute('UPDATE users SET usage_count = usage_count - 1 WHERE verification_code = ?', (verification_code,))
            self.conn.commit()
        return current_count[0] - 1
    
    def increase_usage_count(self, verification_code, number):
        """
        通过verification_code 执行码增加用户使用次数 
        """
        self.cursor.execute('SELECT usage_count FROM users WHERE verification_code = ?', (verification_code,))
        current_count = self.cursor.fetchone()
        
        if current_count is not None:
            new_count = current_count[0] + number
            self.cursor.execute('UPDATE users SET usage_count = ? WHERE verification_code = ?', (new_count, verification_code))
            self.conn.commit()

    def increase_usage_count_by_verification_code(self, verification_code, number):
        """
        通过verification_code 执行码增加用户使用次数 
        """
        self.cursor.execute('UPDATE users SET usage_count = usage_count + ? WHERE verification_code = ?', (number, verification_code))
        self.conn.commit()

    def delete_user(self, wechat_id):
        """
        删除用户
        """
        self.cursor.execute("DELETE FROM users WHERE wechat_id = ?", (wechat_id,))
        self.conn.commit()

    def close(self):
        """
        关闭数据库
        """
        self.cursor.close()
        self.conn.close()



class RechargeCodeDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS rechargeCode (
            id INTEGER PRIMARY KEY,
            recharge_code TEXT NOT NULL UNIQUE,
            used_code TEXT,
            usage_count INTEGER NOT NULL DEFAULT 100
        )
        ''')
        self.conn.commit()

    def create_code(self):
        recharge_code = str(uuid.uuid4())
        self.cursor.execute('SELECT * FROM rechargeCode WHERE recharge_code = ?', 
                        (recharge_code, ))
        if self.cursor.fetchone() is not None:
            raise UserAlreadyExistsError("该用户已存在")

        self.cursor.execute('INSERT INTO rechargeCode (recharge_code) VALUES (?)', (recharge_code, ))
        self.conn.commit()
        return recharge_code

    def get_infos(self):
        self.cursor.execute('SELECT * FROM rechargeCode')
        return self.cursor.fetchall()

    def get_info_by_recharge_code(self, recharge_code):
        self.cursor.execute('SELECT * FROM rechargeCode WHERE recharge_code = ?', (recharge_code,))
        return self.cursor.fetchone()

    def get_info_by_used_code(self, used_code):
        self.cursor.execute('SELECT * FROM rechargeCode WHERE used_code = ?', (used_code,))
        return self.cursor.fetchone()  # 返回匹配的用户信息

    def used_code(self, recharge_code, used_code):
        info = self.get_info_by_recharge_code(recharge_code)
        cost_time = 0
        if info:
            cost_time = info[3]
        self.cursor.execute('UPDATE rechargeCode SET used_code = ?,usage_count = 0 WHERE recharge_code = ?', (used_code, recharge_code, ))
        self.conn.commit()
        return cost_time

    def close(self):
        self.cursor.close()
        self.conn.close()



class AdViewsDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS AdViews (
            id INTEGER PRIMARY KEY,
            verification_code TEXT NOT NULL,
            view_date DATE NOT NULL,
            view_count INTEGER DEFAULT 0
        )
        ''')
        self.conn.commit()

    def create_view_info(self, verification_code):
        today = datetime.now().date()
        self.cursor.execute('SELECT * FROM AdViews WHERE verification_code = ? AND view_date = ?', 
                        (verification_code, today))
        if self.cursor.fetchone() is not None:
            return
        else:
            self.cursor.execute('INSERT INTO AdViews (verification_code, view_date) VALUES (?, ?)', (verification_code, today))
            self.conn.commit()

    def get_all_infos(self):
        self.cursor.execute("SELECT * FROM AdViews")
        return self.cursor.fetchall()

    def get_info_by_verification_code(self, verification_code):
        self.cursor.execute('''SELECT * FROM AdViews WHERE verification_code = ?''', (verification_code,))
        return self.cursor.fetchall()

    def get_info_by_verification_code_on_today(self, verification_code):
        self.cursor.execute('''SELECT * FROM AdViews WHERE verification_code = ? AND view_date = ?''', (verification_code, datetime.now().date()))
        return self.cursor.fetchone()
    
    def watch_one_today(self, verification_code):
        today = datetime.now().date()
        info = self.get_info_by_verification_code_on_today(verification_code)

        if info:
            self.cursor.execute('UPDATE AdViews SET view_count = view_count + 1 WHERE verification_code = ? AND view_date = ?', (verification_code,today))
            self.conn.commit()
            return info[3] + 1
        else:
            self.create_view_info(verification_code)
            self.cursor.execute('UPDATE AdViews SET view_count = view_count + 1 WHERE verification_code = ? AND view_date = ?', (verification_code,today))
            self.conn.commit()
            return 1



    def get_info_by_verification_code_on_chosse_today(self, recharge_code, used_code):
        pass

    def close(self):
        self.cursor.close()
        self.conn.close()



if __name__ == "__main__":
    import uuid
    # db = Database2('db/user.db')

    # conn = sqlite3.connect('db/test_0928 copy.db')
    # cursor = conn.cursor()
    
    # cursor.execute("DROP TABLE IF EXISTS AdViews")

    # db = AdViewsDB('db/test_0928.db')
    db = Database('db/test_0928.db')
    # db.create_view_info("lixumin")
    # db.watch_one_today("9f2734c4-4d35-4bb5-9a83-2097d230830d")
    # for i in db.get_all_infos():
    #     print(i)

    # for i in db.get_users():
    #     print(i)
    


    rechargecode_db = RechargeCodeDB("db/rechargecode.db")
    for i in rechargecode_db.get_infos():
        print(i)
    # rechargecode_db.create_code()
    # print(rechargecode_db.get_info_by_recharge_code("5b475e97-bfea-4d7d-bd50-b37d7cbe3549"))
    # print(db2.get_users())
    # print(db.get_user_info_by_verification_code("2359210977"))
    # for i in db2.get_users():
    #     # if i[1] == "cz71227669889":
    #     print(i)
    # import uuid
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
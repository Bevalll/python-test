import json
import hashlib
import os
from datetime import datetime


class UserManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.users = self.load_users()

    def load_users(self):
        """加载用户数据"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载用户数据失败: {e}")
                return {}
        return {}

    def save_users(self):
        """保存用户数据"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存用户数据失败: {e}")
            return False

    def hash_password(self, password):
        """密码加密"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        """用户注册"""
        if not username or not password:
            return False, "用户名和密码不能为空"

        if username in self.users:
            return False, "用户名已存在"

        if len(username) < 3 or len(username) > 20:
            return False, "用户名长度应在3-20个字符之间"

        if len(password) < 6:
            return False, "密码长度至少6位"

        # 注册新用户
        self.users[username] = {
            'password': self.hash_password(password),
            'online': False,
            'register_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_login': None
        }

        if self.save_users():
            return True, "注册成功"
        else:
            return False, "注册失败，请重试"

    def login(self, username, password):
        """用户登录"""
        if not username or not password:
            return False, "用户名和密码不能为空"

        if username not in self.users:
            return False, "用户不存在"

        if self.users[username]['password'] != self.hash_password(password):
            return False, "密码错误"

        if self.users[username]['online']:
            return False, "用户已在线，不能重复登录"

        # 更新用户状态
        self.users[username]['online'] = True
        self.users[username]['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_users()

        return True, "登录成功"

    def logout(self, username):
        """用户登出"""
        if username in self.users:
            self.users[username]['online'] = False
            self.save_users()
            return True
        return False

    def force_logout(self, username):
        """强制用户下线（用于清理异常状态）"""
        if username in self.users:
            self.users[username]['online'] = False
            self.save_users()
            return True
        return False

    def is_online(self, username):
        """检查用户是否在线"""
        return username in self.users and self.users[username].get('online', False)

    def get_online_users(self):
        """获取在线用户列表"""
        return [username for username, info in self.users.items() if info.get('online', False)]

    def get_all_users(self):
        """获取所有用户"""
        return list(self.users.keys())

    def user_exists(self, username):
        """检查用户是否存在"""
        return username in self.users

    def delete_user(self, username):
        """删除用户"""
        if username in self.users:
            del self.users[username]
            return self.save_users()
        return False
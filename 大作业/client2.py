import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import threading
import json
import time
import os


class ChatClient:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.username = None

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("Python聊天室 - 用户登录")
        self.root.geometry("400x300")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_login_window()

    def create_login_window(self):
        """创建登录窗口"""
        # 清除现有内容
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Python聊天室 - 用户登录")
        self.root.geometry("400x300")

        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = ttk.Label(main_frame, text="Python聊天室",
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # 用户名输入
        username_frame = ttk.Frame(main_frame)
        username_frame.pack(fill=tk.X, pady=10)

        ttk.Label(username_frame, text="用户名:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.username_entry = ttk.Entry(username_frame, font=("Arial", 10))
        self.username_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        # 密码输入
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=10)

        ttk.Label(password_frame, text="密码:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.password_entry = ttk.Entry(password_frame, font=("Arial", 10), show="*")
        self.password_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        # 服务器地址
        server_frame = ttk.Frame(main_frame)
        server_frame.pack(fill=tk.X, pady=10)

        ttk.Label(server_frame, text="服务器:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.server_entry = ttk.Entry(server_frame, font=("Arial", 10))
        self.server_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.server_entry.insert(0, "localhost:8888")

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="登录",
                   command=self.login,
                   width=15).pack(pady=5)

        ttk.Button(button_frame, text="注册",
                   command=self.register,
                   width=15).pack(pady=5)

        ttk.Button(button_frame, text="退出",
                   command=self.root.quit,
                   width=15).pack(pady=5)

        # 状态栏
        self.status_label = ttk.Label(main_frame, text="请输入用户名和密码",
                                      foreground="gray", font=("Arial", 9))
        self.status_label.pack(side=tk.BOTTOM, pady=10)

        # 绑定回车键
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())

        # 设置焦点
        self.username_entry.focus()

    def connect_to_server(self):
        """连接到服务器"""
        try:
            server_info = self.server_entry.get().strip()

            if ':' in server_info:
                host, port = server_info.split(':')
                port = int(port)
            else:
                host = server_info
                port = 8888

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((host, port))
            self.socket.settimeout(None)

            self.connected = True

            # 启动消息接收线程
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            return True

        except Exception as e:
            self.status_label.config(text=f"连接失败: {e}", foreground="red")
            return False

    def login(self):
        """用户登录"""
        if self.connected:
            return

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("输入错误", "请输入用户名和密码")
            return

        self.status_label.config(text="正在连接服务器...", foreground="blue")
        self.root.update()

        if not self.connect_to_server():
            return

        # 发送登录信息
        login_data = {
            'type': 'login',
            'username': username,
            'password': password,
            'timestamp': time.time()
        }

        try:
            self.socket.send(json.dumps(login_data).encode('utf-8'))
            self.username = username
        except Exception as e:
            self.status_label.config(text=f"登录失败: {e}", foreground="red")
            self.connected = False

    def register(self):
        """用户注册"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("输入错误", "请输入用户名和密码")
            return

        self.status_label.config(text="正在连接服务器...", foreground="blue")
        self.root.update()

        if not self.connect_to_server():
            return

        # 发送注册信息
        register_data = {
            'type': 'register',
            'username': username,
            'password': password,
            'timestamp': time.time()
        }

        try:
            self.socket.send(json.dumps(register_data).encode('utf-8'))
        except Exception as e:
            self.status_label.config(text=f"注册失败: {e}", foreground="red")
            self.connected = False

    def create_chat_window(self):
        """创建聊天窗口"""
        # 清除现有内容
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f"Python聊天室 - {self.username}")
        self.root.geometry("800x600")

        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 顶部状态栏
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(status_frame, text=f"欢迎, {self.username}",
                  font=("Arial", 11, "bold")).pack(side=tk.LEFT)

        self.connection_status = ttk.Label(status_frame, text="● 在线",
                                           foreground="green", font=("Arial", 9))
        self.connection_status.pack(side=tk.RIGHT)

        # 内容区域
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧用户列表
        user_frame = ttk.LabelFrame(content_frame, text="在线用户")
        user_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.user_listbox = tk.Listbox(user_frame, width=20, font=("Arial", 10))
        self.user_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 右侧聊天区域
        chat_frame = ttk.LabelFrame(content_frame, text="聊天内容")
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.chat_text = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Arial", 10)
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 配置标签样式
        self.chat_text.tag_config("system", foreground="blue", font=("Arial", 9, "italic"))
        self.chat_text.tag_config("message", foreground="black")
        self.chat_text.tag_config("my_message", foreground="green")

        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(10, 0))

        self.message_entry = ttk.Entry(input_frame, font=("Arial", 10))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind('<Return>', lambda e: self.send_message())

        ttk.Button(input_frame, text="发送",
                   command=self.send_message).pack(side=tk.RIGHT)

        # 底部按钮
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=10)

        ttk.Button(bottom_frame, text="刷新用户列表",
                   command=self.refresh_user_list).pack(side=tk.LEFT)

        ttk.Button(bottom_frame, text="清空聊天",
                   command=self.clear_chat).pack(side=tk.LEFT, padx=5)

        ttk.Button(bottom_frame, text="退出登录",
                   command=self.logout).pack(side=tk.RIGHT)

        # 设置焦点
        self.message_entry.focus()

        # 显示欢迎消息
        self.display_system_message("登录成功！开始聊天吧！")

    def send_message(self):
        """发送消息"""
        if not self.connected:
            messagebox.showwarning("发送失败", "未连接到服务器")
            return

        message = self.message_entry.get().strip()
        if not message:
            return

        try:
            # 发送消息
            message_data = {
                'type': 'message',
                'username': self.username,
                'content': message,
                'timestamp': time.time()
            }
            self.socket.send(json.dumps(message_data).encode('utf-8'))

            # 在聊天框显示自己的消息
            self.display_my_message(message)

            # 清空输入框
            self.message_entry.delete(0, tk.END)

        except Exception as e:
            self.display_system_message(f"发送失败: {e}")
            self.connected = False
            self.connection_status.config(text="● 离线", foreground="red")

    def receive_messages(self):
        """接收服务器消息"""
        while self.connected:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8')
                self.process_message(message)

            except Exception as e:
                if self.connected:
                    print(f"接收消息错误: {e}")
                break

        # 连接断开
        if self.connected:
            self.disconnect()

    def process_message(self, message):
        """处理接收到的消息"""
        try:
            data = json.loads(message)
            msg_type = data.get('type')

            if msg_type == 'register_response':
                self.handle_register_response(data)
            elif msg_type == 'login_response':
                self.handle_login_response(data)
            elif msg_type == 'system_message':
                self.display_system_message(data.get('content', ''))
            elif msg_type == 'chat_message':
                username = data.get('username', '')
                content = data.get('content', '')
                if username != self.username:  # 不显示自己的消息
                    self.display_message(username, content)
            elif msg_type == 'user_list':
                self.handle_user_list(data)
            elif msg_type == 'error':
                self.display_system_message(f"错误: {data.get('message', '')}")

        except json.JSONDecodeError:
            # 如果不是JSON，直接显示
            self.display_system_message(message)

    def handle_register_response(self, data):
        """处理注册响应"""
        success = data.get('success', False)
        message = data.get('message', '')

        if success:
            self.status_label.config(text="注册成功！", foreground="green")
            messagebox.showinfo("注册成功", "注册成功！请点击登录")
        else:
            self.status_label.config(text=f"注册失败: {message}", foreground="red")
            messagebox.showerror("注册失败", message)

        self.disconnect()

    def handle_login_response(self, data):
        """处理登录响应"""
        success = data.get('success', False)
        message = data.get('message', '')

        if success:
            self.status_label.config(text="登录成功！", foreground="green")
            self.root.after(100, self.create_chat_window)
        else:
            self.status_label.config(text=f"登录失败: {message}", foreground="red")
            messagebox.showerror("登录失败", message)
            self.disconnect()

    def handle_user_list(self, data):
        """处理用户列表"""
        users = data.get('users', [])
        if hasattr(self, 'user_listbox'):
            self.user_listbox.delete(0, tk.END)
            for user in users:
                if user != self.username:  # 不显示自己
                    self.user_listbox.insert(tk.END, user)

    def display_system_message(self, message):
        """显示系统消息"""
        if hasattr(self, 'chat_text'):
            timestamp = time.strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] 系统: {message}\n"

            self.chat_text.config(state=tk.NORMAL)
            self.chat_text.insert(tk.END, formatted_message, "system")
            self.chat_text.config(state=tk.DISABLED)
            self.chat_text.see(tk.END)

    def display_message(self, username, message):
        """显示其他用户的消息"""
        if hasattr(self, 'chat_text'):
            timestamp = time.strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {username}: {message}\n"

            self.chat_text.config(state=tk.NORMAL)
            self.chat_text.insert(tk.END, formatted_message, "message")
            self.chat_text.config(state=tk.DISABLED)
            self.chat_text.see(tk.END)

    def display_my_message(self, message):
        """显示自己的消息"""
        if hasattr(self, 'chat_text'):
            timestamp = time.strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] 我: {message}\n"

            self.chat_text.config(state=tk.NORMAL)
            self.chat_text.insert(tk.END, formatted_message, "my_message")
            self.chat_text.config(state=tk.DISABLED)
            self.chat_text.see(tk.END)

    def refresh_user_list(self):
        """刷新用户列表"""
        if self.connected:
            user_list_request = {
                'type': 'get_user_list',
                'username': self.username,
                'timestamp': time.time()
            }
            try:
                self.socket.send(json.dumps(user_list_request).encode('utf-8'))
            except:
                pass

    def clear_chat(self):
        """清空聊天记录"""
        if hasattr(self, 'chat_text'):
            self.chat_text.config(state=tk.NORMAL)
            self.chat_text.delete(1.0, tk.END)
            self.chat_text.config(state=tk.DISABLED)

    def logout(self):
        """退出登录"""
        if self.connected and self.username:
            logout_data = {
                'type': 'logout',
                'username': self.username,
                'timestamp': time.time()
            }
            try:
                self.socket.send(json.dumps(logout_data).encode('utf-8'))
            except:
                pass

        self.disconnect()
        self.create_login_window()

    def disconnect(self):
        """断开连接"""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

        if hasattr(self, 'connection_status'):
            self.connection_status.config(text="● 离线", foreground="red")

    def on_closing(self):
        """窗口关闭事件"""
        if self.connected and self.username:
            self.logout()
        self.root.quit()

    def run(self):
        """运行客户端"""
        self.root.mainloop()


if __name__ == "__main__":
    print("正在启动聊天客户端...")
    client = ChatClient()
    client.run()
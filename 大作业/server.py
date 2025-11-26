import socket
import threading
import json
import time
import os
from user_manager import UserManager


class ChatServer:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8888
        self.clients = {}  # username -> (socket, address)
        self.user_manager = UserManager()
        self.running = True
        self.server_socket = None

        # 启动时清理所有在线状态
        self.cleanup_all_users()

    def cleanup_all_users(self):
        """启动时清理所有用户的在线状态"""
        print("清理用户在线状态...")
        for username in self.user_manager.get_all_users():
            self.user_manager.force_logout(username)
        print("用户状态清理完成")

    def start(self):
        """启动服务器"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

            print(f"=== Python聊天服务器 ===")
            print(f"地址: {self.host}:{self.port}")
            print(f"等待客户端连接...")
            print("=" * 30)

            # 接受客户端连接
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"新的客户端连接: {address}")

                    # 为每个客户端创建线程
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()

                except Exception as e:
                    if self.running:
                        print(f"接受连接时出错: {e}")

        except Exception as e:
            print(f"服务器启动失败: {e}")
        finally:
            self.stop()

    def handle_client(self, client_socket, address):
        """处理客户端连接"""
        username = None
        try:
            while self.running:
                # 接收数据
                data = client_socket.recv(1024)
                if not data:
                    break

                # 处理消息
                message = data.decode('utf-8')
                print(f"收到来自 {address} 的消息: {message}")

                try:
                    msg_data = json.loads(message)
                    username = self.process_message(client_socket, address, msg_data)
                except json.JSONDecodeError as e:
                    print(f"JSON解析错误: {e}")
                    error_msg = {
                        'type': 'error',
                        'message': '消息格式错误'
                    }
                    client_socket.send(json.dumps(error_msg).encode('utf-8'))

        except Exception as e:
            print(f"处理客户端 {address} 时出错: {e}")
        finally:
            if username and username in self.clients:
                self.user_manager.logout(username)
                del self.clients[username]
                self.broadcast_user_list()
                self.broadcast_system_message(f"{username} 离开了聊天室")
                print(f"用户 {username} 已下线")

            client_socket.close()
            print(f"客户端 {address} 断开连接")

    def process_message(self, client_socket, address, data):
        """处理消息"""
        msg_type = data.get('type')
        username = data.get('username')

        if msg_type == 'register':
            self.handle_register(client_socket, data)
            return None
        elif msg_type == 'login':
            return self.handle_login(client_socket, address, data)
        elif msg_type == 'message':
            self.handle_chat_message(data)
            return username
        elif msg_type == 'logout':
            self.handle_logout(data)
            return username
        elif msg_type == 'get_user_list':
            self.send_user_list(client_socket)
            return username

        return username

    def handle_register(self, client_socket, data):
        """处理用户注册"""
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        print(f"处理注册请求 - 用户名: {username}")

        success, message = self.user_manager.register(username, password)

        response = {
            'type': 'register_response',
            'success': success,
            'message': message
        }

        self.send_to_client(client_socket, response)
        print(f"注册结果: {message}")

    def handle_login(self, client_socket, address, data):
        """处理用户登录"""
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        print(f"处理登录请求 - 用户名: {username}")

        # 如果用户已在线，先强制下线
        if username in self.clients:
            print(f"用户 {username} 已在线，强制下线")
            self.remove_client(username)

        success, message = self.user_manager.login(username, password)

        if success:
            # 登录成功
            self.clients[username] = (client_socket, address)

            response = {
                'type': 'login_response',
                'success': True,
                'message': '登录成功',
                'username': username
            }

            # 发送在线用户列表
            self.send_user_list(client_socket)

            # 广播用户上线消息
            self.broadcast_system_message(f"欢迎 {username} 加入聊天室！")
            self.broadcast_user_list()

            print(f"用户 {username} 登录成功")

        else:
            # 登录失败
            response = {
                'type': 'login_response',
                'success': False,
                'message': message
            }
            print(f"用户 {username} 登录失败: {message}")

        self.send_to_client(client_socket, response)
        return username if success else None

    def handle_chat_message(self, data):
        """处理聊天消息"""
        username = data.get('username')
        content = data.get('content', '')
        timestamp = data.get('timestamp', time.time())

        if username in self.clients and content.strip():
            print(f"聊天消息 - {username}: {content}")

            message = {
                'type': 'chat_message',
                'username': username,
                'content': content,
                'timestamp': timestamp
            }
            self.broadcast_message(message)

    def handle_logout(self, data):
        """处理用户登出"""
        username = data.get('username')
        if username and username in self.clients:
            print(f"用户 {username} 主动登出")
            self.remove_client(username)

    def send_to_client(self, client_socket, message):
        """发送消息给指定客户端"""
        try:
            message_json = json.dumps(message, ensure_ascii=False)
            client_socket.send(message_json.encode('utf-8'))
        except Exception as e:
            print(f"发送消息到客户端失败: {e}")

    def broadcast_message(self, message):
        """广播消息给所有客户端"""
        message_json = json.dumps(message, ensure_ascii=False)
        disconnected_users = []

        for username, (client_socket, _) in self.clients.items():
            try:
                client_socket.send(message_json.encode('utf-8'))
            except Exception as e:
                print(f"发送消息给 {username} 失败: {e}")
                disconnected_users.append(username)

        # 清理断开连接的客户端
        for username in disconnected_users:
            self.remove_client(username)

    def broadcast_system_message(self, content):
        """广播系统消息"""
        message = {
            'type': 'system_message',
            'content': content,
            'timestamp': time.time()
        }
        self.broadcast_message(message)

    def send_user_list(self, client_socket):
        """发送用户列表给指定客户端"""
        online_users = list(self.clients.keys())
        message = {
            'type': 'user_list',
            'users': online_users,
            'timestamp': time.time()
        }
        self.send_to_client(client_socket, message)

    def broadcast_user_list(self):
        """广播用户列表给所有客户端"""
        online_users = list(self.clients.keys())
        message = {
            'type': 'user_list',
            'users': online_users,
            'timestamp': time.time()
        }
        self.broadcast_message(message)
        print(f"在线用户列表更新: {online_users}")

    def remove_client(self, username):
        """移除客户端"""
        if username in self.clients:
            print(f"移除客户端: {username}")
            self.user_manager.logout(username)
            del self.clients[username]
            self.broadcast_user_list()
            return True
        return False

    def stop(self):
        """停止服务器"""
        print("正在停止服务器...")
        self.running = False

        # 通知所有客户端
        shutdown_msg = {
            'type': 'system_message',
            'content': '服务器已关闭',
            'timestamp': time.time()
        }
        self.broadcast_message(shutdown_msg)

        # 关闭所有客户端连接
        for username, (client_socket, _) in self.clients.items():
            try:
                client_socket.close()
            except:
                pass

        # 清理所有在线状态
        for username in self.clients.keys():
            self.user_manager.logout(username)

        if self.server_socket:
            self.server_socket.close()

        print("服务器已停止")


if __name__ == "__main__":
    print("正在启动聊天服务器...")
    server = ChatServer()

    try:
        server.start()
    except KeyboardInterrupt:
        print("\n接收到 Ctrl+C，正在关闭服务器...")
        server.stop()
    except Exception as e:
        print(f"服务器运行出错: {e}")
    finally:
        print("程序退出")
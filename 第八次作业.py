import socket
import re
import threading


class StringTypeClassifier:
    """字符串类型分类器"""

    def __init__(self):
        # 中国电话号码正则表达式
        self.phone_pattern = re.compile(r'^(?:\+86)?1[3-9]\d{9}$|^(?:\+86)?\d{3,4}-\d{7,8}$')
        # 中国邮政编码正则表达式
        self.postcode_pattern = re.compile(r'^[1-9]\d{5}$')
        # 网站网址正则表达式
        self.url_pattern = re.compile(
            r'^(https?://)?'  # http:// or https:// (可选)
            r'([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+'  # 域名
            r'[a-zA-Z]{2,}'  # 顶级域名
            r'(:\d+)?'  # 端口 (可选)
            r'(/.*)?$'  # 路径 (可选)
        )

    def classify_string(self, text):
        """分类字符串类型"""
        text = text.strip()

        if not text:
            return "空字符串"

        # 检查电话号码
        if self.phone_pattern.match(text):
            return "中国电话号码类型"

        # 检查邮政编码
        if self.postcode_pattern.match(text):
            return "中国邮政编码类型"

        # 检查网址
        if self.url_pattern.match(text):
            return "网站网址类型"

        return "其他未识别类型"


class SocketServer:
    """Socket服务器类"""

    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.classifier = StringTypeClassifier()
        self.running = False

    def handle_client(self, client_socket, address):
        """处理客户端连接"""
        print(f"新的客户端连接: {address}")

        try:
            while True:
                # 接收客户端发送的数据
                data = client_socket.recv(1024).decode('utf-8')

                if not data:
                    print(f"客户端 {address} 断开连接")
                    break

                print(f"收到来自 {address} 的字符串: {data}")

                # 分类字符串类型
                result = self.classifier.classify_string(data)

                # 发送结果回客户端
                response = f"字符串 '{data}' 的类型是: {result}"
                client_socket.send(response.encode('utf-8'))
                print(f"发送响应给 {address}: {result}")

        except Exception as e:
            print(f"处理客户端 {address} 时发生错误: {e}")
        finally:
            client_socket.close()

    def start_server(self):
        """启动服务器"""
        # 创建socket对象
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            # 绑定地址和端口
            server_socket.bind((self.host, self.port))
            # 开始监听
            server_socket.listen(5)
            self.running = True

            print(f"服务器启动在 {self.host}:{self.port}")
            print("等待客户端连接...")

            while self.running:
                try:
                    # 接受客户端连接
                    client_socket, address = server_socket.accept()

                    # 为每个客户端创建新线程
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()

                except KeyboardInterrupt:
                    print("\n服务器正在关闭...")
                    break
                except Exception as e:
                    print(f"接受连接时发生错误: {e}")

        except Exception as e:
            print(f"服务器启动失败: {e}")
        finally:
            server_socket.close()
            print("服务器已关闭")


def test_classifier():
    """测试分类器功能"""
    classifier = StringTypeClassifier()

    test_cases = [
        "13800138000",  # 手机号码
        "+8613800138000",  # 带国际码的手机
        "010-12345678",  # 固定电话
        "0755-87654321",  # 区号电话
        "518000",  # 邮政编码
        "100000",  # 邮政编码
        "https://www.baidu.com",  # 网址
        "http://google.com",  # 网址
        "www.example.com",  # 网址
        "hello world",  # 其他
        "12345",  # 其他
        ""  # 空字符串
    ]

    print("分类器测试结果:")
    print("-" * 50)
    for test in test_cases:
        result = classifier.classify_string(test)
        print(f"'{test}' -> {result}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # 测试模式
        test_classifier()
    else:
        # 启动服务器
        server = SocketServer('0.0.0.0', 8888)  # 0.0.0.0 允许所有IP连接
        server.start_server()
# client_test.py - 客户端测试程序
import socket


def test_client():
    """测试客户端"""
    try:
        # 创建socket连接
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8888))

        test_strings = [
            "13812345678",
            "518000",
            "https://www.baidu.com",
            "hello world",
            "010-12345678"
        ]

        for test_str in test_strings:
            # 发送字符串
            client_socket.send(test_str.encode('utf-8'))

            # 接收服务器响应
            response = client_socket.recv(1024).decode('utf-8')
            print(f"服务器响应: {response}")

        client_socket.close()

    except Exception as e:
        print(f"客户端错误: {e}")


if __name__ == "__main__":
    test_client()
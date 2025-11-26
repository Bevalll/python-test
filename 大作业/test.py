import socket
import threading
import time

def test_server():
    try:
        # 测试端口是否可用
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', 8888))
        server_socket.listen(5)
        print("✓ 服务器端口测试成功: localhost:8888")
        server_socket.close()
        return True
    except Exception as e:
        print(f"✗ 服务器端口测试失败: {e}")
        return False

def test_imports():
    try:
        import json
        import tkinter
        print("✓ 所有依赖库导入成功")
        return True
    except Exception as e:
        print(f"✗ 依赖库导入失败: {e}")
        return False

if __name__ == "__main__":
    print("正在测试环境...")
    test_imports()
    test_server()
    input("按回车键退出...")
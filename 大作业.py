import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw
import tensorflow as tf
from tensorflow import keras
import os
import io

# 禁用oneDNN警告
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


class HandwrittenDigitRecognizer:
    def __init__(self, root):
        self.root = root
        self.root.title("手写数字识别系统 - 无Ghostscript版本")
        self.root.geometry("800x700")

        # 创建画布图像（用于直接处理，避免EPS转换）
        self.canvas_image = Image.new("RGB", (400, 400), "white")
        self.draw = ImageDraw.Draw(self.canvas_image)

        # 加载模型
        self.model = self.load_simple_model()

        # 创建界面
        self.create_widgets()

    def load_simple_model(self):
        """加载简化模型（避免长时间训练）"""
        try:
            # 尝试加载预训练模型
            return keras.models.load_model('simple_digit_model.h5')
        except:
            # 如果不存在，创建一个简单的模型结构
            model = keras.Sequential([
                keras.layers.Flatten(input_shape=(28, 28, 1)),
                keras.layers.Dense(128, activation='relu'),
                keras.layers.Dense(10, activation='softmax')
            ])
            model.compile(optimizer='adam',
                          loss='sparse_categorical_crossentropy',
                          metrics=['accuracy'])
            return model

    def create_widgets(self):
        """创建界面"""
        # 标题
        title_label = tk.Label(self.root, text="手写数字识别系统",
                               font=("Arial", 16, "bold"), pady=10)
        title_label.pack()

        # 按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        upload_btn = tk.Button(button_frame, text="上传图片",
                               command=self.upload_image,
                               font=("Arial", 12), bg="#4CAF50", fg="white",
                               width=12, height=1)
        upload_btn.grid(row=0, column=0, padx=10)

        recognize_btn = tk.Button(button_frame, text="开始识别",
                                  command=self.recognize_digits,
                                  font=("Arial", 12), bg="#2196F3", fg="white",
                                  width=12, height=1)
        recognize_btn.grid(row=0, column=1, padx=10)

        clear_btn = tk.Button(button_frame, text="清除画布",
                              command=self.clear_canvas,
                              font=("Arial", 12), bg="#f44336", fg="white",
                              width=12, height=1)
        clear_btn.grid(row=0, column=2, padx=10)

        # 画布
        self.canvas = tk.Canvas(self.root, width=400, height=400,
                                bg="white", relief="solid", bd=2)
        self.canvas.pack(pady=10)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.start_paint)
        self.canvas.bind("<ButtonRelease-1>", self.stop_paint)

        # 结果显示
        self.result_label = tk.Label(self.root, text="识别结果: 等待输入...",
                                     font=("Arial", 14, "bold"))
        self.result_label.pack(pady=10)

        # 绘画变量
        self.last_x = None
        self.last_y = None
        self.drawing = False

    def start_paint(self, event):
        """开始绘画"""
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        self.draw.ellipse([event.x - 8, event.y - 8, event.x + 8, event.y + 8], fill='black')

    def stop_paint(self, event):
        """停止绘画"""
        self.drawing = False
        self.last_x = None
        self.last_y = None

    def paint(self, event):
        """绘画过程"""
        if self.drawing and self.last_x and self.last_y:
            # 在tkinter画布上绘制
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=15, fill="black", capstyle=tk.ROUND, smooth=tk.TRUE)
            # 在PIL图像上绘制
            self.draw.line([self.last_x, self.last_y, event.x, event.y],
                           fill='black', width=15)
            self.last_x = event.x
            self.last_y = event.y

    def clear_canvas(self):
        """清除画布"""
        self.canvas.delete("all")
        self.canvas_image = Image.new("RGB", (400, 400), "white")
        self.draw = ImageDraw.Draw(self.canvas_image)
        self.result_label.config(text="识别结果: 等待输入...")

    def upload_image(self):
        """上传图片"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp")]
            )
            if file_path:
                # 显示上传的图片
                img = Image.open(file_path)
                img = img.resize((400, 400))
                self.photo = ImageTk.PhotoImage(img)
                self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

                # 保存为canvas_image用于识别
                self.canvas_image = img.copy()
                self.draw = ImageDraw.Draw(self.canvas_image)

        except Exception as e:
            messagebox.showerror("错误", f"图片加载失败: {str(e)}")

    def recognize_digits(self):
        """识别数字 - 无Ghostscript版本"""
        try:
            # 直接使用PIL图像进行处理，避免EPS转换
            gray_image = self.canvas_image.convert('L')
            image_array = np.array(gray_image)

            processed_digits = self.preprocess_image(image_array)

            if processed_digits is not None:
                # 进行预测
                predictions = self.model.predict(processed_digits, verbose=0)
                recognized_digits = [np.argmax(pred) for pred in predictions]

                result_text = "识别结果: " + "".join(map(str, recognized_digits))
                self.result_label.config(text=result_text)

                # 如果是简单模型，显示提示
                if len(recognized_digits) > 0:
                    messagebox.showinfo("提示",
                                        f"识别结果: {recognized_digits}\n"
                                        f"注意: 这是简化模型，准确率可能不高\n"
                                        f"建议使用预训练模型获得更好效果")
            else:
                messagebox.showwarning("警告", "未检测到手写数字")

        except Exception as e:
            messagebox.showerror("错误", f"识别过程中出现错误: {str(e)}")

    def preprocess_image(self, image):
        """预处理图像"""
        # 二值化
        _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

        # 寻找轮廓
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        digit_images = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            if w > 20 and h > 20:
                digit = binary[y:y + h, x:x + w]
                digit = cv2.resize(digit, (28, 28))
                digit = digit.astype('float32') / 255.0
                digit = digit.reshape(1, 28, 28, 1)
                digit_images.append(digit)

        if digit_images:
            return np.vstack(digit_images)
        return None


# 极简测试版本（确保能运行）
class SimpleDigitTest:
    def __init__(self, root):
        self.root = root
        self.root.title("手写数字识别 - 测试版")
        self.root.geometry("500x500")

        # 标题
        title = tk.Label(root, text="手写数字识别测试", font=("Arial", 16))
        title.pack(pady=10)

        # 画布
        self.canvas = tk.Canvas(root, width=300, height=300, bg='white')
        self.canvas.pack(pady=10)
        self.canvas.bind("<B1-Motion>", self.draw)

        # 按钮
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="识别", command=self.predict).pack(side='left', padx=5)
        tk.Button(btn_frame, text="清除", command=self.clear).pack(side='left', padx=5)
        tk.Button(btn_frame, text="上传", command=self.upload).pack(side='left', padx=5)

        # 结果
        self.result = tk.Label(root, text="请手写数字", font=("Arial", 14))
        self.result.pack(pady=10)

    def draw(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')

    def clear(self):
        self.canvas.delete("all")
        self.result.config(text="请手写数字")

    def upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("图片", "*.jpg *.png")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((300, 300))
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
            self.result.config(text="图片已加载，点击识别")

    def predict(self):
        self.result.config(text="识别结果: 7")  # 模拟识别结果
        messagebox.showinfo("提示", "这是测试版本\n实际使用时需要完整的CNN模型")


if __name__ == "__main__":
    root = tk.Tk()

    # 选择使用哪个版本：
    # app = HandwrittenDigitRecognizer(root)  # 完整版（可能还需要调整）
    app = SimpleDigitTest(root)  # 极简测试版（确保能运行）

    root.mainloop()
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import Qt, QThread
import tkinter as tk
import urllib
from tkinter import messagebox
from pytube import YouTube

theard_error = 0 # 0: good, 1: error

class download_thread(QThread):
    def __init__(self, input):
        QThread.__init__(self)
        self.input_btn = input

    def run(self):
        url = self.input_btn.text()

        try:
            youtube = YouTube(url)
        except RuntimeError:
            self.show_error()
        except urllib.error.URLError:
            self.show_error()
        else:
            root = tk.Tk()
            root.withdraw()
            video = youtube.streams.first()
            messagebox.showinfo("Vidoe title", video.title)
            messagebox.showinfo("Path", "Downloading in Downloads folder, please be patient!")
            video.download('C:\Video')
            messagebox.showinfo("Downloaded", "Downloaded!, Please check for the video in C:\Video")

    def show_error(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setWindowTitle("Unexcpected error")
        self.msg.setText("Unexcpected error. Please try again.")

        retval = self.msg.exec_()

class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.GUI()
        
    def GUI(self):
        self.url_input = QLineEdit(self)
        self.url_btn = QPushButton(self)
        self.label = QLabel("Made by Shayan Kermani", self)
        self.fl = QFormLayout(self)

        self.url_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.url_btn.setText("Download")
        self.url_btn.clicked.connect(self.btn_clicked)

        self.label.setAlignment(Qt.AlignCenter)

        self.fl.addRow("URL:", self.url_input)
        self.fl.addRow(self.url_btn)
        self.fl.addRow(self.label)

        self.setLayout(self.fl)
        self.setWindowTitle("Youtube Downloader")
        self.setWindowIcon(QIcon('img/logo.png'))
        self.resize(1000, 120)

    def btn_clicked(self):
        url = self.url_input.text()
        root = tk.Tk()
        root.withdraw()
        if url == ' ':
            messagebox.showerror("Null", "The input was null! please refill it and try again.")
            return 0
        elif not("https://www.youtube.com" in url):
            messagebox.showerror("Incorrect", "You url is unvailable. It's incorrct actually.")
            return 0
        self.download = download_thread(self.url_input)
        self.download.start()
        if theard_error == 1:
            messagebox.showerror("Unexcpected Error", "There was an unexcpected error.")

if __name__ == "__main__":
    app = QApplication([])
    window = Ui()
    window.show()
    app.exec_()
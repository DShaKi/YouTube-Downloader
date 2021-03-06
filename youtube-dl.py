from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QThread
from pytube import YouTube

class download_thread(QThread):
    def __init__(self, input):
        QThread.__init__(self)
        self.input_btn = input

    def run(self):
        url = self.input_btn.text()
        youtube = YouTube(url)
        video = youtube.streams.first()
        print("Video title: ", video.title)
        print("Downloading in Downloads folder")
        print("Please be patient")
        video.download('C:\Video')
        print("Downloaded")
        print("Please check for the video in C:\Video")

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
        self.resize(1000, 120)

    def btn_clicked(self):
        self.download = download_thread(self.url_input)
        self.download.start()

if __name__ == "__main__":
    app = QApplication([])
    window = Ui()
    window.show()
    app.exec_()
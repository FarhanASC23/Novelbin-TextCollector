import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

def extract_text_from_chapter(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = ''
    for div in soup.find_all('div', class_='chr-c'):
        paragraphs = div.find_all('p')
        for paragraph in paragraphs:
            text += paragraph.get_text() + '\n'
    return text

class ChapterTextExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chapter Text Extractor')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet('background-color: #121212; color: white; border-radius: 10px;')

        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QGridLayout()
        output_layout = QVBoxLayout()

        # URL input
        self.url_label = QLabel('Base URL:')
        self.url_label.setFont(QFont('Arial', 12))
        self.url_input = QLineEdit()
        self.url_input.setFont(QFont('Arial', 12))
        self.url_input.setStyleSheet('background-color: #1e1e1e; color: white; border-radius: 5px; padding: 5px;')
        input_layout.addWidget(self.url_label, 0, 0)
        input_layout.addWidget(self.url_input, 0, 1)

        # Start chapter input
        self.start_chapter_label = QLabel('Start Chapter:')
        self.start_chapter_label.setFont(QFont('Arial', 12))
        self.start_chapter_input = QLineEdit()
        self.start_chapter_input.setFont(QFont('Arial', 12))
        self.start_chapter_input.setStyleSheet('background-color: #1e1e1e; color: white; border-radius: 5px; padding: 5px;')
        input_layout.addWidget(self.start_chapter_label, 1, 0)
        input_layout.addWidget(self.start_chapter_input, 1, 1)

        # End chapter input
        self.end_chapter_label = QLabel('End Chapter:')
        self.end_chapter_label.setFont(QFont('Arial', 12))
        self.end_chapter_input = QLineEdit()
        self.end_chapter_input.setFont(QFont('Arial', 12))
        self.end_chapter_input.setStyleSheet('background-color: #1e1e1e; color: white; border-radius: 5px; padding: 5px;')
        input_layout.addWidget(self.end_chapter_label, 2, 0)
        input_layout.addWidget(self.end_chapter_input, 2, 1)

        # Extract button
        self.extract_button = QPushButton('Start Extraction')
        self.extract_button.setFont(QFont('Arial', 12))
        self.extract_button.setStyleSheet('background-color: #6200EE; color: white; border-radius: 5px; padding: 10px;')
        self.extract_button.clicked.connect(self.start_extraction)
        input_layout.addWidget(self.extract_button, 3, 1)

        # Status label
        self.status_label = QLabel('')
        self.status_label.setFont(QFont('Arial', 12))
        self.status_label.setAlignment(Qt.AlignCenter)

        # Output text box
        self.output_text = QTextEdit()
        self.output_text.setFont(QFont('Arial', 12))
        self.output_text.setStyleSheet('background-color: #1e1e1e; color: white; border-radius: 5px; padding: 10px;')

        # Copy All button
        self.copy_button = QPushButton('Copy All')
        self.copy_button.setFont(QFont('Arial', 12))
        self.copy_button.setStyleSheet('background-color: #6200EE; color: white; border-radius: 5px; padding: 10px;')
        self.copy_button.clicked.connect(self.copy_all)

        output_layout.addWidget(self.status_label)
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(self.copy_button)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)

    def start_extraction(self):
        base_url = self.url_input.text().strip()
        start_chapter = int(self.start_chapter_input.text().strip())
        end_chapter = int(self.end_chapter_input.text().strip())

        self.status_label.setText(f"Extracting text from chapters {start_chapter} to {end_chapter}")
        self.output_text.clear()

        for chapter in range(start_chapter, end_chapter + 1):
            chapter_url = f"{base_url}{chapter}"
            chapter_text = extract_text_from_chapter(chapter_url)
            self.output_text.append(chapter_text)
            self.output_text.append(f"Text from chapter {chapter} saved.\n\n")

    def copy_all(self):
        self.output_text.selectAll()
        self.output_text.copy()
        QMessageBox.information(self, 'Copy All', 'All text has been copied to clipboard.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # Use the Fusion style
    QApplication.setStyle('Fusion')
    
    # Now use a palette to switch to dark colors
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(18, 18, 18))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.AlternateBase, QColor(18, 18, 18))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(30, 30, 30))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    ex = ChapterTextExtractor()
    ex.show()
    sys.exit(app.exec_())

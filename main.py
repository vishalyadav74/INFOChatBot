import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QCompleter
from PyQt5.QtGui import QTextCursor, QPixmap
from PyQt5.QtCore import Qt
import random
import datetime
import re
import pyjokes
from quote import quote
import wikipediaapi
from textblob import TextBlob

class SimpleChatbot:
    def __init__(self):
        self.greetings = ["hello", "hi", "hey", "howdy"]
        self.responses = ["Hello!", "Hi there!", "Hey!", "How can I help you today?"]
        self.commands = ["joke", "quote", "fact", "time", "sentiment", "help"]

    def get_random_joke(self, user_input):
        return pyjokes.get_joke()

    def get_random_quote(self, user_input):
        return quote()

    def get_daily_fact(self):
        wiki_wiki = wikipediaapi.Wikipedia("en")
        page_py = wiki_wiki.page("Special:Random")
        return page_py.summary[:200]  # Display the first 200 characters of the summary

    def get_response(self, user_input):
        user_input = user_input.lower()
        print(f"Detected command: {user_input}")
        if user_input in self.greetings:
            return random.choice(self.responses)
        elif "joke" in user_input:
            return self.get_random_joke(user_input)
        elif "quote" in user_input:
            return self.get_random_quote(user_input)
        elif "sentiment" in user_input:
            return self.analyze_sentiment(user_input)
        elif "fact" in user_input:
            return self.get_daily_fact()
        elif "time" in user_input:
            return self.get_current_time()
        elif "help" in user_input:
            return "Available commands: joke, quote, fact, time, sentiment, help"
        else:
            return "I don't understand that. Please ask me something else."

    def get_current_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"

    def analyze_sentiment(self, user_input):
        blob = TextBlob(user_input)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            return "That sounds positive!"
        elif sentiment < 0:
            return "Seems a bit negative. Is everything okay?"
        else:
            return "I sense a neutral sentiment."

    def tokenize_input(self, user_input):
        return re.findall(r'\b\w+\b', user_input.lower())

class ChatGPTUI(QWidget):
    def __init__(self):
        super().__init__()

        # Create chatbot instance
        self.chatbot = SimpleChatbot()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.conversation_display = QTextEdit(self)
        self.user_input_entry = QLineEdit(self)

        # Set up autocompletion
        completer = QCompleter(self.chatbot.commands, self)
        self.user_input_entry.setCompleter(completer)

        self.send_button = QPushButton('Send', self)
        self.chatbot_image = QLabel(self)

        # Set up dark theme
        self.setStyleSheet(
            f"QWidget {{ background-image: url('C:/Users/VISHA/PycharmProjects/pythonProject1/image2.png'); }}"
            "background-repeat: no-repeat;"
            "background-position: center;"
            "background-size: cover;"
            "color: #ffffff;"
            "font-family: Arial, sans-serif;"
        )

        # Additional styling if needed
        self.conversation_display.setStyleSheet(
            "background-color: #333333;"
            "color: #ffffff;"
            "border: 1px solid #555555;"
            "border-radius: 5px;"
        )

        self.user_input_entry.setStyleSheet(
            "background-color: #444444;"
            "color: #ffffff;"
            "border: 1px solid #666666;"
            "border-radius: 5px;"
        )

        self.send_button.setStyleSheet(
            "background-color: #007bff;"
            "color: #ffffff;"
            "border: 1px solid #0056b3;"
            "border-radius: 5px;"
        )

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.conversation_display)
        layout.addWidget(self.user_input_entry)
        layout.addWidget(self.send_button, 0, Qt.AlignRight)
        layout.addWidget(self.chatbot_image, 0, Qt.AlignCenter)

        # Connect signals
        self.send_button.clicked.connect(self.process_user_input)
        self.user_input_entry.returnPressed.connect(self.send_button.click)

        # Set up the main window
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('InfoBot')

        # Load and set the chatbot image
        try:
            chatbot_pixmap = QPixmap(".png")
            self.chatbot_image.setPixmap(chatbot_pixmap)
            self.chatbot_image.setAlignment(Qt.AlignCenter)
            self.chatbot_image.setStyleSheet("margin: 20px;")
        except Exception as e:
            print(f"Error loading image: {e}")

        self.show()

    def process_user_input(self):
        user_input = self.user_input_entry.text()
        self.display_message(f'<span style="color: #007bff;">You:</span> {user_input}')

        # Call the chatbot to get a response
        response = self.chatbot.get_response(user_input)

        self.display_message(f'<span style="color: #e44d26;">InfoBot:</span> {response}')
        self.user_input_entry.clear()

    def display_message(self, message):
        cursor = self.conversation_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(f'{message}<br>')
        self.conversation_display.setTextCursor(cursor)
        self.conversation_display.verticalScrollBar().setValue(self.conversation_display.verticalScrollBar().maximum())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatgpt_ui = ChatGPTUI()
    sys.exit(app.exec_())

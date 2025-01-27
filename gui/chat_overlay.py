import sys
import hashlib
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QColor, QFont, QFontMetrics

class MessageWidget(QLabel):
    def __init__(self, username, text, color, max_width):
        super().__init__()
        self.username = username
        self.text = text
        self.color = color
        self.max_width = max_width - 20  # Account for container padding
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f"""
            color: white;
            font: 12px 'Arial';
            margin: 0px;
            padding: 0px;
        """)
        self.setTextFormat(Qt.RichText)
        self.setText(f"<font color='{self.color}'>{self.username}:</font> {self.text}")
        self.setWordWrap(True)

        # Calculate exact text height
        metrics = QFontMetrics(QFont("Arial", 12))
        text_rect = metrics.boundingRect(
            QRect(0, 0, self.max_width, 1000),
            Qt.TextWordWrap | Qt.AlignLeft,
            self.text
        )
        
        # Set fixed height with minimal padding
        self.setFixedHeight(text_rect.height() + 4)  # 2px top/bottom padding

class ChatOverlay(QWidget):

    def __init__(self):
        super().__init__()
        self.max_container_height = 300
        self.container_width = 400
        self.messages = []
        self.initUI()
        self.position_at_bottom_right()

        # Deduplication
        self.disallow_spam = True
        self.message_cache = set()  # Cache for deduplication

        # Timer to clear cache every 10 seconds
        self.cache_timer = QTimer(self)
        self.cache_timer.timeout.connect(self.clear_message_cache)
        self.cache_timer.start(30000)  # Clear cache every x seconds

    def clear_message_cache(self):
        """Clear the deduplication cache."""
        self.message_cache.clear()

    def initUI(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            border-radius: 8px;
            padding: 10px;
        """)
        self.setFixedWidth(self.container_width)
        self.resize(self.container_width, self.max_container_height)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # No layout margins
        self.layout.setSpacing(3)  # Consistent small spacing between messages
        self.layout.setAlignment(Qt.AlignBottom)

    def position_at_bottom_right(self):
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 20
        y = screen.height() - self.height() - 60
        self.move(x, y)

    def username_to_color(self, username):
        hash_int = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
        return QColor.fromHsv(hash_int % 360, 150, 230).name()

    def add_message(self, username: str, text: str):

        if self.disallow_spam:
            # Check for duplicates
            message_key = (username, text.strip())
            if message_key in self.message_cache:
                return  # Ignore duplicate message

            # Add message to cache
            self.message_cache.add(message_key)

        color = self.username_to_color(username)
        msg = MessageWidget(username, text.strip("\n"), color, self.container_width)

        self.layout.addWidget(msg)
        self.messages.append(msg)

        # Enforce container height limit
        total_height = sum(msg.height() for msg in self.messages) + (len(self.messages) - 1) * self.layout.spacing()
        while total_height > self.max_container_height and self.messages:
            oldest = self.messages.pop(0)
            self.layout.removeWidget(oldest)
            oldest.deleteLater()
            total_height = sum(msg.height() for msg in self.messages) + (len(self.messages) - 1) * self.layout.spacing()

        self.setFixedHeight(min(self.max_container_height, total_height))
        self.position_at_bottom_right()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = ChatOverlay()
    overlay.show()

    test_messages = [
        ("George", "Short message"),
        ("Mary", "This is a medium-length message that demonstrates proper wrapping"),
        ("Kary", "Very long message that should show consistent spacing between lines. " 
         "The quick brown fox jumps over the lazy dog. " 
         "Pack my box with five dozen liquor jugs."),
        ("Player1", "Two-line message"),
    ]

    timer = QTimer()
    timer.timeout.connect(lambda: (
        overlay.add_message(*test_messages.pop(0)) if test_messages else None
    ))
    timer.start(500)

    sys.exit(app.exec_())

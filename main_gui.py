from gui.ui_mainwindow import *
from live_feed import *

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi
from PyQt5.QtCore import QMetaObject, Qt, Q_ARG

import google.genai as genai


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        # General properties
        self.recording: bool = False
        self.gemini_key: str = None

        self.setupUi(self)
        self.connectSignalsSlots()

        # Default texts
        self.promptInput.setPlainText(DEFAULT_PROMPT)

        # Chat Overlay
        self.chat_overlay: ChatOverlay = ChatOverlay()

        # LiveFeed Thread
        self.live_feed: LiveFeed = None
        self.live_feed_task = None
        self.shutdown_complete = True

        # DEBUG
        #self.startRecordButton.setEnabled(True)

        self.setWindowTitle("LiveChat")

    def connectSignalsSlots(self):
        # Buttons
        self.confirmKeyBtn.clicked.connect(self.confirmKey)
        self.startRecordButton.clicked.connect(self.record)
        self.envUseButton.clicked.connect(self.useEnvKey)

    def useEnvKey(self):
        self.envUseButton.setEnabled(False)
        self.apiKeyInput.setEnabled(False)
        self.confirmKeyBtn.setEnabled(False)

        self.gemini_key = None
        self.startRecordButton.setEnabled(True)

    # Confirm API Key
    def confirmKey(self):
        api_key = self.apiKeyInput.text()

        # Check whether key is valid
        success = True
        try:
            genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'}).models.list()
        except Exception:
            success = False

        if not success:
            QMessageBox.critical(None, "Error", "Invalid API key")
            return
        
        self.apiKeyInput.setEnabled(False)
        self.confirmKeyBtn.setEnabled(False)
        self.envUseButton.setEnabled(False)

        self.gemini_key = api_key
        self.startRecordButton.setEnabled(True)

    def record(self):
        self.recording = not self.recording
        
        # Start Recording
        if self.recording and self.shutdown_complete:
            self.startRecordButton.setText('Stop Recording')

            # Initialize chat overlay and live feed
            self.chat_overlay = ChatOverlay()
            self.live_feed = LiveFeed(self.chat_overlay, gemini_key=self.gemini_key, prompt=self.promptInput.toPlainText(), voice_recording=self.enableVoiceBox.isChecked(), safety_system=self.enableSafetyBox.isChecked())

            self.chat_overlay.show()
            self.chat_overlay.add_message("Chat", "Starting...")

            # Schedule the LiveFeed.run() coroutine
            loop = asyncio.get_event_loop()
            self.live_feed_task = loop.create_task(self.live_feed.run())

            # Shutdown
            self.live_feed_task.add_done_callback(self.on_shutdown_complete)

            # Disable editing some stuff
            self.promptInput.setEnabled(False)
            self.enableVoiceBox.setEnabled(False)
            self.enableSafetyBox.setEnabled(False)

        # Stop recording
        else:
            self.startRecordButton.setText('Start Recording')
            self.startRecordButton.setEnabled(False)
            self.shutdown_complete = False

            # Close any thread
            if self.live_feed:
                self.live_feed.stop()
            if self.chat_overlay:
                self.chat_overlay.close()

    def on_shutdown_complete(self, task):
        # Called when LiveFeed fully stops
        self.recording = False
        self.shutdown_complete = True

        # Enable buttons again
        self.promptInput.setEnabled(True)
        self.enableVoiceBox.setEnabled(True)
        self.enableSafetyBox.setEnabled(True)
        
        QMetaObject.invokeMethod(
            self.startRecordButton,
            "setEnabled",
            Qt.QueuedConnection,
            Q_ARG(bool, True)
        )
        
        if task.exception():
            QMessageBox.critical(self, "Error", str(task.exception()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set up the asyncio event loop with qasync
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    win = Window()
    win.show()
    with loop:
        sys.exit(loop.run_forever())

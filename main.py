from gui import AudioTranscriptionWindow

import sys
from PySide6.QtWidgets import QApplication


app = QApplication(sys.argv)

window = AudioTranscriptionWindow()
window.show()

sys.exit(app.exec())
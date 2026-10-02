import sys
import os

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QComboBox
)

from recorder import AudioRecorder
from transcriber import transcribe_audio
from transcript_formatter import format_transcript


class TranscriptionWorker(QThread):

    finished = Signal(str)
    error = Signal(str)

    def __init__(self, audio_file, language_code):
        super().__init__()

        self.audio_file = audio_file
        self.language_code = language_code

    def run(self):

        try:

            result = transcribe_audio(
                self.audio_file,
                language_code=self.language_code
            )

            transcript = format_transcript(
                result
            )

            self.finished.emit(
                transcript
            )

        except Exception as error:

            self.error.emit(
                str(error)
            )


class AudioTranscriptionWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Volga Audio Transcription App"
        )

        self.resize(
            600,
            450
        )

        self.selected_file = None
        self.transcript = None

        self.worker = None
        self.recorder = AudioRecorder()

        # Title

        self.title_label = QLabel(
            "Volga Audio Transcription App"
        )

        # File

        self.file_label = QLabel(
            "No audio file selected"
        )

        self.browse_button = QPushButton(
            "Browse Audio File"
        )

        self.browse_button.clicked.connect(
            self.browse_audio
        )

        # Recording

        self.start_recording_button = QPushButton(
            "Start Recording"
        )

        self.stop_recording_button = QPushButton(
            "Stop Recording"
        )

        self.stop_recording_button.setEnabled(
            False
        )

        self.start_recording_button.clicked.connect(
            self.start_recording
        )

        self.stop_recording_button.clicked.connect(
            self.stop_recording
        )

        # Language

        self.language_label = QLabel(
            "Language:"
        )

        self.language_combo = QComboBox()

        self.language_combo.addItem(
            "English",
            "eng"
        )

        self.language_combo.addItem(
            "Urdu",
            "urd"
        )

        self.language_combo.addItem(
            "Arabic",
            "ara"
        )

        # Transcribe

        self.transcribe_button = QPushButton(
            "Transcribe"
        )

        self.transcribe_button.clicked.connect(
            self.transcribe
        )

        # Save

        self.save_button = QPushButton(
            "Save Transcript"
        )

        self.save_button.setEnabled(
            False
        )

        self.save_button.clicked.connect(
            self.save_transcript
        )

        # Status

        self.status_label = QLabel(
            "Status: Ready"
        )

        # Layout

        layout = QVBoxLayout()

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.file_label
        )

        layout.addWidget(
            self.browse_button
        )

        layout.addWidget(
            self.start_recording_button
        )

        layout.addWidget(
            self.stop_recording_button
        )

        layout.addWidget(
            self.language_label
        )

        layout.addWidget(
            self.language_combo
        )

        layout.addWidget(
            self.transcribe_button
        )

        layout.addWidget(
            self.save_button
        )

        layout.addWidget(
            self.status_label
        )

        self.setLayout(
            layout
        )

    def browse_audio(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.m4a *.flac *.aac *.ogg *.opus);;All Files (*)"
        )

        if file_path:

            self.selected_file = file_path
            self.transcript = None

            self.file_label.setText(
                os.path.basename(file_path)
            )

            self.status_label.setText(
                "Status: Audio file selected"
            )

            self.save_button.setEnabled(
                False
            )

    def start_recording(self):

        output_file = "output/microphone.wav"

        self.recorder.start_recording()

        self.start_recording_button.setEnabled(
            False
        )

        self.stop_recording_button.setEnabled(
            True
        )

        self.browse_button.setEnabled(
            False
        )

        self.transcribe_button.setEnabled(
            False
        )

        self.save_button.setEnabled(
            False
        )

        self.status_label.setText(
            "Status: Recording..."
        )

    def stop_recording(self):

        output_file = "output/microphone.wav"

        self.recorder.stop_recording(
            output_file
        )

        self.selected_file = output_file
        self.transcript = None

        self.start_recording_button.setEnabled(
            True
        )

        self.stop_recording_button.setEnabled(
            False
        )

        self.browse_button.setEnabled(
            True
        )

        self.transcribe_button.setEnabled(
            True
        )

        self.file_label.setText(
            "microphone.wav"
        )

        self.status_label.setText(
            "Status: Recording complete."
        )

    def transcribe(self):

        if not self.selected_file:

            self.status_label.setText(
                "Status: Please select or record audio first."
            )

            return

        language_code = (
            self.language_combo.currentData()
        )

        self.status_label.setText(
            "Status: Transcribing..."
        )

        self.browse_button.setEnabled(
            False
        )

        self.start_recording_button.setEnabled(
            False
        )

        self.transcribe_button.setEnabled(
            False
        )

        self.save_button.setEnabled(
            False
        )

        self.worker = TranscriptionWorker(
            self.selected_file,
            language_code
        )

        self.worker.finished.connect(
            self.transcription_finished
        )

        self.worker.error.connect(
            self.transcription_error
        )

        self.worker.start()

    def transcription_finished(
        self,
        transcript
    ):

        self.transcript = transcript

        self.status_label.setText(
            "Status: Transcription complete."
        )

        self.browse_button.setEnabled(
            True
        )

        self.start_recording_button.setEnabled(
            True
        )

        self.transcribe_button.setEnabled(
            True
        )

        self.save_button.setEnabled(
            True
        )

    def transcription_error(
        self,
        error
    ):

        self.status_label.setText(
            f"Status: Error - {error}"
        )

        self.browse_button.setEnabled(
            True
        )

        self.start_recording_button.setEnabled(
            True
        )

        self.transcribe_button.setEnabled(
            True
        )

        self.save_button.setEnabled(
            False
        )

    def save_transcript(self):

        if not self.transcript:

            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Transcript",
            "transcription.txt",
            "Text Files (*.txt)"
        )

        if not file_path:

            return

        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    self.transcript
                )

            self.status_label.setText(
                "Status: Transcript saved successfully."
            )

        except Exception as error:

            self.status_label.setText(
                f"Status: Error saving file - {error}"
            )


app = QApplication(sys.argv)

window = AudioTranscriptionWindow()

window.show()

sys.exit(app.exec())
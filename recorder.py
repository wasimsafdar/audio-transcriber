import sounddevice as sd
import soundfile as sf
import numpy as np


SAMPLE_RATE = 16000
CHANNELS = 1


class AudioRecorder:

    def __init__(self):
        self.audio_chunks = []
        self.recording = False
        self.stream = None

    def _callback(self, indata, frames, time, status):

        if status:
            print(status)

        if self.recording:
            self.audio_chunks.append(indata.copy())

    def start_recording(self):

        if self.recording:
            print("Already recording.")
            return

        self.audio_chunks = []
        self.recording = True

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            callback=self._callback
        )

        self.stream.start()

        print("Recording started...")

    def stop_recording(self, output_file):

        if not self.recording:
            print("No recording is currently running.")
            return

        self.recording = False

        self.stream.stop()
        self.stream.close()

        self.stream = None

        if not self.audio_chunks:
            print("No audio was recorded.")
            return

        audio = np.concatenate(
            self.audio_chunks,
            axis=0
        )

        sf.write(
            output_file,
            audio,
            SAMPLE_RATE
        )

        print("Recording stopped.")
        print(f"Audio saved to: {output_file}")
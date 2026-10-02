import os

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

from audio_utils import prepare_audio


load_dotenv()

api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    raise RuntimeError("ELEVENLABS_API_KEY is missing from .env")


client = ElevenLabs(api_key=api_key)


def transcribe_audio(file_path, language_code=None):

    audio_file_path = prepare_audio(file_path)

    with open(audio_file_path, "rb") as audio_file:

        result = client.speech_to_text.convert(
            file=audio_file,
            model_id="scribe_v2",
            language_code=language_code,
            diarize=False,
            timestamps_granularity="word"
        )

    return result
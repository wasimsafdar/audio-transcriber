import os
import subprocess
import tempfile


SUPPORTED_FORMATS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".flac",
    ".aac",
    ".ogg",
    ".opus",
}


def prepare_audio(file_path):
    """
    Prepare an audio file for transcription.

    If the format is already supported by our pipeline,
    return the original file.

    Otherwise, convert it to WAV using FFmpeg.
    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"Audio file not found: {file_path}"
        )

    extension = os.path.splitext(file_path)[1].lower()

    if extension in SUPPORTED_FORMATS:
        return file_path

    return convert_to_wav(file_path)


def convert_to_wav(file_path):
    """
    Convert an audio file to WAV using FFmpeg.
    """

    output_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    output_file.close()

    command = [
        "ffmpeg",
        "-y",
        "-i",
        file_path,
        "-ar",
        "16000",
        "-ac",
        "1",
        output_file.name
    ]

    try:

        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    except FileNotFoundError:

        raise RuntimeError(
            "FFmpeg was not found. "
            "Please install FFmpeg and make sure it is available in PATH."
        )

    except subprocess.CalledProcessError as error:

        raise RuntimeError(
            "FFmpeg could not convert the audio file."
        ) from error

    return output_file.name
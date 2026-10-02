def format_timestamp(seconds):
    """
    Converts seconds into MM:SS format.

    Example:
        0   -> 00:00
        10  -> 00:10
        65  -> 01:05
    """

    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return f"{minutes:02d}:{seconds:02d}"


def format_transcript(result, interval=10):
    """
    Convert ElevenLabs transcription result into
    text grouped into fixed time intervals.

    Example:

    [00:00] How many people are there...
    [00:10] ...
    [00:20] ...
    """

    buckets={}

    for item in result.words:

        if item.type != "word":
            continue

        bucket_start = int(item.start // interval) * interval

        if bucket_start not in buckets:
            buckets[bucket_start] = []

        buckets[bucket_start].append(item.text)

    # Build final transcript
    output = []

    for bucket_start in sorted(buckets.keys()):
        text = " ".join(buckets[bucket_start])

        timestamp = format_timestamp(bucket_start)

        output.append(
            f"[{timestamp}] {text}"
        )

    return "\n\n".join(output)


def save_transcript(transcript, output_file):
    """
    Save transcript text to a file.
    """

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(transcript)
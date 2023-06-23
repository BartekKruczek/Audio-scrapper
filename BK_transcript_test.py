from youtube_transcript_api import YouTubeTranscriptApi

video_id = "OHf4tcgcX2M"

# retrieve the available transcripts
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

# iterate over all available transcripts
for transcript in transcript_list:
    lines = []
    for line in transcript.fetch():
        text = line["text"]
        start = line["start"]
        duration = line["duration"]

        line_with_timestamp = f"[{start}] {text} [{duration}]"
        lines.append(line_with_timestamp)

    text_formatted = "\n".join(lines)

    with open("your_filename.txt", "w", encoding="utf-8") as text_file:
        text_file.write(text_formatted)

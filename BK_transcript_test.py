from youtube_transcript_api import YouTubeTranscriptApi

video_ids = ["OHf4tcgcX2M", "ANkWjOx2d3A", "CDBVdVHTr_w"]  # lista video IDs

for video_id in video_ids:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_manually_created_transcript(["pl"])
    try:
        if transcript is not None:
            lines = []
            for line in transcript.fetch():
                text = line["text"]
                start = line["start"]
                duration = line["duration"]

                line_with_timestamp = f"[{duration}] [{start}] {text}"
                lines.append(line_with_timestamp)

            text_formatted = "\n".join(lines)

            with open(f"{video_id}_transcript.txt", "w", encoding="utf-8") as text_file:
                text_file.write(text_formatted)

            print(f"Transkrypcja dla video ID {video_id} została zapisana.")
        else:
            print(f"Brak dostępnej transkrypcji po polsku dla video ID {video_id}.")
    except Exception as e:
        print(str(e))

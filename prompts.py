def get_summary_prompt(transcript):
    return f"Summarize the following YouTube video transcript in 5 bullet points:\n\n{transcript[:4000]}"

def get_timestamps_prompt(transcript):
    return f"Divide this video transcript into key sections with timestamps (estimate if exact not available):\n\n{transcript[:4000]}"

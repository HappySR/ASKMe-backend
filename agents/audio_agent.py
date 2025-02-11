from services.whisper_service import transcribe_audio
from services.gemini_service import process_text_with_gemini

async def process_audio(file, prompt: str = None):
    """
    Processes an uploaded audio file:
    - Reads the file
    - Transcribes the audio
    - Sends transcription (and optional user prompt) to Gemini
    """

    # Read the audio file as bytes
    audio_content = await file.read()

    # Transcribe the audio
    transcription_result = transcribe_audio(audio_content)

    # Debugging: Print transcription result
    print("DEBUG: Transcription Result =", transcription_result)

    if "error" in transcription_result or not transcription_result["text"]:
        return {"response": {"error": "Transcription failed or returned empty text."}}

    # Create a final prompt using user's input (if provided)
    final_prompt = f"Transcription: {transcription_result['text']}\n\n"
    if prompt:
        final_prompt += f"User Request: {prompt}\n\n"

    final_prompt += "Please provide a meaningful response based on the transcription and the user's request."

    # Send final prompt to Gemini
    response = await process_text_with_gemini(final_prompt)

    return {"response": response}

import os
import asyncio
import tempfile
import aiofiles
import traceback
import moviepy.editor as mp
from services.whisper_service import transcribe_audio
from services.gemini_service import process_text_with_gemini

async def process_video(file, prompt: str = None):
    """
    Processes an uploaded video:
    - Saves it temporarily
    - Extracts audio if available
    - Transcribes the audio
    - Sends transcription (with an optional prompt) to Gemini
    - Returns only the relevant response
    """
    print(f"🔍 Received prompt: '{prompt}'")  # Debugging

    if not prompt:
        print("⚠️ Warning: No prompt received!")  # Debugging

    temp_video_path = tempfile.mktemp(suffix=".mp4")
    temp_audio_path = None  # Initialize audio path

    try:
        # 🔹 Step 1: Save uploaded video as a temp file (efficiently)
        async with aiofiles.open(temp_video_path, "wb") as temp_file:
            while True:
                chunk = await file.read(1024 * 1024)  # ✅ Read in 1MB chunks
                if not chunk:
                    break
                await temp_file.write(chunk)

        print(f"✅ Video saved at: {temp_video_path}")  # Debugging Log

        # 🔹 Step 2: Extract audio from video
        video = await asyncio.to_thread(mp.VideoFileClip, temp_video_path)  # ✅ Offload to separate thread

        if not video.audio:
            video.close()
            return {"error": "No audio track found in the video."}

        temp_audio_path = tempfile.mktemp(suffix=".wav")
        await asyncio.to_thread(video.audio.write_audiofile, temp_audio_path)

        # Properly close resources
        video.reader.close()
        if video.audio:
            try:
                video.audio.reader.close_proc()
            except Exception as e:
                print(f"Warning: Failed to close audio reader properly: {e}")
        video.close()

        print(f"✅ Audio extracted at: {temp_audio_path}")  # Debugging Log

        # 🔹 Step 3: Transcribe audio (Ensure passing bytes if required)
        async with aiofiles.open(temp_audio_path, "rb") as audio_file:
            audio_data = await audio_file.read()  # ✅ Read file as bytes

        transcription = await asyncio.to_thread(transcribe_audio, audio_data)  # ✅ Pass bytes, not path

        if not transcription.get("text") or not transcription["text"].strip():
            return {"error": "No speech detected in the video."}

        print(f"✅ Transcription received: {transcription['text'][:100]}...")  # Debugging Log

        # 🔹 Step 4: Process transcription with Gemini
        if prompt and prompt.strip():  # ✅ Ensures prompt is non-empty and not just whitespace
            final_prompt = f"""
            You are analyzing a transcribed video speech.

            **Task:**
            - Follow the user’s request **strictly**.
            - Do **NOT** add any extra information.
            - Keep responses **concise and relevant**.

            **User Request:** {prompt}

            **Transcription:** 
            {transcription["text"]}

            Respond **only** based on the transcription and user request.
            """
        else:
            final_prompt = f"""
            The following is a transcription of a video. Extract and summarize the most relevant details.

            **Transcription:** 
            {transcription["text"]}

            Keep your response concise.
            """

        print(f"✅ Final Prompt Sent to Gemini:\n{final_prompt}\n")  # Debugging Log


        response = await process_text_with_gemini(final_prompt)  # ✅ Await for async call

        return {"response": response}

    except Exception as e:
        error_message = f"❌ Error processing video: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return {"error": str(e)}

    finally:
        # Cleanup temporary files
        for temp_path in [temp_video_path, temp_audio_path]:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                    print(f"✅ Deleted temp file: {temp_path}")  # Debugging Log
                except Exception as cleanup_error:
                    print(f"⚠️ Cleanup error: {cleanup_error}")  # Log cleanup issues

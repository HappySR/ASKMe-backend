from fastapi import FastAPI, File, UploadFile, Form
from agents.text_agent import process_text
from agents.response_translation_agent import translate_response
from agents.document_agent import process_document
from agents.audio_agent import process_audio
from agents.video_agent import process_video

app = FastAPI()

def process_and_translate(response, target_language):
    """
    If target_language is not English, translate the response.
    Otherwise, return the original response.
    """
    if target_language.lower() != "en":
        response = translate_response(response, target_language)  # ✅ Remove `await`
    return response

@app.post("/api/process_text")
async def process_text_api(
    text: str = Form(...),
    target_language: str = Form("en")
):
    response = await process_text(text, "en")
    return {"response": process_and_translate(response, target_language)}

@app.post("/api/translate_response")
async def translate_response_api(text: str, target_language: str):
    response = await translate_response(text, target_language)
    return {"response": response}

@app.post("/api/process_document")
async def process_document_api(
    file: UploadFile = File(...), 
    prompt: str = Form(None),
    target_language: str = Form("en")
):
    response = await process_document(file, prompt)
    return {"response": process_and_translate(response["response"], target_language)}

@app.post("/api/process_audio")
async def process_audio_api(
    file: UploadFile = File(...),
    prompt: str = Form(None),
    target_language: str = Form("en")
):
    response = await process_audio(file, prompt)
    return {"response": process_and_translate(response["response"], target_language)}

@app.post("/api/process_video")
async def process_video_api(
    file: UploadFile = File(...),
    prompt: str = Form(None),
    target_language: str = Form("en")
):
    response = await process_video(file, prompt)
    return {"response": process_and_translate(response["response"], target_language)}

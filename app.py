from fastapi import FastAPI, File, UploadFile, Form
from agents.text_agent import process_text
from agents.response_translation_agent import translate_response
from agents.document_agent import process_document
from agents.image_agent import process_image
from agents.audio_agent import process_audio
from agents.video_agent import process_video

app = FastAPI()

def process_and_translate(response, target_language):
    """
    If target_language is not English, translate the response.
    Otherwise, return the original response.
    """
    if target_language.lower() != "en":
        response = translate_response(response, target_language)
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
    response = translate_response(text, target_language)
    return {"response": response}

@app.post("/api/process_document")
async def process_document_api(
    file: UploadFile = File(...), 
    prompt: str = Form(None),
    target_language: str = Form("en")
):
    response = await process_document(file, prompt)

    print(f"🔍 Debug: Response from process_document -> {response}")  # Debugging Log

    # ✅ Check if 'response' key exists before accessing it
    if not response or "response" not in response:
        return {"error": f"Invalid response from document processor: {response}"}

    translated_response = process_and_translate(response["response"], target_language)
    
    return {"response": translated_response}

@app.post("/process_image/")
async def process_image_endpoint(
    image: UploadFile = File(...), 
    prompt: str = Form("Describe this image"), 
    source_lang: str = Form("auto"), 
    target_lang: str = Form("en")
):
    """
    API endpoint to process images with optional multilingual prompts.
    """
    image_data = await image.read()
    response = await process_image(image_data, prompt, source_lang, target_lang)
    return response

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

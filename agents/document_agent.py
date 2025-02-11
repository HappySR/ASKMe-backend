import fitz  # PyMuPDF for PDFs
import io
import docx
from fastapi import UploadFile
from services.gemini_service import process_text_with_gemini  # Ensure this is used

async def process_document(file: UploadFile, prompt: str = None):
    """
    Processes uploaded document files (.pdf, .docx, .txt)
    - Extracts text based on file type
    - Sends to Gemini for processing (optional prompt)
    """
    
    # Read the file
    content = await file.read()
    file_ext = file.filename.split(".")[-1].lower()
    
    # Debugging log
    print(f"📄 Processing document: {file.filename} (Type: {file_ext})")

    extracted_text = ""

    try:
        if file_ext == "pdf":
            doc = fitz.open(stream=content, filetype="pdf")  
            extracted_text = "\n".join([page.get_text("text") for page in doc])

        elif file_ext == "docx":
            doc = docx.Document(io.BytesIO(content))  # Open .docx in memory
            extracted_text = "\n".join([para.text for para in doc.paragraphs])

        elif file_ext == "txt":
            extracted_text = content.decode("utf-8").strip()

        else:
            return {"error": "Unsupported file type. Please upload PDF, DOCX, or TXT."}

        if not extracted_text.strip():
            return {"error": "No readable text found in the document."}

        print(f"✅ Extracted text: {extracted_text[:100]}...")  # Debugging Log

        # 🔹 Step 2: Process with Gemini (like video & audio)
        if prompt and prompt.strip():
            final_prompt = f"""
            You are analyzing a document.

            **Task:**
            - Follow the user’s request **strictly**.
            - Do **NOT** add any extra information.
            - Keep responses **concise and relevant**.

            **User Request:** {prompt}

            **Document Content:**
            {extracted_text}

            Respond **only** based on the document content and user request.
            """
        else:
            final_prompt = f"""
            The following is a document. Extract and summarize the most relevant details.

            **Document Content:**
            {extracted_text}

            Keep your response concise.
            """

        print(f"✅ Final Prompt Sent to Gemini:\n{final_prompt}\n")  # Debugging Log

        response = await process_text_with_gemini(final_prompt)  # Call Gemini

        return {"response": response}

    except Exception as e:
        return {"error": f"Error processing document: {str(e)}"}

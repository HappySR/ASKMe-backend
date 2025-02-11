# **ASKMe Backend** 🧠💬  

This is the backend service for **ASKMe**, a powerful AI-driven conversational assistant that supports **text, documents, audio, and video processing**. It integrates **Google Gemini AI**, **LibreTranslate**, and **Whisper** to provide intelligent responses, translations, and transcriptions.

## 🚀 Features  
- ✅ **Text Processing**: Understands and responds to text-based queries.  
- 📄 **Document Analysis**: Extracts and processes text from **PDF, DOCX, and TXT** files.  
- 🎙 **Audio Processing**: Transcribes and analyzes audio files using **Whisper AI**.  
- 🎥 **Video Processing**: Extracts audio from video files, transcribes it, and processes it via **Gemini AI**.  
- 🌍 **Translation Support**: Detects language and translates responses using **LibreTranslate**.  
- 🔥 **FastAPI-based API**: A robust, asynchronous backend built with **FastAPI**.  

---

## 📌 **Installation**  

### 1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/YOUR_USERNAME/askme-backend.git
cd askme-backend
```

### 2️⃣ Set Up the Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create a .env File

Create a .env file in the root directory and add the following:

```bash
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
LIBRETRANSLATE_URL="http://localhost:5000" # Example LibreTranslate instance
```

## 🛠 Usage
### 1️⃣ Run the Server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

This starts the FastAPI server on http://127.0.0.1:8000/.
### 2️⃣ API Endpoints
#### 📌 Process Text Input

```bash
POST /api/process_text
```

    • Description: Processes a text query and returns a response.
    • Request Body:

```bash
{
  "text": "What is the capital of France?",
  "target_language": "fr"
}
```

• Response:

```bash
    {
      "response": "La capitale de la France est Paris."
    }
```

#### 📌 Process Document (PDF, DOCX, TXT)

```bash
POST /api/process_document
```

    • Description: Extracts and processes text from a document.
    • Request Example (Using cURL):

```bash
curl -X 'POST' 'http://127.0.0.1:8000/api/process_document' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@document.pdf' \
  -F 'prompt=Summarize this document' \
  -F 'target_language=en'
```

• Response Example:

```bash
    {
      "response": "This document discusses the effects of climate change on global agriculture."
    }
```

## 🎙 Process Audio (MP3, WAV, FLAC)

```bash
POST /api/process_audio
```

    • Description: Transcribes an audio file and sends it to Gemini AI.
    • Request Example:

```bash
curl -X 'POST' 'http://127.0.0.1:8000/api/process_audio' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@speech.wav' \
  -F 'prompt=Summarize this speech'
```

• Response Example:

```bash
    {
      "response": "The speaker discusses the importance of AI in modern education."
    }
```

## 🎥 Process Video (MP4, MOV, AVI)

```bash
POST /api/process_video
```

    • Description: Extracts audio from a video, transcribes it, and processes it via Gemini AI.
    • Request Example:

```bash
curl -X 'POST' 'http://127.0.0.1:8000/api/process_video' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@lecture.mp4' \
  -F 'prompt=Summarize the key points'
```

• Response Example:

```bash
    {
      "response": "The lecture explains Newton's three laws of motion with examples."
    }
```

## ⚙️ Project Structure

```bash
askme-backend/
│── agents/
│   ├── audio_agent.py        # Handles audio processing
│   ├── document_agent.py     # Handles document analysis
│   ├── video_agent.py        # Handles video processing
│
│── services/
│   ├── gemini_service.py     # Manages communication with Gemini AI
│   ├── whisper_service.py    # Transcribes speech using Whisper
│   ├── libretranslate_service.py  # Handles translation
│
│── app.py                    # Main FastAPI application
│── requirements.txt           # Python dependencies
│── .env                       # API keys & environment variables
│── README.md                  # This file
```

## 🎯 Future Improvements

    🏆 Support for more file types (PPTX, EPUB, etc.)
    🔥 Real-time transcription for live audio/video streams
    🌍 Improved multilingual support
    ⚡ Better caching for faster responses

## 🤝 Contributing

We welcome contributions! 🎉
To contribute:

    Fork the repository
    Create a new branch: git checkout -b feature-name
    Make your changes and commit: git commit -m "Added new feature"
    Push to your branch: git push origin feature-name
    Create a Pull Request

## 📜 License

This project is licensed under the MIT License.
🛠 Developed By

💡 Subhajit Roy
🚀 Connect with me: [GitHub](https://github.com/YOUR_GITHUB_USERNAME) | [LinkedIn](https://www.linkedin.com/in/YOUR_LINKEDIN_USERNAME)
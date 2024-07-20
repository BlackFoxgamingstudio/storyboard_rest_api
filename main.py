from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import openai
import os
from typing import Dict

app = FastAPI()

# MongoDB connection details (update if necessary)
client = MongoClient("mongodb+srv://blackloin:naruto45@cluster0.fmktl.mongodb.net/?retryWrites=true&w=majority")
db = client['keytechlabs']
components_collection = db['components_collection']

# Configure CORS
allowed_origins = [
    "https://blackfoxgamingstudio.github.io",
    "https://blackfoxgamingstudio.github.io/storyboard_rest_api/",
    "https://blackfoxgamingstudio.github.io/storyboard_rest_api",
    "http://localhost:8080",
    "https://googleusercontent.com",
    "https://1509109279-atari-embeds.googleusercontent.com/"
    "https://sites.google.com/view/russellpowersskillsportfolio/storyboard",
    "*",  # Allow all origins for testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Upload Directory
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper Function to Check Allowed File Types
def allowed_file(filename: str) -> bool:
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/generate_image")
async def generate_image(request: Request):
    data = await request.json()

    
    prompt = data
    response = openai.images.generate(
    model="dall-e-3",
    prompt="for the story, show the next secne: " +prompt,
    size="1024x1024",
    quality="hd",
    n=1
    )
    image_url = response.data[0].url
    return {"url": image_url}

@app.post("/upload_document")
async def upload_document(file: bytes, filename: str):
    if not file or not filename:
        raise HTTPException(status_code=400, detail="File and filename are required")
    if not allowed_file(filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as f:
        f.write(file)
    return {"success": "File uploaded and processed successfully"}

@app.post("/generate_story")
async def generate_story(story_details: Dict):
    title = story_details.get('title', '')
    genre = story_details.get('genre', '')
    characters = story_details.get('characters', '')
    setting = story_details.get('setting', '')
    plot = story_details.get('plot', '')
    conflict = story_details.get('conflict', '')
    resolution = story_details.get('resolution', '')
    additional = story_details.get('additional', '')

    story = f"Title: {title}\nGenre: {genre}\nCharacters: {characters}\nSetting: {setting}\nPlot: {plot}\nConflict: {conflict}\nResolution: {resolution}\nAdditional: {additional}"
    return {"story": story}

@app.post("/generate_next_chapter")
async def generate_next_chapter(story_id: str):
    next_chapter = "This is the next chapter of your story."
    return {"next_chapter": next_chapter}

@app.post("/generate_3d_model")
async def generate_3d_model(variables: Dict):
    economic_factors = variables.get('economicFactors', [])
    creative_culture = variables.get('creativeCulture', [])
    knowledge_points = variables.get('knowledgePoints', [])
    model_url = "http://example.com/3d_model.png"
    return FileResponse(model_url)

@app.post("/add_character")
async def add_character(character_data: Dict):
    character_name = character_data.get('characterName', '')
    attributes = character_data.get('attributes', {})
    return {"success": f"Character {character_name} added/updated successfully"}

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(app, host="0.0.0.0", port=8000)

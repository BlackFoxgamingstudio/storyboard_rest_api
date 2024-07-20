import os
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import openai
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient



app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# MongoDB connection
client = MongoClient("mongodb+srv://blackloin:naruto45@cluster0.fmktl.mongodb.net/?retryWrites=true&w=majority")
db = client['test']  # Assuming 'keytechlabs' is the correct database
components_collection = db['components_collection']
checklist_tech_collection = db['keytechlabs.Checklist_tech']
powershell_checklist_collection = db['keytechlabs.powershell_Checklist']
image_collection = db['keytechlabs.image_collection']



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}
openai.api_key = 'sk-proj-lUTO4mEBYhFfbcq0qkZ9T3BlbkFJRn8ohuhf3wzPpgD7Rm4i'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.json.get('prompt', '')
    response = openai.images.generate(
    model="dall-e-3",
    prompt="for the story, show the next secne: " +prompt,
    size="1024x1024",
    quality="hd",
    n=1
    )
    image_url = response.data[0].url
    return jsonify({'url': image_url})

@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Here you would process the file and extract prompts
        return jsonify({'success': 'File uploaded and processed successfully'})
    return jsonify({'error': 'File type not allowed'})

@app.route('/generate_story', methods=['POST'])
def generate_story():
    story_details = request.json
    title = story_details.get('title', '')
    genre = story_details.get('genre', '')
    characters = story_details.get('characters', '')
    setting = story_details.get('setting', '')
    plot = story_details.get('plot', '')
    conflict = story_details.get('conflict', '')
    resolution = story_details.get('resolution', '')
    additional = story_details.get('additional', '')
    
    # Here you would generate the story based on the details provided
    story = f"Title: {title}\nGenre: {genre}\nCharacters: {characters}\nSetting: {setting}\nPlot: {plot}\nConflict: {conflict}\nResolution: {resolution}\nAdditional: {additional}"
    
    return jsonify({'story': story})

@app.route('/generate_next_chapter', methods=['POST'])
def generate_next_chapter():
    story_id = request.json.get('story_id', '')
    # Here you would generate the next chapter based on the story_id
    next_chapter = "This is the next chapter of your story."
    
    return jsonify({'next_chapter': next_chapter})

@app.route('/generate_3d_model', methods=['POST'])
def generate_3d_model():
    variables = request.json
    economic_factors = variables.get('economicFactors', [])
    creative_culture = variables.get('creativeCulture', [])
    knowledge_points = variables.get('knowledgePoints', [])
    
    # Here you would generate the 3D model based on the variables provided
    model_url = "http://example.com/3d_model.png"
    
    return send_file(model_url)

@app.route('/add_character', methods=['POST'])
def add_character():
    character_data = request.json
    character_name = character_data.get('characterName', '')
    attributes = character_data.get('attributes', {})
    
    # Here you would save the character attributes
    return jsonify({'success': f'Character {character_name} added/updated successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5081)

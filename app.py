from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os

app = Flask(__name__, static_folder='.')

# 🔑 PASTE YOUR GOOGLE GEMINI API KEY HERE! this is moomin api key isko latter change krna hai
GEMINI_API_KEY = "AIzaSyAdrfCqUXWtklz14c4pQQ1P63h9N2dgf50"

# Configure Gemini once
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-2.0-flash-exp')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('.', path)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    gene_name = data.get('gene', '').strip()
    dna_code = data.get('dna', '').strip()

    if not gene_name or not dna_code:
        return jsonify({"error": "Please fill both fields!"}), 400

    try:
        prompt = f"""
        You are a medical genetics expert.
        Normal Gene: {gene_name}
        Patient's DNA Sequence: {dna_code}

        Please explain:
        1. first check if the normal gene is actually a gene, if it is not a gene and anything else than a gene name display error message "this gene doesn't exist".
        2. What genetic disease this might indicate.
        3. How this sequence differs from normal.
        4. What treatments or management options exist.
        5. if the pateint's DNA sequence does't match to the noraml gene or a disease related to the normal gene display an error message"this DNA sequence doesn't match our database".

        Keep it simple, clear, to the point no extra information and under 300 words.
        """

        response = model.generate_content(prompt)
        return jsonify({"answer": response.text.strip()})

    except Exception as e:
        return jsonify({"error": f"AI Error: {str(e)}"}), 500

@app.route('/disorder-info', methods=['POST'])
def disorder_info():
    data = request.get_json()
    disorder_name = data.get('disorder', '').strip()

    if not disorder_name:
        return jsonify({"error": "Please enter a disorder name!"}), 400

    try:
        prompt = f"""
        You are a medical genetics expert. Please provide comprehensive information about the genetic disorder: {disorder_name}

        Include:
        1. Overview and description
        2. Genetic cause (which gene(s) are affected)
        3. Inheritance pattern
        4. Common symptoms
        5. Diagnosis methods
        6. Treatment options
        7. Prognosis

        Format the response clearly with sections. Keep it informative but accessible to non-specialists, if the disorder isn't an actual known disorder or is anything else than a genetic disorder display error message "DISORDER DOESN'T EXIST".
        """

        response = model.generate_content(prompt)
        return jsonify({"answer": response.text.strip()})

    except Exception as e:
        return jsonify({"error": f"AI Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

def load_nasa_data():
    """
    Carga los datos desde nasadata.jsonl
    """
    jsonl_path = os.path.join(os.path.dirname(__file__), 'nasadata.jsonl')
    data = []
    
    with open(jsonl_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                data.append(json.loads(line))
    
    return data

@app.route('/api/articles', methods=['GET'])
def get_articles():
    try:
        data = load_nasa_data()
        
        articles = []
        for idx, item in enumerate(data):
            parts = item['input_text'].split(' | ')
            
            title = parts[0] if len(parts) > 0 else ""
            url = parts[1] if len(parts) > 1 else ""
            description = parts[2] if len(parts) > 2 else ""
            category = item['output_text']
            
            articles.append({
                'id': idx + 1,
                'title': title,
                'url': url,
                'description': description,
                'category': category
            })
        
        return jsonify({'success': True, 'articles': articles})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import os

app = Flask(__name__)
CORS(app)

credentials_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                'nasaappschallenge-474115-7e9223349475.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

connector = Connector()

def get_db_connection():
    conn = connector.connect(
        "nasaappschallenge-474115:us-central1:nasapps",
        "pymysql",
        user="wurs",
        password="wursthannover123",
        db="ArticlesData",
        ip_type=IPTypes.PUBLIC
    )
    return conn

@app.route('/api/articles', methods=['GET'])
def get_articles():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute('''
            SELECT a.id, a.title, a.url, a.description, c.name as category
            FROM articles a
            JOIN category c ON a.category_id = c.id
            ORDER BY a.id
        ''')
        
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'articles': articles})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute('''
            SELECT c.id, c.name, COUNT(a.id) as article_count
            FROM category c
            LEFT JOIN articles a ON c.id = a.category_id
            GROUP BY c.id, c.name
            ORDER BY c.name
        ''')
        
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'categories': categories})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)

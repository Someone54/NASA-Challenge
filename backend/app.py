from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import os

app = Flask(__name__)
CORS(app)

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
            SELECT id, title, url, description, category_id as category
            FROM articles
            ORDER BY id
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
            SELECT DISTINCT category_id as id, category_id as name, COUNT(*) as article_count
            FROM articles
            GROUP BY category_id
            ORDER BY category_id
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

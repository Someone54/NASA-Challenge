from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud.sql.connector import Connector, IPTypes
import os
import csv
import json

app = Flask(__name__)
CORS(app)

# Construye la ruta al archivo de credenciales en la carpeta raíz del proyecto
credentials_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nasaappschallenge-474115-698d077518cf.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Inicializa el conector de Cloud SQL
connector = Connector()

def get_db_connection():
    """
    Establece una conexión segura a la base de datos de Cloud SQL
    usando el Cloud SQL Python Connector.
    """
    conn = connector.connect(
        "nasaappschallenge-474115:us-central1:nasapps", # <-- PEGA AQUÍ EL "NOMBRE DE CONEXIÓN DE LA INSTANCIA"
        "mysql.connector", # Indica que usamos la librería mysql-connector-python
        user="wurs",
        password="nasapps",
        db="ArticlesData",
        ip_type=IPTypes.PUBLIC # Asegúrate de que tu instancia tiene IP pública habilitada
    )
    return conn

@app.route('/api/populate-database', methods=['POST'])
def populate_database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(500) UNIQUE NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cluster_id INT,
                category_id INT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY (category_id) REFERENCES category(id)
            )
        ''')
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                'SB_publication_categorizado_NASA_temas.csv')
        
        categories_set = set()
        articles_data = []
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                categories_set.add(row['Categoria_Nombre'])
                articles_data.append(row)
        
        category_ids = {}
        for category_name in categories_set:
            cursor.execute(
                "INSERT IGNORE INTO category (name) VALUES (%s)",
                (category_name,)
            )
            cursor.execute(
                "SELECT id FROM category WHERE name = %s",
                (category_name,)
            )
            result = cursor.fetchone()
            category_ids[category_name] = result[0]
        
        for article in articles_data:
            category_id = category_ids[article['Categoria_Nombre']]
            cursor.execute(
                '''INSERT INTO articles (cluster_id, category_id, title, url, description) 
                   VALUES (%s, %s, %s, %s, %s)''',
                (
                    int(article['Cluster_ID']),
                    category_id,
                    article['Title'],
                    article['Link'],
                    article['Title'][:200] + '...' if len(article['Title']) > 200 else article['Title']
                )
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Database populated with {len(categories_set)} categories and {len(articles_data)} articles'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
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

@app.route('/api/articles', methods=['GET'])
def get_articles():
    try:
        category_id = request.args.get('category_id')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        if category_id:
            cursor.execute('''
                SELECT a.id, a.title, a.url, a.description, c.name as category
                FROM articles a
                JOIN category c ON a.category_id = c.id
                WHERE a.category_id = %s
                ORDER BY a.title
            ''', (category_id,))
        else:
            cursor.execute('''
                SELECT a.id, a.title, a.url, a.description, c.name as category
                FROM articles a
                JOIN category c ON a.category_id = c.id
                ORDER BY a.title
            ''')
        
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'articles': articles})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/article/<int:article_id>', methods=['GET'])
def get_article(article_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT a.id, a.title, a.url, a.description, c.name as category
            FROM articles a
            JOIN category c ON a.category_id = c.id
            WHERE a.id = %s
        ''', (article_id,))
        
        article = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if article:
            return jsonify({'success': True, 'article': article})
        else:
            return jsonify({'success': False, 'error': 'Article not found'}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

import mysql.connector
import csv
import os

DB_CONFIG = {
    'host': '34.29.39.61',
    'user': 'wurs',
    'password': 'nasapps',
    'database': 'ArticlesData'
}

def create_tables(cursor):
    print("📋 Creating tables...")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(500) UNIQUE NOT NULL
        )
    ''')
    print("✅ Table 'category' created/verified")
    
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
    print("✅ Table 'articles' created/verified")

def load_csv_data():
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'SB_publication_categorizado_NASA_temas.csv'
    )
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    print(f"📂 Reading CSV from: {csv_path}")
    
    categories_set = set()
    articles_data = []
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            categories_set.add(row['Categoria_Nombre'])
            articles_data.append(row)
    
    print(f"📊 Found {len(categories_set)} unique categories")
    print(f"📄 Found {len(articles_data)} articles")
    
    return categories_set, articles_data

def insert_categories(cursor, categories_set):
    print("\n📥 Inserting categories...")
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
    
    print(f"✅ {len(category_ids)} categories inserted")
    return category_ids

def insert_articles(cursor, articles_data, category_ids):
    print("\n📥 Inserting articles...")
    
    for idx, article in enumerate(articles_data, 1):
        category_id = category_ids[article['Categoria_Nombre']]
        
        title = article['Title']
        description = title[:200] + '...' if len(title) > 200 else title
        
        cursor.execute(
            '''INSERT INTO articles (cluster_id, category_id, title, url, description) 
               VALUES (%s, %s, %s, %s, %s)''',
            (
                int(article['Cluster_ID']),
                category_id,
                title,
                article['Link'],
                description
            )
        )
        
        if idx % 100 == 0:
            print(f"  ⏳ Inserted {idx}/{len(articles_data)} articles...")
    
    print(f"✅ {len(articles_data)} articles inserted")

def main():
    print("🚀 NASA Bioscience Database Setup")
    print("=" * 50)
    
    try:
        print("\n🔌 Connecting to database...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✅ Connected successfully")
        
        create_tables(cursor)
        
        categories_set, articles_data = load_csv_data()
        
        category_ids = insert_categories(cursor, categories_set)
        
        insert_articles(cursor, articles_data, category_ids)
        
        conn.commit()
        print("\n💾 Changes committed to database")
        
        cursor.close()
        conn.close()
        print("✅ Database connection closed")
        
        print("\n" + "=" * 50)
        print("🎉 Database setup completed successfully!")
        print(f"📊 Total categories: {len(categories_set)}")
        print(f"📄 Total articles: {len(articles_data)}")
        
    except mysql.connector.Error as e:
        print(f"\n❌ Database error: {e}")
        print("\nPlease check:")
        print("  - Database host, user, and password are correct")
        print("  - Database 'ArticlesData' exists")
        print("  - You have proper permissions")
        return 1
        
    except FileNotFoundError as e:
        print(f"\n❌ File error: {e}")
        print("\nMake sure the CSV file exists at:")
        print("  NASA-Challenge/SB_publication_categorizado_NASA_temas.csv")
        return 1
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())

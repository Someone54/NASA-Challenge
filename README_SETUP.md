

# NASA Bioscience Articles - Setup Guide

## Project Overview
This application displays NASA bioscience research articles organized by categories. It consists of:
- **Backend API** (Flask/Python) - Manages database operations and exposes REST endpoints
- **Frontend** (HTML/CSS/JavaScript) - Displays categories and articles in an intuitive card layout

## Prerequisites
- Python 3.8+
- MySQL database (Google Cloud SQL)
- Google Cloud credentials file

## Installation Steps

### 1. Backend Setup

#### Create and Activate a Virtual Environment (Recommended)
This isolates project dependencies and prevents conflicts.
```bash
# Create the environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Configure Database Connection:
Make sure the `nasaappschallenge-474115-5c59de3642ff.json` file is in the root directory.

Update `DB_CONFIG` in `backend/app.py` if needed:
```python
```

#### Run the Backend Server:
```bash
cd backend
python app.py
```
The API will run on `http://localhost:5000`

### 2. Populate Database

Once the backend is running, populate the database with CSV data:

**Option 1: Using curl (Windows PowerShell)**
```powershell
curl -X POST http://localhost:5000/api/populate-database
```

**Option 2: Using Python**
```python
import requests
response = requests.post('http://localhost:5000/api/populate-database')
print(response.json())
```

**Option 3: Using browser**
Create a simple HTML file or use the browser console:
```javascript
fetch('http://localhost:5000/api/populate-database', {
    method: 'POST'
}).then(r => r.json()).then(console.log);
```

### 3. Frontend Setup

#### Serve the Frontend:

**Option 1: Using Python's built-in server**
```bash
cd frontend
python -m http.server 8000
```
Open `http://localhost:8000` in your browser

**Option 2: Using VS Code Live Server**
- Install "Live Server" extension
- Right-click on `frontend/index.html`
- Select "Open with Live Server"

**Option 3: Open directly**
- Simply double-click `frontend/index.html`
- Note: CORS might be an issue with this method

## API Endpoints

### GET /api/categories
Returns all categories with article counts
```json
{
  "success": true,
  "categories": [
    {
      "id": 1,
      "name": "Biología Espacial y Humana",
      "article_count": 150
    }
  ]
}
```

### GET /api/articles?category_id={id}
Returns articles for a specific category
```json
{
  "success": true,
  "articles": [
    {
      "id": 1,
      "title": "Article Title",
      "url": "https://...",
      "description": "Article description",
      "category": "Category Name"
    }
  ]
}
```

### GET /api/article/{id}
Returns a single article by ID

### POST /api/populate-database
Populates database from CSV file

## Project Structure

```
NASA-Challenge/
├── backend/
│   ├── app.py                 # Flask application with API endpoints
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html            # Main HTML structure
│   ├── styles.css            # Styling and responsive design
│   └── app.js                # JavaScript for API consumption
├── SB_publication_categorizado_NASA_temas.csv  # Data source
├── nasaappschallenge-474115-5c59de3642ff.json  # GCP credentials
└── README_SETUP.md           # This file
```

## Features Implemented

✅ Backend API with Flask
✅ Google Cloud SQL database integration
✅ CSV data import endpoint
✅ REST API endpoints for categories and articles
✅ Responsive card-based frontend
✅ Category browsing
✅ Article listing by category
✅ Direct links to full articles
✅ Error handling and loading states
✅ CORS support for frontend-backend communication

## Troubleshooting

### Backend won't start
- Verify Python dependencies are installed: `pip install -r requirements.txt`
- Check database credentials and connectivity
- Ensure port 5000 is not in use

### Frontend can't connect to API
- Verify backend is running on port 5000
- Check browser console for CORS errors
- Ensure `API_BASE_URL` in `app.js` matches your backend URL

### Database population fails
- Verify CSV file path is correct
- Check database permissions
- Ensure tables don't already exist or drop them first

## Next Steps

1. ✅ Basic functionality complete
2. 🔄 Add AI-powered article summaries using Google Cloud AI
3. 🔄 Implement user authentication
4. 🔄 Add search functionality
5. 🔄 Add pagination for large result sets
6. 🔄 Deploy to production

## Tech Stack

- **Backend**: Flask (Python) - Simple and easy to understand for junior developers
- **Database**: MySQL (Google Cloud SQL)
- **Frontend**: Vanilla HTML/CSS/JavaScript - No complex frameworks, easy to learn
- **Styling**: Custom CSS with modern features (Grid, Flexbox)

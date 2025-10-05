gcloud run deploy nasa-backend-service --source . --platform managed --region us-central1 --allow-unauthenticated --add-cloudsql-instances nasaappschallenge-474115:us-central1:nasapps


# NASA Bioscience Articles - Deployment Guide

## Project Overview
This application displays NASA bioscience research articles from a Google Cloud SQL database. It consists of:
- **Backend API** (Flask/Python) - Deployed on Google Cloud Run, connects to Cloud SQL
- **Frontend** (HTML/CSS/JavaScript) - Deployed on GitHub Pages as a static site

## Architecture
- **Database**: Google Cloud SQL (MySQL) - Stores articles and categories
- **Backend**: Google Cloud Run - Serverless API that queries the database
- **Frontend**: GitHub Pages - Static site that consumes the API

## Prerequisites
- Google Cloud account with billing enabled
- GitHub account
- Google Cloud SDK installed (`gcloud` CLI)
- Git installed

## Deployment Steps

### 1. Deploy Backend to Google Cloud Run

The backend needs to be deployed to Google Cloud Run to be accessible from GitHub Pages.

#### Step 1: Authenticate with Google Cloud
```bash
gcloud auth login
gcloud config set project nasaappschallenge-474115
```

#### Step 2: Enable Required APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

#### Step 3: Deploy to Cloud Run
```bash
cd backend

# Build and deploy in one command
gcloud run deploy nasa-backend-service \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --add-cloudsql-instances nasaappschallenge-474115:us-central1:nasapps
```

#### Step 4: Get Your Backend URL
After deployment, you'll see a URL like:
```
https://nasa-backend-service-XXXXX-uc.a.run.app
```

Copy this URL - you'll need it for the frontend configuration.

### 2. Configure Frontend for Production

#### Step 1: Update API URL
Edit `frontend/config.js` and replace the production API URL:
```javascript
const CONFIG = {
    production: {
        API_URL: 'https://nasa-backend-service-XXXXX-uc.a.run.app/api'  // Replace with your URL
    },
    development: {
        API_URL: 'http://localhost:8080/api'
    }
};
```

### 3. Deploy Frontend to GitHub Pages

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main
```

#### Step 2: Enable GitHub Pages
1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Source", select **Deploy from a branch**
4. Select branch: **main** and folder: **/ (root)** or **/frontend**
5. Click **Save**

#### Step 3: Access Your Site
Your site will be available at:
```
https://YOUR-USERNAME.github.io/NASA-Challenge/frontend/
```

Or if you configured a custom domain:
```
https://your-custom-domain.com
```

### 4. Testing the Deployment

1. Open your GitHub Pages URL
2. You should see articles loading from the Google Cloud SQL database
3. Check browser console (F12) for any errors
4. Verify the API URL is correct in the console logs

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

## Local Development (Optional)

If you want to test locally before deploying:

### Run Backend Locally
```bash
cd backend
pip install -r requirements.txt
python app.py
```
The API runs on `http://localhost:8080`

### Test Frontend Locally
```bash
cd frontend
python -m http.server 3000
```
Open `http://localhost:3000` in your browser

## Troubleshooting

### CORS Errors
- Verify your Cloud Run service allows unauthenticated requests
- Check that CORS is properly configured in `app.py`
- Ensure the API URL in `config.js` is correct

### Backend Deployment Fails
- Verify Google Cloud credentials are correct
- Check that Cloud SQL instance is running
- Ensure `nasaappschallenge-474115-7e9223349475.json` is in the backend folder
- Check Cloud Run logs: `gcloud run logs read nasa-backend-service`

### Frontend Shows "Error loading articles"
- Open browser console (F12) and check for errors
- Verify the API URL in `config.js` matches your Cloud Run URL
- Test the API directly: `curl https://YOUR-CLOUD-RUN-URL/api/articles`
- Check that Cloud SQL database has data

### GitHub Pages Not Updating
- Wait 2-5 minutes after pushing changes
- Clear browser cache (Ctrl+Shift+R)
- Check GitHub Actions for deployment errors

## Deployment Checklist

- [ ] Google Cloud SQL database is populated with articles
- [ ] Backend deployed to Cloud Run
- [ ] Cloud Run URL copied
- [ ] `frontend/config.js` updated with Cloud Run URL
- [ ] Frontend pushed to GitHub
- [ ] GitHub Pages enabled
- [ ] Site accessible and loading articles

## Cost Considerations

- **Google Cloud SQL**: ~$10-30/month (depending on instance size)
- **Cloud Run**: Pay-per-use, free tier includes 2 million requests/month
- **GitHub Pages**: Free for public repositories

To minimize costs:
- Use Cloud SQL's smallest instance type
- Set up automatic backups only if needed
- Consider pausing Cloud SQL when not in use (requires manual restart)

## Next Steps

1. ✅ Database populated with articles
2. ✅ Backend deployed to Cloud Run
3. ✅ Frontend deployed to GitHub Pages
4. 🔄 Add custom domain (optional)
5. 🔄 Add AI-powered article summaries
6. 🔄 Implement search and filtering
7. 🔄 Add analytics tracking

## Tech Stack

- **Database**: MySQL (Google Cloud SQL) - Stores articles and categories
- **Backend**: Flask (Python) on Google Cloud Run - Serverless, auto-scaling API
- **Frontend**: Vanilla HTML/CSS/JavaScript on GitHub Pages - Fast, free static hosting
- **Styling**: Custom CSS with Grid/Flexbox - Responsive design




# 1. Agregar el repositorio de Google Cloud
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# 2. Importar la clave pública de Google Cloud
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# 3. Actualizar e instalar
sudo apt-get update && sudo apt-get install google-cloud-cli

# 4. Inicializar gcloud
gcloud init

sudo snap install google-cloud-cli --classic
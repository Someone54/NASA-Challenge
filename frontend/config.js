const CONFIG = {
    production: {
        API_URL: 'https://YOUR-CLOUD-RUN-URL.run.app/api'
    },
    development: {
        API_URL: 'http://localhost:8000/api'
    }
};

const IS_PRODUCTION = window.location.hostname !== 'localhost' && 
                      window.location.hostname !== '127.0.0.1' &&
                      !window.location.hostname.includes('192.168');

const API_BASE_URL = IS_PRODUCTION ? CONFIG.production.API_URL : CONFIG.development.API_URL;

console.log('Environment:', IS_PRODUCTION ? 'Production' : 'Development');
console.log('API URL:', API_BASE_URL);

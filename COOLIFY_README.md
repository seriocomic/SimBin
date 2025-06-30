# Coolify Configuration for Simbin Django App

## Environment Variables (set these in Coolify)

### Required
- SECRET_KEY: Django secret key for production
- ALLOWED_HOSTS: Comma-separated list of allowed hosts (e.g., yourdomain.com,www.yourdomain.com)

### Optional
- DEBUG: Set to 'false' for production (default: true)
- DATABASE_URL: PostgreSQL connection string (format: postgres://user:password@host:port/dbname)

## Configuration Notes

Default configuration uses SQLite if no DATABASE_URL is provided

Health Check Endpoint: /health/
This endpoint returns JSON with status information for monitoring

Static Files:
Static files are served using WhiteNoise middleware
All static files will be collected and served from /staticfiles/

## Deployment Notes

1. Set environment variables in Coolify dashboard
2. Ensure PORT environment variable is set to 8000 (default for Django)
3. The app will automatically run database migrations on startup
4. Static files are collected during Docker build process

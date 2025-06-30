# Simbin Django App - Coolify Deployment Guide

This Django application (Simbin) is now ready for deployment to Coolify.

## Prerequisites

- Coolify instance running
- Git repository with this code
- Domain name (optional but recommended)

## Deployment Steps

### 1. Create a New Service in Coolify

1. Log into your Coolify dashboard
2. Create a new service
3. Choose "Docker Compose" or "Dockerfile" deployment type
4. Connect your Git repository

### 2. Environment Variables

Set these environment variables in Coolify:

**Required:**

- `SECRET_KEY`: A secure Django secret key (generate a new one for production - minimum 50 characters)
- `ALLOWED_HOSTS`: Your domain(s), comma-separated (e.g., `example.com,www.example.com`)

**Optional:**

- `DEBUG`: Set to `false` for production (default: `true`)
- `DATABASE_URL`: PostgreSQL connection string if using external database

### 3. Configuration

This application is **database-free** and stateless, making deployment extremely simple. No additional database configuration is needed.

### 4. Domain and SSL

1. Add your domain in Coolify service settings
2. Enable SSL certificate (Let's Encrypt)
3. Update `ALLOWED_HOSTS` environment variable with your domain

### 5. Health Check

The application includes a health check endpoint at `/health/` that returns:
```json
{"status": "healthy", "message": "Simbin is running"}
```

## Post-Deployment

1. Verify the application is running by visiting your domain
2. Check the `/health/` endpoint for monitoring
3. Test the main functionality

## File Structure for Coolify

```
├── Dockerfile              # Container configuration (Python 3.13)
├── docker-compose.yml      # Local development setup
├── entrypoint.sh           # Startup script with migrations
├── requirements.txt        # Python dependencies (latest stable)
├── .dockerignore          # Docker build exclusions
├── .env.example           # Environment variable template
├── .python-version        # Python version specification
├── upgrade_environment.sh  # Environment upgrade script
└── COOLIFY_README.md      # Coolify-specific configuration notes
```

## Troubleshooting

- Check Coolify logs if deployment fails
- Ensure all required environment variables are set
- Verify domain DNS settings if using custom domain
- Check health endpoint: `https://yourdomain.com/health/`

## Security Notes

- Generate a new `SECRET_KEY` for production
- Set `DEBUG=false` in production
- Use HTTPS in production
- Consider using PostgreSQL for production databases
- Regularly update dependencies

## Local Development

To run locally with Docker:

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your local settings
nano .env

# Run with Docker Compose
docker-compose up --build
```

The application will be available at `http://localhost:8881`

# Social Media API

A comprehensive Django REST API for a social media platform with user authentication, posts, comments, following system, notifications, and likes functionality.

## Features

### Task 0: User Authentication

- Custom user model with bio, profile picture, and followers
- Token-based authentication
- User registration and login endpoints
- User profile management

### Task 1: Posts and Comments

- CRUD operations for posts and comments
- Permission-based access (users can only edit their own content)
- Pagination and filtering capabilities
- Search functionality for posts

### Task 2: User Follows and Feed

- Follow/unfollow other users
- Personalized feed showing posts from followed users
- Many-to-many relationship for user following

### Task 3: Notifications and Likes

- Like/unlike posts functionality
- Comprehensive notification system for follows, likes, and comments
- Real-time notifications for user interactions

### Task 4: Production Ready

- Production settings configuration
- Static files handling with WhiteNoise
- Database configuration for PostgreSQL
- Security settings and HTTPS support
- Deployment scripts and configuration

## API Endpoints

### Authentication

- `POST /register/` - User registration
- `POST /login/` - User login
- `GET/PUT /profile/` - User profile management

### User Management

- `POST /follow/<user_id>/` - Follow a user
- `POST /unfollow/<user_id>/` - Unfollow a user

### Posts

- `GET /posts/` - List all posts (with pagination)
- `POST /posts/` - Create a new post
- `GET /posts/<id>/` - Retrieve a specific post
- `PUT/PATCH /posts/<id>/` - Update a post (author only)
- `DELETE /posts/<id>/` - Delete a post (author only)
- `GET /feed/` - Get personalized feed

### Comments

- `GET /comments/` - List all comments
- `POST /comments/` - Create a new comment
- `GET /comments/<id>/` - Retrieve a specific comment
- `PUT/PATCH /comments/<id>/` - Update a comment (author only)
- `DELETE /comments/<id>/` - Delete a comment (author only)

### Likes

- `POST /posts/<id>/like/` - Like a post
- `DELETE /posts/<id>/unlike/` - Unlike a post

### Notifications

- `GET /notifications/` - List user notifications
- `POST /notifications/<id>/read/` - Mark notification as read

## Installation and Setup

### Prerequisites

- Python 3.8+
- Virtual environment
- PostgreSQL (for production)

### Development Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd social_media_api
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**

   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

5. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Production Deployment

#### Option 1: Heroku Deployment

1. **Install Heroku CLI**

   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login to Heroku**

   ```bash
   heroku login
   ```

3. **Create Heroku app**

   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables**

   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

5. **Add PostgreSQL addon**

   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

6. **Deploy**

   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

7. **Run migrations on Heroku**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

#### Option 2: AWS/DigitalOcean/VPS Deployment

1. **Server setup**

   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python, pip, and PostgreSQL
   sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx
   ```

2. **Clone and setup project**

   ```bash
   git clone <repository-url>
   cd social_media_api
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure PostgreSQL**

   ```bash
   sudo -u postgres psql
   CREATE DATABASE social_media_api;
   CREATE USER social_media_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE social_media_api TO social_media_user;
   \q
   ```

4. **Run deployment script**

   ```bash
   ./deploy.sh
   ```

5. **Configure Nginx**

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static/ {
           alias /path/to/your/project/staticfiles/;
       }

       location /media/ {
           alias /path/to/your/project/media/;
       }
   }
   ```

6. **Start Gunicorn**
   ```bash
   gunicorn social_media_api.wsgi:application --bind 0.0.0.0:8000
   ```

## Testing

Run the development server and test endpoints using tools like:

- **Postman** - For manual API testing
- **curl** - Command line testing
- **Django REST Framework Browsable API** - Visit endpoints in browser

### Sample API Usage

1. **Register a new user**

   ```bash
   curl -X POST http://localhost:8000/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123", "password_confirm": "testpass123"}'
   ```

2. **Login**

   ```bash
   curl -X POST http://localhost:8000/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass123"}'
   ```

3. **Create a post (with token)**
   ```bash
   curl -X POST http://localhost:8000/posts/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Token your-token-here" \
     -d '{"title": "My First Post", "content": "This is my first post!"}'
   ```

## Security Features

- **Token Authentication** - Secure API access
- **Permission Classes** - Role-based access control
- **CSRF Protection** - Cross-site request forgery protection
- **XSS Protection** - Cross-site scripting prevention
- **HTTPS Redirect** - Forced HTTPS in production
- **Security Headers** - Comprehensive security headers

## Architecture

### Models

- **CustomUser** - Extended user model with social features
- **Post** - Blog posts with author relationship
- **Comment** - Comments linked to posts and users
- **Like** - Many-to-many relationship for post likes
- **Notification** - Generic notification system

### Permissions

- **IsAuthorOrReadOnly** - Custom permission for content ownership
- **IsAuthenticated** - Require authentication for most actions

### Pagination

- **PageNumberPagination** - Paginated responses for list views
- **Page size**: 10 items per page

## Monitoring and Maintenance

### Logging

- Application logs stored in `logs/django.log`
- Console and file logging configured
- Different log levels for development and production

### Health Checks

- Admin interface available at `/admin/`
- Database connectivity checks
- Static files serving verification

### Backup Strategy

- Regular database backups recommended
- Media files backup to cloud storage
- Environment variables backup

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is developed for educational purposes as part of the ALX Software Engineering Program.

## Support

For issues and questions:

1. Check existing documentation
2. Review API endpoint specifications
3. Test with provided examples
4. Contact development team

---

**Note**: This is a learning project implementing a complete social media API following industry best practices for Django REST Framework development.

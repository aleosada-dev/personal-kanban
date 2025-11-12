# Personal Kanban Board

A simple and intuitive personal kanban board application built with modern web technologies.

## Tech Stack

- **Frontend**: Bootstrap 5, htmx
- **Backend**: Python, FastAPI
- **Database**: MariaDB
- **Container**: Docker & Docker Compose

## Features

- Create, read, update, and delete kanban cards
- Three-column board layout (To Do, In Progress, Done)
- Card prioritization
- Drag and drop support for moving cards between columns
- Responsive design for mobile and desktop
- RESTful API
- Real-time updates with htmx

## Project Structure

```
personal-kanban/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Database operations
│   ├── database.py      # Database connection
│   └── config.py        # Configuration settings
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   └── templates/
│       └── index.html
├── docker-compose.yml   # Docker configuration for MariaDB
├── init.sql            # Database initialization script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd personal-kanban
```

### 2. Set Up Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` if you want to customize database credentials or other settings.

### 3. Start MariaDB with Docker

```bash
docker-compose up -d
```

This will start a MariaDB container with the configured database.

### 4. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

## Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Click "Add New Card" to create a new kanban card
3. Fill in the title, description, status, and priority
4. View your cards organized in three columns: To Do, In Progress, and Done
5. Edit or delete cards using the action buttons on each card
6. Drag cards between columns to update their status

### API Endpoints

The application provides a RESTful API:

- `GET /` - Main web interface
- `GET /api/cards` - Get all cards
- `POST /api/cards` - Create a new card
- `PUT /api/cards/{card_id}` - Update a card
- `DELETE /api/cards/{card_id}` - Delete a card
- `GET /api/health` - Health check endpoint

### API Documentation

FastAPI provides automatic API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Running Tests

```bash
pytest
```

### Database Management

To reset the database:

```bash
docker-compose down -v
docker-compose up -d
```

To view database logs:

```bash
docker-compose logs -f mariadb
```

To access the MariaDB shell:

```bash
docker-compose exec mariadb mysql -u kanban_user -p kanban_db
# Password: kanban_password (or your custom password from .env)
```

## Configuration

Configuration is managed through environment variables in the `.env` file:

- `DB_USER` - Database username
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host (default: localhost)
- `DB_PORT` - Database port (default: 3306)
- `DB_NAME` - Database name
- `APP_NAME` - Application name
- `DEBUG` - Debug mode (default: False)

## Database Schema

### Cards Table

| Column      | Type        | Description                              |
|-------------|-------------|------------------------------------------|
| id          | Integer     | Primary key                              |
| title       | String(255) | Card title (required)                    |
| description | Text        | Card description (optional)              |
| status      | Enum        | Card status: todo, in_progress, done     |
| priority    | Integer     | Card priority (higher = more important)  |
| created_at  | DateTime    | Creation timestamp                       |
| updated_at  | DateTime    | Last update timestamp                    |

## Troubleshooting

### Database Connection Issues

If you encounter database connection errors:

1. Ensure Docker container is running: `docker-compose ps`
2. Check database logs: `docker-compose logs mariadb`
3. Verify credentials in `.env` match `docker-compose.yml`

### Port Already in Use

If port 8000 or 3306 is already in use:

- For the application: Change the port in the uvicorn command
- For MariaDB: Edit the port mapping in `docker-compose.yml`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Future Enhancements

- User authentication and multiple boards
- Card tags and labels
- Due dates and reminders
- Card comments and attachments
- Search and filter functionality
- Export/import functionality
- Dark mode support
- Mobile app version

## Support

For issues, questions, or contributions, please open an issue in the repository.

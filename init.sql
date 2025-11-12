-- Initialize database for Personal Kanban Board
-- This script runs automatically when the MariaDB container starts

USE kanban_db;

-- Grant additional privileges to the kanban user
GRANT ALL PRIVILEGES ON kanban_db.* TO 'kanban_user'@'%';
FLUSH PRIVILEGES;

-- The tables will be created automatically by SQLAlchemy
-- but you can add seed data here if needed

-- Example seed data (uncomment to use):
-- INSERT INTO cards (title, description, status, priority, created_at) VALUES
-- ('Setup Development Environment', 'Install Python, FastAPI, and dependencies', 'done', 3, NOW()),
-- ('Create Database Schema', 'Design and implement database models', 'done', 2, NOW()),
-- ('Build Frontend UI', 'Create kanban board interface with Bootstrap', 'in_progress', 2, NOW()),
-- ('Add Drag and Drop', 'Implement card drag and drop functionality', 'todo', 1, NOW()),
-- ('Write Documentation', 'Create comprehensive README and API docs', 'todo', 1, NOW());

# AI Prompts (Gemini CLI) – Template
Prompt 1 – Project Planning & Setup :
"I have decided to make a Shipment Management System using Flask. Generate a scalable project structure with app.py, auth.py, models.py, shipment.py, a templates folder for HTML, and configuration for SQLAlchemy and Flask-Login."
Outcome:
Gemini generated a clean Flask project structure with separate modules for app initialization, authentication, models, shipment management, and HTML templates. The configuration included SQLAlchemy for database operations and Flask-Login for user session handling.

Prompt 2 – Authentication Module (auth.py) :
"Create auth.py for user registration and login using Flask-Login, including password hashing, session handling, and form validation."
Outcome:
Received fully functional authentication routes for user registration and login, complete with password hashing via werkzeug.security, session management using Flask-Login, and form validation. The code cleanly integrated with the SQLAlchemy User model and supported both web form and API-based login.

Prompt 3 – Shipment Management API (shipment.py) :
"In shipment.py, create REST API endpoints to add, view, update, and delete shipments. Each shipment should have origin, destination, distance_km, service_level, and status fields, linked to the logged-in user."
Outcome:
Generated RESTful API endpoints for adding, retrieving, updating, and deleting shipments. Each shipment record included origin, destination, distance_km, service_level, and status fields, automatically linked to the authenticated user. Responses were returned in JSON format for easy frontend integration.

Prompt 4 – Database Models (models.py)
"Write models.py with User and Shipment models using SQLAlchemy, setting up relationships and constraints. Include methods for serialization for API responses."
Outcome:
Built SQLAlchemy models for User and Shipment with a one-to-many relationship. Serialization methods were added for converting model objects to JSON. All constraints, such as non-nullable fields and foreign key relations, were enforced for database integrity.

Prompt 5 – Debugging Circular Imports (extensions.py)
"I’m getting circular import errors between app.py, models.py, and auth.py. Refactor my Flask app by creating an extensions.py file to initialize and manage SQLAlchemy, Flask-Login, and other extensions, then update all imports accordingly."
Outcome:
Circular import issues between app.py, models.py, and auth.py were resolved by introducing an extensions.py file. This file handled the initialization of all extensions (db, login_manager, etc.), allowing other modules to import these extensions without causing dependency loops.

Prompt 6 – Deployment Configuration
"Already made requirements.txt via pip freeze,Generate .gitignore, and Procfile for deployment on Render. Configure gunicorn for production, and explain the deployment steps from GitHub to Render."
Outcome:
Generated a requirements.txt listing all dependencies, a .gitignore to exclude unnecessary files, and a Procfile configured for gunicorn. Deployment instructions were followed to push the code to GitHub and deploy successfully on Render, with the app running in production mode.

Prompt 7 – Project Documentation & README
"Write a professional README.md for my Shipment Management System including project overview, architecture diagram, setup instructions, API endpoint documentation (with sample Postman requests/responses), deployed Render app link, and contribution guidelines."
Outcome:
Gemini produced a clean, developer-friendly README file. It started with a short project description, displayed the uploaded architecture diagram, listed all API endpoints with request/response examples from Postman, added environment setup instructions, and included the live deployment link for quick access. The README was structured with headings, code blocks, and markdown tables, making it easy for reviewers and contributors to navigate.
"# nuage_assignment"

Overview
This documentation provides guidelines for setting up and working on the Django project. It includes instructions for installation, configuration, and running the project.

Prerequisites

Python 3.x
pip (Python package installer)
Virtualenv (recommended for creating isolated environments)

Setup
1. Clone the Repository
First, clone the repository to your local machine:

git clone <repository_url>
cd <project_directory>

2. Create and Activate a Virtual Environment
It’s a good practice to create a virtual environment for Python projects to manage dependencies:

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
3. Install Dependencies
Install the required Python packages:

pip install -r requirements.txt

4. Configure the Project
Environment Variables

Database Setup
Run migrations to set up the database schema:
python manage.py migrate

Note: After running migrations, you will find a file named initial_user_creation.log in the project directory. This file contains the credentials for the initial user. Check this file to retrieve the credentials.

5. Run the Development Server
Start the Django development server to test the setup:
python manage.py runserver
Visit http://127.0.0.1:8000/ in your web browser to see the application running.

6. Create a Superuser
Create an admin user to access the Django admin interface:
python manage.py createsuperuser

Follow the prompts to create the superuser account.

8. Running Tests
To run the test suite, use:
python manage.py test



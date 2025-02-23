CampusPing - Realtime Chat & Student Portal

📌 Project Overview

CampusPing is a real-time chat and student management web application built using Flask and MySQL. It allows students to communicate via a live chat system, manage their profiles, and search for other students. The application uses Flask-SocketIO for real-time messaging and supports profile photo uploads.


🚀 Features

🔑 User Authentication – Secure login system using session management.
💬 Real-time Chat – Students can send and receive messages instantly using Flask-SocketIO.
🔍 Student Search – Find students by name and view their details.
🖼️ Profile Photo Upload – Users can upload and update their profile photos.
🔄 Session Management – Ensures authenticated access to protected routes.


🛠️ Technologies Used

Backend: Flask, Flask-SocketIO, MySQL
Frontend: HTML, CSS, JavaScript (Jinja2 for templating)
Database: MySQL
Other Libraries: Werkzeug, MySQL Connector, Socket.IO


📂 Project Structure
CampusPing/
│-- static/
│   │-- uploads/                 # Profile photo storage
│   │-- css/                     # Stylesheets
│   │   │-- home.css             # Styles for home page
│   │   │-- login.css            # Styles for login page
│   │-- videos/                  # Video assets
│   │-- images/                  # Image assets
│-- templates/                   # HTML templates
│   │-- home.html                 # Chat & profile page
│   │-- login.html                # Login page
│-- app.py                        # Main Flask application
│-- requirements.txt              # Dependencies
│-- README.md                     # Project documentation



⚡ Installation & Setup

1. Clone the Repository
git clone  https://github.com/Zorojuro32/Campus-Ping.git


2. Create a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows


3. Install Dependencies
pip install -r requirements.txt


4. Configure Database

Ensure MySQL is running.
Create a database named campusping.
Import required tables using a SQL file or manually create them.


5. Run the Application

python app.py
Visit http://localhost:5000 in your browser.



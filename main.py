from flask import Flask, redirect, render_template, url_for, session, request, flash, jsonify
import mysql.connector
import os
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, send


app = Flask(__name__)
app.secret_key = "het123"

socketio = SocketIO(app)

UPLOAD_FOLDER = "static/uploads" 
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = mysql.connector.connect(host="sql12.freesqldatabase.com", port=3306 ,user="sql12764264",password="b3yUICBLKL",database="sql12764264")
cursor = db.cursor()


@socketio.on('message')
def handle_message(data):
    msg = data['message']
    sender_name = data['sender_name']
    sender_id = data['sender_id']

    print(f"Received Message: {msg} from {sender_name} (ID: {sender_id})")  
    
    query = "INSERT INTO chat_messages (sender_id, sender_name, message) VALUES (%s, %s, %s)"
    cursor.execute(query, (sender_id, sender_name, msg))
    db.commit()
    
    send({'message': msg, 'sender_name': sender_name, 'sender_id': sender_id}, broadcast=True)

    
@app.route('/get_messages')
def get_messages():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT sender_name, message FROM chat_messages ORDER BY id ASC")
    messages = cursor.fetchall()
    cursor.close()
    return jsonify(messages)


@app.route('/chat')
def chat():
    if 'uid' not in session:
        return redirect(url_for('login'))
    
    return render_template('home.html', username=session['name'], user_id=session['uid'])



    
    
@app.route("/", methods=['GET','POST'])
def login():    
    error = None
    if request.method == 'POST':
        uid = request.form['uid']
        password = request.form['Password']
        
        query = "SELECT password from users where uid=%s and password=%s"
        cursor.execute(query, (uid, password))
        user = cursor.fetchone()
        
        if user:
            session['uid'] = uid
            return redirect(url_for('Home'))
        else:
            error = "Invalid UID or Password. Try Again!" 
        
    return render_template('login.html', error=error)



@app.route('/home')
def Home():
    if 'uid' not in session:
        return redirect(url_for('login'))
    
    uid = session['uid']
    
    cursor.execute("SELECT name, age, department, profile_photo from students where student_id=%s", (uid,))
    conn = cursor.fetchone()
     
    if conn:
        name, age, department, profile_photo = conn
        if not profile_photo:
            profile_photo = "static/uploads/default.jpg"
    else:
        name, age, department = "Unknown", "empty", "empty"
       
        
    session['profile_photo'] = profile_photo
    session['name'] = name
    
    return render_template('home.html', name=name, age=age, department=department, profile_photo=profile_photo)

    
@app.route('/search', methods=['GET'])
def search_users():
    if 'uid' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('query', '').strip()  
    
    if not search_query:
        return {"status": "error", "message": "No search query provided"}, 400

    cursor.execute("SELECT student_id, name, age, department, profile_photo FROM students WHERE name LIKE %s", ('%' + search_query + '%',))
    results = cursor.fetchall()

    users = []
    for student in results:
        student_id, name, age, department, profile_photo = student
        users.append({
            "student_id": student_id,
            "name": name,
            "age": age,
            "department": department,
            "profile_photo": profile_photo if profile_photo else "static/uploads/default.jpg"
        })

    return {"status": "success", "users": users}



@app.route('/upload',  methods=['POST'])
def upload_photo():
    if 'uid' not in session:
        return redirect(url_for('login'))
    
    if 'profile_photo' not in request.files:
        flash("No file selected!", "error")
        return redirect(url_for('home'))

    file = request.files['profile_photo']
    if file.filename == '':
        flash("No file selected!", "error")
        return redirect(url_for('home'))
    
    if file:
        filename = secure_filename(f"{session['uid']}_{file.filename}")  
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

       
        cursor.execute("UPDATE students SET profile_photo=%s WHERE student_id=%s", (file_path, session['uid']))
        db.commit()

        
        session['profile_photo'] = file_path

        flash("Profile photo updated successfully!", "success")
    
    return redirect(url_for('Home'))


if __name__ == '__main__':
    socketio.run(app, debug=True)
    import os
    port = int(os.environ.get("PORT", 5000))  # Get PORT from environment, default to 5000
    app.run(host='0.0.0.0', port=port)
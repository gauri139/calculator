from flask import Flask, jsonify, render_template, request, send_from_directory
from app.database_users import get_db
from app.database_history import get_history
from datetime import datetime
from datetime import datetime

user_collection = get_db()
history_collection=get_history()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/<page>')
def serve_page(page):
    return send_from_directory('templates', page)

@app.route('/register', methods = ['POST'])
def register():
    user_data = request.form
    name = user_data.get('name','')
    username = user_data.get('username', '')
    password = user_data.get('password','')
    email_id = user_data.get('email_id','')
    mobile_number = user_data.get('mobile_number','')
    dob = user_data.get('dob','')

    response =  user_collection.find_one({'email_id':email_id})
    if not response:
        user_collection.insert_one({"name":name, 'username':username, 'password':password,
                    'email_id':email_id, 'mobile_number':mobile_number, 'dob':dob})
        return jsonify({"status": 'Success', "message" :  "User Registerd Successfully"})

    else:
        return jsonify({"status": 'Error', "message" :  "User already exist"})

@app.route('/login', methods = ['POST'])
def login():
    user_data = request.form
    username = user_data.get('username', '')
    password = user_data.get('password','')
    response =  user_collection.find_one({'username':username,'password':password})
    if response:
        return jsonify({"status": 'Success', "message" :  "Login Successful"})
    
    else:
        return jsonify({"status": 'Error', "message" :  "Invalid Credentials"})

@app.route('/forgot', methods = ['POST'])
def forgot_password():
    user_data = request.form
    email_id = user_data.get('email_id', '')
    dob = user_data.get('dob','')
    new_password = user_data.get('new_password','')
    response =  user_collection.find_one({'email_id':email_id,'dob':dob})
    if response:
        user_collection.update_one({'email_id':email_id,'dob':dob}, 
                                   {"$set": {'password':new_password}})
        
        return jsonify({"status": 'Success', "message" :  "Password updated successfully"})
    
    else:
        return jsonify({"status": 'Error', "message" :  "User not exist"})

@app.route('/calculator', methods = ['POST'])
def calculator():
    data = request.form
    x = eval(data['x'])
    y = eval(data['y'])
    username = data.get('username', '')
    operation = data['operation']
    if operation == 'addition':
        result = x + y
    
    elif operation == 'multiplication':
        result = x * y

    elif operation == 'subtraction':
        result = x - y

    elif operation == 'division':
        result = x / y
    
    history_collection.insert_one({'username':username,'x':x,'y':y,'operation':operation,'result':result, 'timestamp': datetime.now()})
    
    return jsonify({"status": "success", "result":result})

@app.route('/history', methods=['POST'])
def history():
    data = request.form  # or request.json if using JSON
    username = data.get('username', '')
    records = list(history_collection.find({'username': username}, {'_id': 0}))
    return jsonify({"status": "success", "history": records})

@app.route('/clear-history', methods=['POST'])  # or DELETE if you prefer
def clear_history():
    data = request.form  # or request.json for JSON requests
    username = data.get('username', '')
    result = history_collection.delete_many({'username': username})
    return jsonify({
        "status": "success",
        "message": f"{result.deleted_count} record(s) deleted for user '{username}'."
    })



if __name__=='__main__':
    app.run(host='0.0.0.0',port=5005,debug=True)
    
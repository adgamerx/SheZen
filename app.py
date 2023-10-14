from flask import Flask, send_file, render_template, request, jsonify, session, redirect
import mailsend, os, string, random, bcrypt
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = 'super_secret'

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
@app.route('/')
def home():
    return render_template('index.html')

<<<<<<< HEAD
def gen_string(length):
    characters = string.ascii_letters + string.digits 
    key = ''.join(random.choice(characters) for _ in range(length))
    return key

@app.route('/register')
def register():
    try:
        user_data = request.get_json()
        password = user_data["password"]
        bytes = password.encode('utf-8') 
        salt = bcrypt.gensalt() 
        pass_hash = bcrypt.hashpw(bytes, salt)
        verification_code = gen_string(20)
        user = {
            "name": user_data["name"],
            "pass": pass_hash,
            "phone": user_data["phone"],
            "blood_group": user_data["blood_group"],
            "age": user_data["age"],
            "email": user_data["email"],
            "emergency_con": user_data["emergency_con"],
            "verification_code": verification_code,
            "verified": False
        }
        mailsend.verification_mail(email=user_data["email"], verification_code=verification_code, name=user_data["name"])
        data = supabase.table("users").insert(user).execute()
        return jsonify({"status": "registered"}), 200
    except:
        return jsonify({"status": "something went wrong"}), 400

@app.route('/verify')
def verify():
    verification_code = request.args.get("code")
    user = supabase.table('users').select('*').eq('verification_code', verification_code).execute()
    if user:
        supabase.table("users").update({"verified": True, "verification_code": ""}).eq('verification_code', verification_code).execute()
        session['username'] = user.data['email']
        return render_template("dashboard.html")
    return jsonify({"message": "email not verified"}), 401

@app.route('/login')
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    bytes = password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    pass_hash = bcrypt.hashpw(bytes, salt)
    user = supabase.table('users').select({"email": email}).execute()
    if user.data['email'] == email and user.data['pass'] == pass_hash:
        session['username'] = email
        return render_template("dashboard.html"), 200
    return 'Invalid credentials', 401

@app.route('/edit-profile')
def edit_profile():
    if session['logged_in']:
        user_data = request.get_json()
        email = session['username']
        password = user_data["password"]
        bytes = password.encode('utf-8') 
        salt = bcrypt.gensalt() 
        pass_hash = bcrypt.hashpw(bytes, salt)
        user = {
                "name": user_data["name"],
                "pass": pass_hash,
                "phone": user_data["phone"],
                "blood_group": user_data["blood_group"],
                "age": user_data["age"],
                "email": user_data["email"],
                "emergency_con": user_data["emergency_con"]
            }
        supabase.table("users").update(user).eq('email', user_data["email"]).execute()
        return render_template("dashboard.html")
    return redirect("/login")
    
@app.route('/delete-profile')
def delete_profile():
    if session['logged_in']:
        user_data = request.get_json()
        email = session['username']
        data = supabase.table('users').delete().eq('email', user_data["email"]).execute()
        return render_template("register.html")
    
    


=======
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/safeRoute')
def safeRoute():
    return render_template('safeRoute.html')
>>>>>>> c867ea6cb26a5fcc5a8c029b95e87f04ba9fc0e5
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, send_file, render_template, request, jsonify, session, redirect
import mailsend, os, string, random, bcrypt
from supabase import create_client, Client
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Use a proper session storage type
Session(app)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def gen_string(length):
    characters = string.ascii_letters + string.digits 
    key = ''.join(random.choice(characters) for _ in range(length))
    return key

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
        password = request.form["password"]
        verification_code = gen_string(20)
        user = {
            "name": request.form["name"],
            "pass": request.form["password"],
            "phone": request.form["phone"],
            "blood_group": request.form["blood"],
            "age": urequest.form["age"],
            "email": request.form["email"],
            "emergency_con": user_data["emergency_con"],
            "verification_code": verification_code,
            "verified": False
        }
        mailsend.verification_mail(email=user_data["email"], verification_code=verification_code, name=user_data["name"])
        supabase.table("users").insert(user).execute()
        return jsonify({"status": "registered"}), 200

@app.route('/verify', methods=['GET'])
def verify():
    verification_code = request.args.get("code")
    user = supabase.table('users').select('*').eq('verification_code', verification_code).execute()
    if user:
        supabase.table("users").update({"verified": True, "verification_code": ""}).eq('verification_code', verification_code).execute()
        session['logged_in'] = True
        session['username'] = user.data[0]['email']
        return render_template("dashboard.html")
    return jsonify({"message": "email not verified"}), 401

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form["username"]
        password = request.form['password']
        user = supabase.table('users').select("*").eq("email",email).execute().data[0]
        if user['email'] == email and user['pass'] == password:
            session['logged_in'] = True
            session['username'] = user['email']
            return render_template("index.html"), 200
        return 'Invalid credentials', 401

@app.route('/edit-profile', methods=['POST', 'GET'])
def edit_profile():
    if session.get('logged_in'):
        if request.method == 'POST':
            email = session['username']
            password = user_data["password"]
            user = {
                    "name": request.form['name'],
                    "pass": request.form['password'],
                    "phone": request.form['phone'],
                    "blood_group": request.form['blood'],
                    "age": request.form['age'],
                    "email": request.form['email'],
                    "emergency_con": request.form['emergency_con']
                }
            supabase.table("users").update(user).eq('email', user_data["email"]).execute()
            return render_template("dashboard.html")
        return render_template("editprofile.html")
    return redirect("/login")
    
@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    if session.get('logged_in'):
        email = session['username']
        data = supabase.table('users').delete().eq('email', user_data["email"]).execute()
        return redirect('/register')
    
@app.route('/create-shop', methods=['POST', 'GET'])
def create_shop():
    try:
        if session.get('logged_in'):
            if request.method == "POST":
                name = request.form['shopname']
                desc = request.form['shopdesc']
                uid = request.form['shopid']
                shop_data = {
                    "name": name,
                    "desc": desc,
                    "uid": uid
                }
                email = session['username']
                supabase.table("users").update({"shop": shop_data}).eq('email', session['username']).execute()
                return redirect('/products')
            return render_template("create-shop.html")
        return redirect('/login')
    except Exception as e:
        return str(e)

@app.route('/<shopid>/<pid>', methods=['GET'])
def show_product(shopid, pid):
    if session.get('logged_in'):
        email = session['username']
        user_shop = supabase.table("users").select("*").eq("email", email).execute().data[0]['shop']
        if user_shop:
            product = user_shop['products'][pid-1]
            return render_template('product.html', product=product)
        return redirect('/create-shop')
    return redirect('/login')


@app.route('/market', methods=['GET'])
def products():
    if session.get('logged_in'):
        email = session['username']
        businesses = []
        try:
            data = supabase.table("users").select("*").execute().data
            for user in data:
                shop_data = user.get('shop', {})  # Get the 'shop' data or an empty dictionary
                businesses.append(shop_data)
# Assuming we're looking at the first user's 'shop' data
                return render_template('market.html', shops=businesses)
        except:
            return redirect('/create-shop')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/submit-post', methods=['POST'])
def add_thread():
    if session.get('logged_in'):
        thread_title = request.form['post-title']
        thread_desc = request.form['post-desc']
        user = supabase.table('users').select("*").eq('email', session['username']).execute().data[0]['name']
        thread = {
            'title': thread_title,
            'name': user,
            'description': thread_desc,
            'replies': []
        }
        thread_data = supabase.table('forum').insert(thread).execute()
        return redirect('/forum')

@app.route('/thread/<id>')
def show_thread(id):
    if session.get('logged_in'):
        threads = supabase.table('forum').select('*').eq('id', id).execute().data[0]
        return render_template('post.html', threads=threads, id=id)
    return redirect('/login')

@app.route('/forum')
def forum():
    if session.get('logged_in'):
        forum = supabase.table('forum').select('*').execute().data
        return render_template('forum.html', forum=forum)
    return redirect('/login')

@app.route('/add-reply', methods=['POST'])
def add_reply():
    if session.get('logged_in'):
        reply_text = request.form['reply']
        thread_id = request.form['id']
        name = supabase.table('users').select("*").eq('email', session['username']).execute().data[0]['name']
        reply = {
            "reply": reply_text,
            "name": name
        }
        forum = supabase.table('forum').select('*').eq('id', thread_id).execute().data
        forum['replies'].append(reply)
        supabase.table('forum').update(forum).eq('email', email).execute()
        return redirect(f'/thread/{thread_id}')
        data['products'].append(product)
        supabase.table("users").update({"shop": data}).eq('email', session['username']).execute()
        return redirect('/products')
    return redirect('/login')


    
@app.route("/guides")
def guides():
    return render_template("guide_cards.html")

@app.route("/periodtracker")
def periodtracker():
    return render_template("periodtracker.html")

@app.route("/saferoute")
def saferoute():
    return render_template("safeRoute.html")

@app.route("/gynacfinder")
def gynac():
    return render_template("gynacfinder.html")

@app.route("/financial-independence")
def finde():
    return render_template("financial-independence.html")

@app.route("/periodguide")
def periodguide():
    return render_template("periods.html")

@app.route("/maternity-guide")
def maternity():
    return render_template("maternity-guide.html")

if __name__ == '__main__':
    app.run(debug=True)

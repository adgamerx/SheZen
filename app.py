from flask import Flask, send_file, render_template, request, jsonify, session, redirect
import mailsend, os, string, random, bcrypt
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = 'super_secret'

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

@app.route('/verify', methods=['GET'])
def verify():
    verification_code = request.args.get("code")
    user = supabase.table('users').select('*').eq('verification_code', verification_code).execute()
    if user:
        supabase.table("users").update({"verified": True, "verification_code": ""}).eq('verification_code', verification_code).execute()
        session['username'] = user.data['email']
        return render_template("dashboard.html")
    return jsonify({"message": "email not verified"}), 401

@app.route('/login', methods=['POST'])
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

@app.route('/edit-profile', methods=['POST'])
def edit_profile():
    if session.get('logged_in'):
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
    
@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    if session.get('logged_in'):
        user_data = request.get_json()
        email = session['username']
        data = supabase.table('users').delete().eq('email', user_data["email"]).execute()
        return render_template("register.html")
    
@app.route('/create-shop', methods=['POST'])
def create_shop():
    try:
        if session.get('logged_in'):
            data = request.get_json()
            shop_data = {
                "name": data['name'],
                "category": data['category'],
                "uid": data['uid'],
                "products": []
            }
            supabase.table("users").select("*").eq("email", email).execute()
            supabase.table("users").update({"shop": shop_data}).eq('email', session['username']).execute()
            return redirect('/products')
        return redirect('/login')
    except Exception as e:
        return str(e)

@app.route('/<shopid>/<pid>', methods=['GET'])
def show_product(shopid, pid):
    if session.get('logged_in'):
        user_shop = supabase.table("users").select("*").eq("email", email).execute().data[0]['shop']
        if user_shop:
            product = user_shop['products'][pid-1]
            return render_template('product.html', product=product)
        return redirect('/create-shop')
    return redirect('/login')


@app.route('/products', methods=['GET'])
def products():
    if session.get('logged_in'):
        email = session['username']
        data = supabase.table("users").select("*").eq("email", email).execute()
        data = data.data[0]
        if data['shop']:
            products = data['shop']['products']
            return render_template('products.html', products=products)
        return redirect('/create-shop')
    return redirect('/login')

@app.route('/add-product', methods=['POST'])
def add_product():
    if session.get('logged_in'):
        product_data = request.get_json()
        data = supabase.table("users").select("*").eq("email", email).execute().data[0]
        if data['shop']:
            pid = len(data) + 1
            product = {
                "name": product_data['name'],
                "description": product_data['description'],
                "pid": pid,
                "images": product_data['images'],
                "category": product_data['category'],
                "price": product_data['price']
            }
            data['products'].append(product)
            supabase.table("users").update({"shop": data}).eq('email', session['username']).execute()
            return redirect('/products')
        return redirect('/create-shop')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/add-thread', methods=['POST'])
def add_thread():
    if session.get('logged_in'):
        user_data = request.get_json()
        user = supabase.table('users').select("*").eq('email', session['username']).execute().data[0]['name']
        thread = {
            'title': user_data['title'],
            'name': user_data['name'],
            'description': user_data['description'],
            'replies': []
        }
        thread_data = supabase.table('forum').insert(thread).execute()
        return redirect(f'/thread/{thread_data.data[0].id}')

@app.route('/thread/<id>')
def show_thread(id):
    if session.get('logged_in'):
        threads = supabase.table('forum').select('*').eq('id', id).execute().data[0]
        return render_template('thread.html', threads=threads)
    return redirect('/login')

@app.route('/forum')
def forum():
    if session.get('logged_in'):
        forum = supabase.table('forum').select('*').execute().data
        return render_template('forum.html', forum=forum)
    return redirect('/login')

@app.route('/add-reply')
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


if __name__ == '__main__':
    app.run(debug=True)

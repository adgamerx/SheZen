# SheZen




# **App Features**

- **Women Safety:**
    - Emergency
        - Location share with Family and Friends
        - Show nearby Police station and Hospital
    - Extreme Emergency
        - Share details with nearby hospitals and emergency helplines
    - General: Safe route for Womens (Traffic Layer API by Google Maps)
- **Women Health**
    - Period Tracker
    - Maternity guide with products suggestion on the month
    - Gynecologist booking
- **Financial Planning for Women**
    - Gov. and other schemes to support women notification
    - Marketplace supporting womenprenuers
- **Guides for Women**:
    - Miscellaneous
    

## Tech Used
**Authentication**

- Google OAuth API
- Email/Pass Auth-
- Registration through Social and Email/Pass (verify through ElasticMail API)

**Database**

- PostgreSQL (supabase)
- [supabase.py](http://supabase.py/)

**SMTP**

- ElasticEmail

# **Installation Guide**

To run this app follow the given steps:

### Step 1: Clone the Git Repository

Assuming you have Git installed, you can clone the existing repository using the following command:

```bash
git clone <repository_url>
```

Replace `<repository_url>` with the URL of the Git repository you want to clone.

### Step 2: Navigate to the Project Directory

Change your current working directory to the newly cloned project folder:

```bash
cd <project_folder>
```

### Step 3: Create and Activate a Virtual Environment (Optional but Recommended)

Creating a virtual environment is still recommended to isolate project dependencies, even when working with an existing project. You can use the same commands mentioned earlier:

```bash
virtualenv venv
# On Windows:
venv\Scripts\activate
# On macOS and Linux:
source venv/bin/activate
```

### Step 4: Install Project Dependencies

Install the required dependencies specified in the project's `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 5: Set Up Supabase

Follow the earlier steps to set up Supabase, configure your project, and initialize the Supabase client in the Flask application.

Copy its `supabase_url` and `supabase_key` and set them as environment variables:

```bash
export SUPABASE_URL=<supabase_url>
export SUPABASE_KEY=<supabase_key>
```

### Step 6: Run Your Flask Application with Gunicorn

You can use Gunicorn to run the existing Flask application, just as mentioned in the previous guide:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Make sure to adjust the number of worker processes and the host/port as needed for the existing project.

### Step 7: Access SheZen Application

Your Flask application should now be running. You can access it in your web browser.

By following these steps, you've successfully set up and run an existing Flask project from a Git repository with Flask-Session, Gunicorn, and integrated it with Supabase.

**Team Members**
    - [Abhishek Verma](https://www.linkedin.com/in/w3abhishek/)
    - [Aman Sharma](https://www.linkedin.com/in/adgamerx/)
    - [Bhavya Bhagwani](https://www.linkedin.com/in/bhavyabhagwani/)
    - [Raj Priya Singh](https://www.linkedin.com/in/raj-priya-singh-ba49541a0/)
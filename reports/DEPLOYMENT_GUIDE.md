# Complete Deployment Guide — CrimeWatch Analytics
## Deploying Your B.Sc Data Science Web Application

This guide covers the **3 easiest ways** to deploy your project so that your college professors, examiners, or friends can access it live on their phones or laptops.

---

## 🚀 METHOD 1: Instant Mobile / Local Network Access (Ready Right Now!)

Your Flask app is already configured with `host="0.0.0.0", port=5000`. This means anyone connected to the same Wi-Fi network (including your mobile phone or a professor's laptop in the college lab) can view the website immediately!

### How to open on your phone or another laptop:
1. Make sure your laptop and your phone are connected to the same Wi-Fi.
2. Ensure the server is running on your laptop (double-click `Start_Crime_Website.bat` on Desktop).
3. On your phone’s browser (Chrome/Safari), enter your laptop’s local Wi-Fi IP address:  
   👉 **`http://192.168.0.108:5000`**

*(If Windows Firewall asks for permission, click **"Allow Access"**).*

---

## ☁️ METHOD 2: Free 24/7 Cloud Hosting on Render.com (Recommended for Resume & Viva)

Render provides free, permanent 24/7 cloud hosting with an HTTPS link (e.g., `https://crime-safety-analytics.onrender.com`).

All production configuration files have already been prepared for you:
- `Procfile` (`web: gunicorn app:app`)
- `wsgi.py`
- `render.yaml`
- `requirements.txt` (includes `gunicorn`)

### Step-by-Step Instructions:
1. **Upload your code to GitHub**:
   - Go to [github.com](https://github.com) and log in.
   - Click **New Repository** &rarr; Name it `Crime-Safety-Analytics` &rarr; Click **Create repository**.
   - Click **"Upload an existing file"** &rarr; Drag and drop all files from your `Crime-Safety-Analytics` folder (except the `venv` folder) &rarr; Click **Commit changes**.
2. **Deploy on Render**:
   - Go to [render.com](https://render.com) and sign up for a free account (choose **Sign in with GitHub**).
   - Click **New +** &rarr; Select **Web Service**.
   - Select your `Crime-Safety-Analytics` repository and click **Connect**.
   - Fill in the basic settings:
     - **Name**: `crime-safety-analytics`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Instance Type**: `Free`
   - Click **Create Web Service**.
3. **Done!** Within 2–3 minutes, Render will build your application and give you a permanent live public URL like:  
   `https://crime-safety-analytics.onrender.com`

---

## 🐍 METHOD 3: PythonAnywhere (Zero Git Required — Just Upload a ZIP)

If you don't want to use GitHub, PythonAnywhere is a dedicated Python cloud platform where you can upload files directly through your web browser:

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com) and create a free account.
2. In the Dashboard, go to **Web** &rarr; Click **Add a new web app**.
3. Select **Flask** &rarr; Choose **Python 3.10 / 3.11**.
4. Go to the **Files** tab and upload your `data/`, `model/`, `database/`, `templates/`, `static/`, and `app.py` files.
5. In the **Web** tab, click **Reload your-username.pythonanywhere.com**.
6. Your website is live at: `http://your-username.pythonanywhere.com`!

---

### 🎓 Viva Tip for Cloud Deployment:
> **Professor:** *"How is your web application deployed in production?"*  
> **Your Answer:** *"Sir/Ma'am, for local demonstrations, our Flask WSGI server binds to `0.0.0.0:5000` for intranet and mobile access. For public cloud deployment, we configured a production-ready **Gunicorn WSGI HTTP server** specified in our `Procfile` (`web: gunicorn app:app`), which serves the Flask application asynchronously behind cloud reverse proxies on Render."*

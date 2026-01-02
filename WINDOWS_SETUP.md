# 🪟 CreatorBank - Windows Setup Guide

## Step-by-Step Setup for Windows

You have Python 3.12.7 ✅ - Great! Now let's get PostgreSQL and run your app.

---

## 📥 Step 1: Install PostgreSQL

### Option A: Using Official Installer (Recommended)

1. **Download PostgreSQL:**
   - Go to: https://www.postgresql.org/download/windows/
   - Click "Download the installer"
   - Choose **PostgreSQL 14 or 15** (recommended)
   - Download the Windows x86-64 installer

2. **Run the Installer:**
   - Double-click the downloaded .exe file
   - Click "Next" through the wizard
   - **IMPORTANT - Remember these settings:**
     - Port: `5432` (default)
     - Password: Choose a password (e.g., `postgres`)
     - **Write down your password!** ⚠️

3. **Select Components:**
   - ✅ PostgreSQL Server
   - ✅ pgAdmin 4 (database management tool)
   - ✅ Command Line Tools
   - ❌ Stack Builder (not needed)

4. **Complete Installation:**
   - Click "Finish"
   - pgAdmin 4 will open automatically

### Option B: Using Chocolatey (If you have it)

```bash
choco install postgresql14
```

---

## 🔧 Step 2: Create CreatorBank Database

### Using pgAdmin (GUI - Easier)

1. **Open pgAdmin 4** (should open after installation)
2. **Connect to server:**
   - You'll see "PostgreSQL 14" or similar in left panel
   - Click on it
   - Enter the password you set during installation
3. **Create database:**
   - Right-click "Databases"
   - Select "Create" → "Database"
   - Name: `creatorbank`
   - Owner: `postgres`
   - Click "Save"

**Done! Your database is ready!** ✅

### Using Command Line (Advanced)

```bash
# Open Command Prompt or PowerShell as Admin
psql -U postgres

# You'll be prompted for password
# Then type:
CREATE DATABASE creatorbank;

# Exit with:
\q
```

---

## 🐍 Step 3: Set Up Python Environment

Open **PowerShell** or **Command Prompt** in your project folder:

```bash
# Navigate to project
cd D:\Projects\Creator_Bank\backend

# Create virtual environment
py -m venv venv

# Activate it (PowerShell)
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or for Command Prompt:
venv\Scripts\activate

# You should see (venv) in your prompt now!
```

---

## 📦 Step 4: Install Python Packages

```bash
# Make sure you're in backend folder and venv is activated
# You should see (venv) in your prompt

pip install -r requirements.txt

# This will take 2-3 minutes - it's installing ~30 packages
# Wait for it to complete...
```

---

## ⚙️ Step 5: Configure Environment

```bash
# Still in backend folder

# Copy the example environment file
copy .env.example .env

# Now edit .env with Notepad or VS Code
notepad .env
```

**Edit these lines in .env:**

```ini
# Change this line to match your PostgreSQL password:
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD_HERE@localhost:5432/creatorbank

# For example, if your password is "postgres123":
DATABASE_URL=postgresql+asyncpg://postgres:postgres123@localhost:5432/creatorbank

# Change the SECRET_KEY to something random (important for security!):
SECRET_KEY=your-super-secret-key-change-this-in-production-abc123xyz789

# Keep DEBUG as True for development:
DEBUG=True
```

**Save and close** the file.

---

## 🗄️ Step 6: Create Database Tables

Now let's create all the tables (users, earnings, expenses, etc.):

```bash
# Make sure you're in backend folder with venv activated

# Run migrations
alembic upgrade head

# You should see output like:
# INFO  [alembic.runtime.migration] Running upgrade  -> xxxxx, Initial tables
# INFO  [alembic.runtime.migration] Running upgrade xxxxx -> xxxxx, ...
```

**This creates all 7 tables in your database!** ✅

---

## 🚀 Step 7: Start the Backend Server

```bash
# Still in backend folder with venv activated

uvicorn app.main:app --reload

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
# INFO:     Started server process
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

**🎉 YOUR BACKEND IS RUNNING!** 🎉

---

## 🧪 Step 8: Test It!

Open your browser and go to:

**http://localhost:8000/docs**

You should see the **Swagger UI** with all your API endpoints!

### Quick Test:

1. **Find the `/health` endpoint** in the docs
2. Click on it
3. Click "Try it out"
4. Click "Execute"
5. You should see: `{"status": "healthy"}`

**IT WORKS!** 🎊

---

## 🔍 Step 9: View Your Database

### Using pgAdmin:

1. Open **pgAdmin 4**
2. Navigate to:
   - Servers → PostgreSQL 14 → Databases → creatorbank → Schemas → public → Tables
3. You should see **7 tables:**
   - users
   - connected_platforms
   - earnings
   - expenses
   - transactions
   - invoices
   - predictions

4. **Right-click any table** → "View/Edit Data" → "All Rows" to see data

---

## 📝 Step 10: Create Your First User!

Go to **http://localhost:8000/docs** and:

1. **Find `POST /api/v1/auth/register`**
2. Click "Try it out"
3. Enter:
   ```json
   {
     "email": "your-email@example.com",
     "password": "securepass123",
     "full_name": "Your Name"
   }
   ```
4. Click "Execute"
5. You should see a 201 response with your user data!

6. **Now login:**
   - Find `POST /api/v1/auth/login`
   - Click "Try it out"
   - username: `your-email@example.com`
   - password: `securepass123`
   - Click "Execute"
   - Copy the `access_token` from response

7. **Authorize:**
   - Click the 🔓 **Authorize** button at top right
   - Paste your token
   - Click "Authorize"
   - Now you can test all protected endpoints!

---

## 🎯 You're All Set!

You now have:
- ✅ PostgreSQL running
- ✅ Database created with 7 tables
- ✅ Backend server running
- ✅ First user created
- ✅ Authentication working

---

## 🐛 Troubleshooting

### Database Connection Error

**Error:** `could not connect to server`

**Fix:**
1. Make sure PostgreSQL is running:
   - Open **Services** (Windows + R → type `services.msc`)
   - Find "postgresql-x64-14" or similar
   - Make sure it's "Running"
   - If not, right-click → Start

2. Check your password in `.env` file

### Port Already in Use

**Error:** `Address already in use`

**Fix:**
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the number you see)
taskkill /PID <PID> /F
```

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Fix:**
```bash
# Make sure venv is activated (you should see (venv) in prompt)
# If not:
.\venv\Scripts\Activate.ps1

# Then reinstall:
pip install -r requirements.txt
```

### Alembic Error

**Error:** `Can't locate revision identified by 'xxxxx'`

**Fix:**
```bash
# Delete and recreate migrations
alembic upgrade head
```

---

## 🚀 Next Steps

Now that your backend is running:

1. **Test all endpoints** at http://localhost:8000/docs
2. **Set up YouTube API credentials** (see SETUP.md)
3. **Complete YouTube OAuth** (we'll code this next!)
4. **Build the frontend** (React dashboard)

---

## 💡 Useful Commands

### Start Backend
```bash
cd D:\Projects\Creator_Bank\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

### Access Database
```bash
# Using psql
psql -U postgres -d creatorbank

# Common commands:
\dt          # List all tables
\d users     # Describe users table
SELECT * FROM users;  # View all users
\q           # Quit
```

### Run Tests
```bash
cd D:\Projects\Creator_Bank\backend
.\venv\Scripts\Activate.ps1
pytest
```

### View Logs
The backend logs appear in your terminal where uvicorn is running.

---

**You're ready to build! 🎉**

# AI-Job-Agent Command Handbook

**Project Location**

```
C:\AI-Job-Agent
```

---

# 📂 Navigation

Go to the project folder:

```powershell
cd C:\AI-Job-Agent
```

Show current folder:

```powershell
pwd
```

List files:

```powershell
dir
```

---

# 📝 Git

Check project status:

```powershell
git status
```

Stage all files:

```powershell
git add .
```

Commit changes:

```powershell
git commit -m "Describe your changes"
```

Push to GitHub:

```powershell
git push
```

View commit history:

```powershell
git log --oneline
```

View configured remote:

```powershell
git remote -v
```

---

# 🐳 Docker

Check running containers:

```powershell
docker ps
```

Go to Docker folder:

```powershell
cd C:\AI-Job-Agent\docker
```

Start n8n:

```powershell
docker compose up -d
```

Stop n8n:

```powershell
docker compose down
```

Restart n8n:

```powershell
docker compose restart
```

View container logs:

```powershell
docker logs n8n
```

---

# 🤖 LM Studio

API endpoint:

```
http://localhost:1234/v1/models
```

Quick health check:

Open the URL in your browser.

If you see JSON listing your models, LM Studio is working.

---

# 🔄 n8n

Open:

```
http://localhost:5678
```

End-of-session checklist:

* Save workflow (if applicable)
* Export workflow JSON
* Store in:

```
C:\AI-Job-Agent\workflows
```

Then:

```powershell
git add .
git commit -m "Describe milestone"
git push
```

---

# 🗄 SQLite (Coming Soon)

Open DB Browser for SQLite.

Future database location:

```
C:\AI-Job-Agent\Database
```

---

# 🐍 Python (Coming Soon)

Check version:

```powershell
python --version
```

---

# 🎭 Playwright (Coming Soon)

Check version:

```powershell
npx playwright --version
```

---

# 🔍 Troubleshooting

Check Docker:

```powershell
docker ps
```

Check Git status:

```powershell
git status
```

Check current folder:

```powershell
pwd
```

LM Studio API test:

```
http://localhost:1234/v1/models
```

n8n:

```
http://localhost:5678
```

---

# 📋 Session Shutdown Checklist

Before ending a session:

☐ Export the n8n workflow

☐ Save it in:

```
C:\AI-Job-Agent\workflows
```

☐ Check Git:

```powershell
git status
```

☐ Commit:

```powershell
git add .
git commit -m "Describe today's progress"
```

☐ Push:

```powershell
git push
```

☐ Verify GitHub contains the latest commit

---

# 🚀 Current Project Goal

Build a local AI-powered job application assistant that:

* Scrapes job postings
* Compares jobs against Andrew's profile
* Scores each opportunity
* Recommends Apply / Maybe / Skip
* Tracks applications in SQLite
* Generates tailored resumes and cover letters
* Runs entirely on local infrastructure

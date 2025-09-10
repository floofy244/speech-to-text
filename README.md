# 🗣️ Speech-to-Text App

A full-stack speech-to-text application built with **Django REST** on the backend and **React** on the frontend.  
It leverages **OpenAI Whisper** for high-accuracy transcription and **JWT** for secure multi-user authentication.

> ⚠️ **Project status:** Backend complete · Frontend development in progress 🚧

---

## ✨ Features (Planned / Implemented)

- ✅ **Django REST API** for uploading audio files and returning transcriptions  
- ✅ **OpenAI Whisper integration** with Faster Whisper for accurate multilingual speech recognition  
- ✅ **JWT authentication** for secure multi-user access with quota management  
- ✅ **Multi-language support** (10+ languages including auto-detection)  
- ✅ **Multiple model sizes** (Tiny, Base, Small, Medium, Large) for speed/accuracy trade-offs  
- ✅ **Usage tracking** with cost calculation and monthly quota system  
- ✅ **Multiple export formats** (TXT, SRT, VTT, JSON)  
- 🔜 **React frontend** with upload UI, user login/registration, and transcription viewer  
- 🔜 **User dashboard** to manage past transcriptions and view usage analytics  

---

## 🛠️ Tech Stack

| Layer        | Technologies                                      |
|--------------|---------------------------------------------------|
| **Backend**  | Django 4.2.7 · Django REST Framework · Faster Whisper · SQLite/PostgreSQL |
| **Frontend** | React 19.1.1 (planned) · Tailwind CSS 4.1.12 (planned) · Axios · React Dropzone |
| **Auth**     | JSON Web Tokens (JWT) · SimpleJWT |
| **Audio**    | Pydub · Faster Whisper · Multiple format support (MP3, WAV, M4A, OGG, WebM) |
| **Deployment** | Docker (planned) · Render/Heroku/AWS EC2 (planned) |

---

## 📂 Project Structure

```
speech-to-text-app/
├─ stt_app/                    # Django backend
│  ├─ accounts/               # JWT authentication & user management
│  │  ├─ models.py           # Custom User model with quota system
│  │  ├─ views.py            # Auth endpoints (login, register, profile)
│  │  └─ serializers.py      # User data serialization
│  ├─ transcriptions/        # Core transcription functionality
│  │  ├─ models.py           # AudioJob, Transcript, UsageLog models
│  │  ├─ views.py            # Upload & transcription logic
│  │  └─ serializers.py      # Data serialization
│  ├─ frontend/ (WIP)        # React app (default template, needs implementation)
│  │  ├─ src/App.js          # Main React component
│  │  └─ package.json        # Frontend dependencies
│  ├─ stt_app/               # Django project settings
│  │  ├─ settings.py         # Main configuration
│  │  └─ urls.py             # URL routing (needs API endpoints)
│  └─ manage.py              # Django management script
├─ requirements.txt           # Python dependencies
└─ README.md                 # This file
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone <repository-url>
cd speech-to-text-app
```

### 2️⃣ Backend setup

```bash
# Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (create .env file)
echo "SECRET_KEY=your-secret-key-here" > .env
echo "DEBUG=True" >> .env
echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env

# Run migrations and start server
cd stt_app
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 3️⃣ Frontend (coming soon)

Frontend folder contains React app with default template. For now you can interact with the API directly via Postman or cURL.

```bash
cd stt_app/frontend
npm install
npm start  # Will run on http://localhost:3000
```

---

## 📡 API Endpoints (Current)

| Method | Endpoint               | Description                                  |
| ------ | ---------------------- | -------------------------------------------- |
| `POST` | `/api/auth/register/`  | Register new user                            |
| `POST` | `/api/auth/login/`     | Obtain JWT token                             |
| `GET`  | `/api/auth/profile/`   | Get user profile (JWT protected)             |
| `PUT`  | `/api/auth/profile/`   | Update user profile (JWT protected)          |
| `GET`  | `/api/auth/quota/`     | Get user quota information (JWT protected)   |
| `POST` | `/api/transcriptions/upload/` | Upload audio file for transcription (JWT protected) |
| `GET`  | `/api/transcriptions/jobs/` | List user's transcription jobs (JWT protected) |
| `GET`  | `/api/transcriptions/jobs/{id}/` | Get specific job details (JWT protected) |
| `GET`  | `/api/transcriptions/transcripts/{id}/` | Get transcript details (JWT protected) |
| `GET`  | `/api/transcriptions/usage/` | Get usage logs (JWT protected) |

---

## 💰 Pricing Model

Cost-per-minute based on Whisper model size:

| Model   | Cost/minute | Speed | Accuracy |
|---------|-------------|-------|----------|
| Tiny    | ₹0.09       | Fastest | Lowest |
| Base    | ₹0.17       | Fast | Good |
| Small   | ₹0.35       | Medium | Better |
| Medium  | ₹0.70       | Slow | High |
| Large   | ₹1.40       | Slowest | Highest |

Users have monthly quota system with usage tracking and automatic cost calculation.

---

## 📝 Roadmap

* [x] Backend API with Whisper integration
* [x] JWT Authentication with quota management
* [x] Multi-language and multi-model support
* [x] Usage tracking and cost calculation
* [x] Multiple export format support
* [ ] Complete React frontend implementation
* [ ] Configure API URL routing
* [ ] Complete export file generation
* [ ] Dockerize and deploy
* [ ] Real-time progress tracking with WebSockets
* [ ] Batch processing for multiple files

---

## 🤝 Contributing

PRs and issues are welcome! If you'd like to help build the frontend or improve the backend, open an issue or a draft pull request.

---

**Note**: Backend API is fully functional with comprehensive features. Frontend needs implementation to provide complete user experience.

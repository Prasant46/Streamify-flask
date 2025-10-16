# 💬 Streamify - Real-Time Chat Application

A modern full-stack real-time chat and video calling application built with Flask and React.

[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat&logo=react&logoColor=white)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-4.0+-010101?style=flat&logo=socket.io&logoColor=white)](https://socket.io/)

---

## 🌐 Live Demo

**URL:** [https://stramify-flask.vercel.app](https://rupyatrack.vercel.app)  

---

## ✨ Features

- 💬 **Real-Time Chat** - Instant messaging with WebSocket (Socket.IO)
- 📹 **Video Calls** - Peer-to-peer video calling with WebRTC
- 👥 **Friend System** - Send/accept/decline friend requests
- 🔔 **Live Notifications** - Real-time friend request notifications
- 🔐 **Authentication** - JWT-based secure authentication
- 🌑 **Theme Support** - Multiple theme options
- 📱 **Responsive Design** - Mobile-first UI with bottom navigation
- 🟢 **Online Status** - See who's online in real-time

---

## 🛠 Tech Stack

**Frontend:** React 18 • Vite • Tailwind CSS • Socket.IO Client • Axios • Zustand

**Backend:** Flask 3.0 • PostgreSQL • Socket.IO • SQLAlchemy • JWT • Bcrypt • Flask-CORS

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 15+

### 1. Clone & Setup Backend

```bash
# Clone repository
git clone https://github.com/yourusername/streamify-flask.git
cd streamify-flask/backend-flask

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Setup database
python manage.py db upgrade

# Start backend
python run.py
```

Backend runs on **http://localhost:5000**

### 2. Setup Frontend

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Set VITE_API_URL=http://localhost:5000

# Start development server
npm run dev
```

Frontend runs on **http://localhost:5173**

### 3. Access Application

Open **http://localhost:5173** in your browser

---

## 🔑 Environment Variables

### Backend `.env`
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://user:pass@localhost:5432/streamify
FRONTEND_URL=http://localhost:5173
```

### Frontend `.env`
```env
VITE_API_URL=http://localhost:5000
```

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user

### Users & Friends
- `GET /api/users/search?query=name` - Search users
- `POST /api/users/friend-request` - Send friend request
- `PUT /api/users/friend-request/:id` - Accept/decline request
- `GET /api/users/friends` - Get friends list
- `GET /api/users/notifications` - Get friend request notifications

### Chat
- `GET /api/chat/:friendId` - Get chat messages
- `POST /api/chat/:friendId` - Send message
- WebSocket events: `message`, `typing`, `online_status`

---

## 🎯 Key Features Explained

### Real-Time Communication
- Uses **Socket.IO** for bidirectional WebSocket connections
- Real-time message delivery without page refresh
- Typing indicators and online status updates

### Video Calling
- **WebRTC** peer-to-peer video calls
- Direct browser-to-browser connection
- Low latency, high quality video

### Friend System
- Send friend requests to other users
- Accept or decline incoming requests
- Real-time notification updates

---

## 👨‍💻 Author

**Prasant46** - [@Prasant46](https://github.com/Prasant46)

⭐ Star this repo if you found it helpful!
# UniVerse
The study discussion board connecting Australian university students for cross-campus academic support.

## Tech Stack

- **Frontend:** React + TypeScript + Vite + Shadcn UI + TailwindCSS  
- **Backend:** Flask + SQLite + SQLAlchemy + Flask-CORS  

---

## Requirements

- **Node.js** v22.21.0
- **npm** 10.8.1
- **Python** 3.11.9

---

## Setup (DEV)

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/universe.git
cd universe
```

### 2. Backend Setup

```bash
cd backend
```

```bash
# Setup and activate venv

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run backend
flask run
```

### 3. Frontend Setup

```bash
cd frontend

# Install npm packages
npm install

# Run frontend
npm run dev
```
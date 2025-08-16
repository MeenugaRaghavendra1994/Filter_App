# 🚀 Full Stack Application (FastAPI + React)

This project consists of a **backend (FastAPI)** and a **frontend (React)**.  
Follow the steps below to run the application in **VS Code**.

---

## 📂 Project Structure
```
project-root/
│── backend/   # FastAPI backend
│   ├── main.py
│   └── requirements.txt
│
│── frontend/  # React frontend
│   ├── src/
│   └── package.json
│
└── README.md
```

---

## 🖥️ 1. Open the Project in VS Code
1. Open **Visual Studio Code**.  
2. Open the folder containing both `backend/` and `frontend/`.  

---

## ⚙️ 2. Run the Backend (FastAPI)
1. Open the integrated terminal (**Ctrl + `**).  
2. Navigate to the backend folder:
   ```bash
   cd backend
   ```
3. (First time only) install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```
   - Runs at: **http://127.0.0.1:8000**  
   - API Docs: **http://127.0.0.1:8000/docs**

---

## 🌐 3. Run the Frontend (React)
1. Open a **new terminal** in VS Code (`Ctrl + Shift + ``).  
2. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
3. (First time only) install dependencies:
   ```bash
   npm install
   ```
4. Start the frontend server:
   ```bash
   npm start
   ```
   - Runs at: **http://localhost:3000**

---

## ✅ 4. Access the Application
- **Frontend (UI):** [http://localhost:3000](http://localhost:3000)  
- **Backend (API):** [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- **API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

---

## 🛠️ Requirements
- [Python 3.8+](https://www.python.org/downloads/)  
- [Node.js & npm](https://nodejs.org/)  
- [VS Code](https://code.visualstudio.com/)  

---

## 📌 Notes
- Keep the **backend** and **frontend** running in separate terminals.  
- The frontend will automatically connect to the backend APIs if configured.  

---

✨ You’re all set! Run both servers and open the browser 🚀

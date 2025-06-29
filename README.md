# 🚀 AutoBill Backend

AutoBill is a backend API system designed to automate billing operations. This backend handles user requests, processes data, and integrates with OCR systems to extract and manage invoice or receipt data automatically.

## 📂 Project Structure

```
auto_bill_backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   └── main.py
├── .env
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🛠️ Features

- ✅ FastAPI for high-performance async APIs  
- ✅ Pydantic for data validation  
- ✅ Docker-ready for containerized deployment  
- ✅ Modular structure: separation of routes, models, and services  
- ✅ Environment variable configuration using `.env`

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/auto_bill_backend.git
cd auto_bill_backend
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Rename `.env.example` to `.env` and configure your values (DB URL, secret keys, etc.).

### 5. Run the development server

```bash
uvicorn app.main:app --reload
```

> The server will be live at `http://127.0.0.1:8000`

## 🐳 Run with Docker

### Build and run the container:

```bash
docker build -t auto-bill-backend .
docker run -d -p 8000:8000 --env-file .env auto-bill-backend
```

## 🔍 API Documentation

Once the server is running, access interactive API docs at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📦 Tech Stack

- **FastAPI** – Web framework  
- **Pydantic** – Data validation  
- **Docker** – Containerization  
- **Uvicorn** – ASGI server  
- **Python 3.9+**

## 📁 Future Roadmap

- [ ] Add authentication support (JWT / OAuth)
- [ ] Database integration (PostgreSQL / SQLite / MongoDB)
- [ ] CI/CD pipeline integration
- [ ] Testing suite with `pytest`

## 🤝 Contributing

Feel free to fork the repo and open pull requests. All contributions are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/xyz`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature/xyz`)
5. Open a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

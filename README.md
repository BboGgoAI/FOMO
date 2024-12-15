# **SF Events Aggregator**

A modern web application to discover events happening in San Francisco. Built with **Next.js**, **FastAPI**, and **Supabase**.

---

## **Project Structure**

*Project structure details to be added*

---

## **Setup Instructions**

### Backend Setup
```bash
cd server
python3 -m venv venv
# For macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```
The backend will run on http://127.0.0.1:8000/.

### Frontend Setup
```bash
cd client
npm install
npm run dev
```
The frontend will run on http://localhost:3000/.

### Run the Scraper
```bash
cd scripts
python3 eventbrite.py
```

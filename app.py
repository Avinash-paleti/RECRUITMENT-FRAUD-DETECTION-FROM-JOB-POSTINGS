from flask import Flask, render_template, request, redirect, session, jsonify
import joblib, re, os, nltk, bcrypt
import numpy as np
from datetime import datetime

from db import users_col, predictions_col

from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pandas as pd
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
nltk.download("stopwords")

app = Flask(__name__)
app.secret_key = "fraudshield_secret"
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs("uploads", exist_ok=True)

model = joblib.load("models/fraud_model.pkl")
vectorizer = joblib.load("models/tfidf.pkl")
stop_words = set(stopwords.words("english"))

# ---------- UTILITIES ----------

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return " ".join(w for w in text.split() if w not in stop_words)

def extract_text_from_file(path):
    if path.endswith(".pdf"):
        reader = PdfReader(path)
        return " ".join(p.extract_text() or "" for p in reader.pages)
    elif path.endswith(".docx"):
        doc = Document(path)
        return " ".join(p.text for p in doc.paragraphs)
    elif path.endswith(".xlsx"):
        df = pd.read_excel(path)
        return " ".join(df.astype(str).values.flatten())
    elif path.lower().endswith((".png", ".jpg", ".jpeg")):
        return pytesseract.image_to_string(Image.open(path))
    return ""

def get_probs(vec):
    if hasattr(model, "predict_proba"):
        p = model.predict_proba(vec)[0]
        return p[1]*100, p[0]*100
    score = model.decision_function(vec)[0]
    fraud = 1/(1+np.exp(-score))*100
    return fraud, 100-fraud

def risk_level(p):
    if p < 30: return "Low"
    if p < 70: return "Medium"
    return "High"

# ---------- ROUTES ----------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.form.get("job_text", "")
    file = request.files.get("file")
    extracted = text

    if file and file.filename:
        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)
        extracted += " " + extract_text_from_file(path)

    cleaned = clean_text(extracted)
    vec = vectorizer.transform([cleaned])

    fraud, genuine = get_probs(vec)
    # ✅ Convert NumPy types to native Python float
    fraud = float(fraud)
    genuine = float(genuine)
    risk = risk_level(fraud)

    prediction = "🚨 Fraudulent Job Advertisement" if fraud > 50 else "✅ Genuine Job Advertisement"

    predictions_col.insert_one({
        "prediction": prediction,
        "fraud_probability": fraud,
        "risk": risk,
        "created_at": datetime.now()
    })

    return render_template(
        "index.html",
        prediction=prediction,
        fraud_prob=round(fraud,2),
        genuine_prob=round(genuine,2),
        risk=risk,
        job_text=text
    )

# ---------- AUTH ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if users_col.find_one({"username": username}):
            return "User already exists"

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        users_col.insert_one({
            "username": username,
            "password": hashed,
            "role": role
        })

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = users_col.find_one({"username": request.form["username"]})
        if user and bcrypt.checkpw(request.form["password"].encode(), user["password"]):
            session["role"] = user["role"]
            return redirect("/admin")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- ADMIN ----------

@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/login")
    return render_template("admin.html")

@app.route("/admin/stats")
def stats():
    total = predictions_col.count_documents({})
    frauds = predictions_col.count_documents({"prediction":{"$regex":"Fraud"}})
    return jsonify({
        "total": total,
        "frauds": frauds,
        "genuine": total - frauds
    })

if __name__ == "__main__":
    app.run(debug=True)
Recruitment Fraud Detection From Job Advertisement 
(Final Year B.Tech Project)

📌 Project Overview

The Fake Job Advertisement Detection System is a web-based machine learning application designed to identify and classify job advertisements as Fraudulent or Genuine. With the rapid growth of online job portals, fake job postings have become a serious concern. This project aims to assist users by automatically analyzing job descriptions and warning them about potential fraud.

This project is developed as part of the Final Year B.Tech Project requirement.

🎯 Objectives

To detect fraudulent job advertisements using Machine Learning techniques
To prevent meaningless or random text from producing misleading predictions
To provide users with a simple and interactive web interface
To classify job ads with probability scores and risk levels

🧠 System Features

Accepts job descriptions via text input or file upload
Performs input validation to block invalid or random text
Uses Natural Language Processing (NLP) for text cleaning
Applies TF-IDF vectorization for feature extraction
Predicts whether a job advertisement is Fraudulent or Genuine
Displays fraud probability, genuine probability, and risk level
Stores prediction results with timestamps in the database

🏗️ Project Architecture

User Input (Text / File)
        ↓
Input Validation Layer
        ↓
Text Preprocessing (NLP)
        ↓
TF-IDF Feature Extraction
        ↓
Machine Learning Model
        ↓
Prediction & Risk Analysis
        ↓
Result Display (Web Interface)

🛠️ Technologies Used

Programming & Frameworks
Python
Flask (Web Framework)
Machine Learning & NLP
Scikit-learn
TF-IDF Vectorizer
Logistic Regression / Ensemble Model
Frontend
HTML
CSS
Jinja2 Templates
Database
MongoDB (for storing prediction results)

🔍 Input Validation Logic

To ensure prediction reliability, the system includes semantic validation layers:

Rejects empty or very short input
Requires presence of job-related keywords
Detects and blocks random or meaningless text
Only valid job advertisements are passed to the ML model

This prevents incorrect predictions on invalid inputs.

🚀 How to Run the Project

Clone the repository

Install required dependencies

pip install -r requirements.txt

Start the Flask application

python app.py

Open the browser and navigate to

http://127.0.0.1:5000/

📊 Output Details

Prediction: Fraudulent or Genuine
Fraud Probability (%)
Genuine Probability (%)
Risk Level: Low / Medium / High

Invalid or random input results in an error message instead of prediction.

📚 Dataset Description

The model is trained on a dataset containing:

Real job advertisements
Fake job advertisements

Text features include job title, description, requirements, and company information.

🎓 Academic Relevance

This project demonstrates practical application of:

Machine Learning
Natural Language Processing
Web Development
Data Validation and Model Reliability

It aligns with real-world cybersecurity and fraud detection problems.

🏁 Conclusion

The Fake Job Advertisement Detection System successfully identifies fraudulent job postings while preventing invalid input from misleading users. The combination of input validation and machine learning improves prediction accuracy and user trust.

👤 Project Details

Project Type: Final Year B.Tech Project
Domain: Machine Learning / NLP / Web Development
Application: Fraud Detection in Online Job Portals

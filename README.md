# Phishing URL Detector 🔐

This project is a **machine learning–based phishing URL detection system**. It helps identify whether a given URL is **legitimate** or **phishing (malicious)** by analyzing URL features and using a trained model.

## 🚀 Features
- Detects **phishing vs legitimate URLs**
- Machine Learning–based classifier (`phishing_model.pkl`)
- Web application interface built with **Flask** + **HTML templates**
- Displays phishing analysis results with graphs (`Analysis_Result[Phishing].png`)
- Demo video included (`Demo.mp4`)

## 🛠️ Tech Stack
- **Python 3.x**
- **Flask** (for the web app)
- **scikit-learn / pickle** (for ML model)
- **HTML, CSS** (frontend templates)

## 📂 Project Structure

OutriX_tasks/

│── phishing.py # Main Flask app

│── phishing_model.pkl # Trained ML model

│── templates/ # HTML frontend

│── Analysis_Result[Phishing].png # Result visualization

│── Demo.mp4 # Demo video of the project

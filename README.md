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

│── Analysis_result[Legitimate].png # Result visualization

│── Demo.mp4 # Demo video of the project

⚙️ Installation & Setup

Clone the repository:

git clone https://github.com/Roshni7865/OutriX_tasks.git
cd OutriX_tasks


Create & activate virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


Install dependencies:

pip install -r requirements.txt


(If requirements.txt is missing, install Flask, scikit-learn, pandas, etc.)

Run the application:

python phishing.py


Open in browser:

http://127.0.0.1:5000/

🧪 Usage

- Enter a URL in the web interface

- The system analyzes the URL

- The result will be Legitimate ✅ or Phishing ❌

📊 Example Output

📺 Demo

A demo video (Demo.mp4) is included in the repository.

📌 Future Enhancements

- Support for real-time phishing detection via APIs

- Integration with browser extensions

- Improved model accuracy with more datasets

👩‍💻 Author

RoshniA

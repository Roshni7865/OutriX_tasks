import pandas as pd # type: ignore
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import re
from urllib.parse import urlparse
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify # type: ignore
import warnings
import os
warnings.filterwarnings('ignore')

# Initialize Flask app
app = Flask(__name__)

# 1. Feature Extraction
def extract_features(url):
    features = {}
    parsed = urlparse(url)

    features['url_length'] = len(url)
    features['hostname_length'] = len(parsed.hostname) if parsed.hostname else 0
    features['path_length'] = len(parsed.path) if parsed.path else 0
    features['query_length'] = len(parsed.query) if parsed.query else 0

    features['uses_ip'] = 1 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", parsed.hostname or '') else 0

    features['num_digits'] = sum(c.isdigit() for c in url)
    features['num_letters'] = sum(c.isalpha() for c in url)
    features['num_special_chars'] = sum(not c.isalnum() for c in url)
    features['num_dots'] = url.count('.')
    features['num_hyphens'] = url.count('-')
    features['num_underscores'] = url.count('_')
    features['num_slashes'] = url.count('/')
    features['num_questionmarks'] = url.count('?')
    features['num_equals'] = url.count('=')
    features['num_ampersands'] = url.count('&')
    features['num_at'] = url.count('@')

    features['is_https'] = 1 if parsed.scheme == 'https' else 0
    features['has_redirect'] = 1 if '//' in parsed.path else 0
    features['shortening_service'] = 1 if parsed.hostname and any(service in parsed.hostname for service in ['bit.ly', 'goo.gl', 'tinyurl', 't.co', 'ow.ly']) else 0
    return features

# 2. Dataset
def load_data():
    return pd.DataFrame({
        'url': [
            'http://example.com/login',
            'http://142.251.16.100/search',
            'http://secure-bank-login.com?verify=account&user=1',
            'https://www.google.com',
            'http://freelotto.com.winner.get.prize.now',
            'https://www.amazon.com/gp/buy.html',
            'http://paypal-security-update.com/login.php',
            'https://www.microsoft.com/en-us/',
            'http://facebook.verify-account.security.com',
            'https://www.netflix.com/login'
        ],
        'label': [0, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    })

# 3. Train model
def train_model():
    data = load_data()
    features_list = [extract_features(url) for url in data['url']]
    X = pd.DataFrame(features_list)
    y = data['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Save feature importance plot
    feature_importance = model.feature_importances_
    feature_names = X.columns
    plt.figure(figsize=(10, 6))
    indices = np.argsort(feature_importance)[::-1]
    plt.title("Feature Importance in Phishing Detection")
    plt.bar(range(len(feature_importance)), feature_importance[indices])
    plt.xticks(range(len(feature_importance)), [feature_names[i] for i in indices], rotation=90)
    plt.tight_layout()
    plt.savefig('static/feature_importance.png')

    return model, accuracy, X.columns.tolist()

# 4. Prediction
def predict_url(url, model, feature_columns):
    features = extract_features(url)
    features_df = pd.DataFrame([features])

    for col in feature_columns:
        if col not in features_df:
            features_df[col] = 0
    features_df = features_df[feature_columns]

    prediction = model.predict(features_df)[0]
    probability = model.predict_proba(features_df)[0]

    return {
        'prediction': 'Phishing URL' if prediction == 1 else 'Legitimate URL',
        'confidence': max(probability) * 100,
        'features': features
    }

# 5. Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    try:
        result = predict_url(url, model, feature_columns)
        feature_analysis = []
        for feature, value in result['features'].items():
            feature_analysis.append({
                'name': feature.replace('_', ' ').title(),
                'value': value,
                'risk': 'High' if value > (feature_stats[feature]['mean'] + feature_stats[feature]['std'])
                         else 'Medium' if value > feature_stats[feature]['mean'] else 'Low'
            })
        return render_template('result.html',
                               url=url,
                               prediction=result['prediction'],
                               confidence=round(result['confidence'], 2),
                               features=feature_analysis)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/predict', methods=['GET'])
def api_predict():
    url = request.args.get('url')
    try:
        result = predict_url(url, model, feature_columns)
        return jsonify({'url': url,
                        'prediction': result['prediction'],
                        'confidence': round(result['confidence'], 2),
                        'features': result['features']})
    except Exception as e:
        return jsonify({'error': str(e)})

# 6. Auto-create HTML templates
def create_templates():
    if not os.path.exists('templates'):
        os.makedirs('templates')

    with open('templates/index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
        <html>
        <head>
            <title>Phishing URL Detector</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { background-color: #f8f9fa; }
                .container { max-width: 800px; }
                .header { background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%); color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem; }
                .form-container { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }
            </style>
        </head>
        <body>
            <div class="container my-5">
                <div class="header text-center">
                    <h1>Phishing URL Detector</h1>
                    <p class="lead">Check if a URL is safe or potentially phishing</p>
                </div>
                
                <div class="form-container">
                    <form action="/predict" method="post">
                        <div class="mb-3">
                            <label for="url" class="form-label">Enter URL to analyze:</label>
                            <input type="url" class="form-control" id="url" name="url" placeholder="https://example.com" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Analyze URL</button>
                    </form>
                </div>
                
                <div class="mt-4 text-center">
                    <h4>How It Works</h4>
                    <p>This tool uses machine learning to analyze various features of a URL to determine if it's legitimate or potentially phishing.</p>
                    <img src="/static/feature_importance.png" class="img-fluid" alt="Feature Importance">
                </div>
            </div>
        </body>
        </html>
        ''')
    
    # Create result.html
    with open('templates/result.html', 'w') as f:
        f.write('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Analysis Result - Phishing URL Detector</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { background-color: #f8f9fa; }
                .container { max-width: 1000px; }
                .header { padding: 2rem; border-radius: 10px; margin-bottom: 2rem; }
                .result-card { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }
                .phishing { background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%); color: white; }
                .legitimate { background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%); color: white; }
                .risk-high { color: #dc3545; }
                .risk-medium { color: #fd7e14; }
                .risk-low { color: #198754; }
            </style>
        </head>
        <body>
            <div class="container my-5">
                <div class="header {{ 'phishing' if prediction == 'Phishing URL' else 'legitimate' }}">
                    <h1 class="text-center">Analysis Result</h1>
                </div>
                
                <div class="result-card">
                    <h3>URL: <code>{{ url }}</code></h3>
                    
                    <div class="alert {{ 'alert-danger' if prediction == 'Phishing URL' else 'alert-success' }} mt-4">
                        <h4 class="alert-heading">{{ prediction }}</h4>
                        <p class="mb-0">Confidence: {{ confidence }}%</p>
                    </div>
                    
                    <h4 class="mt-4">Feature Analysis</h4>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Feature</th>
                                    <th>Value</th>
                                    <th>Risk Level</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for feature in features %}
                                <tr>
                                    <td>{{ feature.name }}</td>
                                    <td>{{ feature.value }}</td>
                                    <td class="risk-{{ feature.risk|lower }}">{{ feature.risk }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="mt-4">
                        <a href="/" class="btn btn-primary">Analyze Another URL</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        ''')
    
    # Create error.html
    with open('templates/error.html', 'w') as f:
        f.write('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error - Phishing URL Detector</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container my-5">
                <div class="alert alert-danger">
                    <h4 class="alert-heading">An Error Occurred</h4>
                    <p>{{ error }}</p>
                </div>
                <a href="/" class="btn btn-primary">Try Again</a>
            </div>
        </body>
        </html>
        ''')
# 7. Main
if __name__ == '__main__':
    print("Starting Phishing Detector...")

    if not os.path.exists('static'):
        os.makedirs('static')
    create_templates()

    if os.path.exists("phishing_model.pkl"):
        loaded = joblib.load("phishing_model.pkl")
        if isinstance(loaded, tuple):
            if len(loaded) == 2:
                model, feature_columns = loaded
            elif len(loaded) == 3:
                model, _, feature_columns = loaded
            else:
                raise ValueError("Unexpected format in phishing_model.pkl")
        print("Loaded saved model.")
        accuracy = None
    else:
        model, accuracy, feature_columns = train_model()
        print(f"Model trained with accuracy: {accuracy:.2f}")
        joblib.dump((model, feature_columns), "phishing_model.pkl")

    # Feature stats
    data = load_data()
    features_list = [extract_features(url) for url in data['url']]
    feature_df = pd.DataFrame(features_list)
    feature_stats = {col: {'mean': feature_df[col].mean(), 'std': feature_df[col].std()}
                     for col in feature_df.columns}

    print("Web server running at http://localhost:5000")
    app.run(debug=True)

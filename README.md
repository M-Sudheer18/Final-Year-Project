🚀 Employee Performance Prediction System (ML + Flask + Hugging Face)
📌 Overview

This project is a Machine Learning-based web application that predicts employee performance using historical HR data.

It uses multiple ML algorithms and deploys the best model through a Flask web app, enabling both:

🔹 Single employee prediction
🔹 Bulk prediction using CSV/Excel

📄 Project foundation:

🎯 Key Features

✅ Predict employee performance (Very Low → High Performer)
✅ Real-time prediction using Flask
✅ Bulk prediction via CSV/Excel upload
✅ Model hosted on Hugging Face
✅ Clean UI with charts & results
✅ Download prediction results

🧠 Machine Learning Models Used
Logistic Regression
Random Forest Classifier
XGBoost Classifier

📊 Best model selected based on:

Accuracy
Precision
Recall
F1-Score
⚙️ Tech Stack
🖥️ Backend
Python
Flask
🤖 ML Libraries
Scikit-learn
XGBoost
Pandas
NumPy
🌐 Frontend
HTML
CSS
JavaScript
☁️ Model Hosting
Hugging Face Hub (Model loading via API)

📂 Project Structure
project/
│
├── app.py                # Flask Backend
├── Model.pkl            # ML Model (loaded from Hugging Face)
├── templates/
│   ├── single.html
│   ├── second.html
│   ├── third.html
│   ├── multiple.html
│   └── multiple_result.html
│
├── static/
│   └── sample_emp_data.csv
│
└── requirements.txt

🔄 Workflow
User Input → Flask Backend → Data Preprocessing → ML Model → Prediction → UI Output

📄 Architecture based on report:

🧾 Input Features

The model uses features like:

Age
Years at Company
Salary
Work Hours
Projects Handled
Overtime Hours
Promotions
Satisfaction Score
Department (One-Hot Encoded)
Job Role
Education Level

(From your preprocessing + encoding logic in code )

📊 Output

The system predicts:

Score	Performance Level
1	Very Low Performer
2	Low Performer
3	Average Performer
4	Good Performer
5	High Performer

👉 Score = Prediction × 20 (%)

🔌 API Routes (Flask)
🔹 Single Prediction
POST /predict
🔹 Bulk Prediction
POST /predict_multiple
🔹 Download Sample File
GET /download_sample
🔹 Download Results
GET /download_results/<filename>

(Defined in your Flask backend )

☁️ Model Loading (Hugging Face)

The model is dynamically downloaded if not present:

MODEL_FILE = hf_hub_download(
    repo_id="Sudheer17/employee-performance-model",
    filename="Model.pkl"
)

✔ Ensures portability
✔ No need to store model in repo

(From your implementation )

📦 Installation
git clone https://github.com/your-username/your-repo.git
cd your-repo

pip install -r requirements.txt
▶️ Run the App
python app.py

Then open:

http://127.0.0.1:5000/

📈 Sample Use Cases
HR performance evaluation
Employee retention analysis
Promotion decision support
Workforce analytics
🔍 Future Improvements
Add real HR datasets
Use SHAP (Explainable AI)
Deploy on AWS / Render
Add authentication system
Improve UI (React / Dashboard)

(From report future scope )

👨‍💻 Authors
Sudheer Muthyala
Team Members

GIET Engineering College
ECE Department (2026 Batch)

📜 License

This project is for educational and research purposes.

⭐ Final Note

This project demonstrates how Machine Learning + Web Development + Cloud (Hugging Face) can be combined to build a real-world HR analytics system.

from flask import Flask, render_template, request
import pickle
import uuid
from flask import send_file
import pandas as pd

app = Flask(__name__)

# Connecting Frontend to Backend
@app.route('/', methods = ['GET'])
def single():
    return render_template("single.html")

@app.route('/second', methods = ['GET', 'POST'])
def second():
        return render_template("second.html")

@app.route('/third')
def third():
    return render_template("third.html")

@app.route('/multiple', methods=['GET'])
def multiple():
    return render_template("multiple.html")

# For dowling the File 
@app.route('/download_sample')
def download_sample():
     return send_file('static/sample_emp_data.xlsx', as_attachment=True)

columns = [
        'Age',
        'Years_At_Company',
        'Monthly_Salary',
        'Work_Hours_Per_Week',
        'Projects_Handled',
        'Overtime_Hours',
        'Remote_Work_Frequency',
        'Promotions',
        'Employee_Satisfaction_Score',

        # Department
        'Department_Engineering',
        'Department_Finance',
        'Department_HR',
        'Department_IT',
        'Department_Legal',
        'Department_Marketing',
        'Department_Operations',
        'Department_Sales',

        #job Title
        'Job_Title_Consultant',
        'Job_Title_Developer',
        'Job_Title_Engineer',
        'Job_Title_Manager',
        'Job_Title_Specialist',
        'Job_Title_Technician',

        #Education
        'Education_Level_High School',
        'Education_Level_Master',
        'Education_Level_PhD'
]


cat_cols = [
     # Department
        'Department_Engineering',
        'Department_Finance',
        'Department_HR',
        'Department_IT',
        'Department_Legal',
        'Department_Marketing',
        'Department_Operations',
        'Department_Sales',

        #job Title
        'Job_Title_Consultant',
        'Job_Title_Developer',
        'Job_Title_Engineer',
        'Job_Title_Manager',
        'Job_Title_Specialist',
        'Job_Title_Technician',

        #Education
        'Education_Level_High School',
        'Education_Level_Master',
        'Education_Level_PhD'
]


try:
    with open("Model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    print("Model loading error:", e)




@app.route('/predict', methods = ["POST"])
def predict():

    # Name
    name = request.form["name"]
    gender = request.form["gender"]

    #initialize 
    data = {col: 0 for col in columns}

    # Data 
    data['Age'] = int(request.form["Age"])
    data['Years_At_Company'] = int(request.form["Years_At_Company"])
    data['Monthly_Salary'] = int(request.form["Monthly_Salary"])
    data['Work_Hours_Per_Week'] = int(request.form["Work_Hours_Per_Week"])
    data['Projects_Handled'] = int(request.form["Projects_Handled"])
    data['Overtime_Hours'] = int(request.form["Overtime_Hours"])
    data['Remote_Work_Frequency'] = int(request.form["Remote_Work_Frequency"])
    data['Promotions'] = int(request.form["Promotions"])
    data['Employee_Satisfaction_Score'] = float(request.form.get("Employee_Satisfaction_Score", 0))

    # Cat Columns
    department = request.form["department"]
    job = request.form["job"]

    # For Department
    if f"Department_{department}" in data:
         data[f"Department_{department}"] = 1
    
    # For JOB
    if f"Job_Title_{job}" in data:
         data[f"Job_Title_{job}"] = 1

    # For Education
    edu_map = {
    "Bachelor": "High School",
    "Master": "Master",
    "PhD": "PhD"
    }

    edu = edu_map[request.form["education"]]

    if f"Education_Level_{edu}" in data:
        data[f"Education_Level_{edu}"] = 1


    # Convert to Dataframe
    df = pd.DataFrame([data])

    prediction_value = model.predict(df)[0]
    performance_map = {
         1 : "Very Low Performer",
         2 : "Low Performer",
         3 : "Average Performer",
         4 : "Good Performer",
         5 : "High Performer" 
    }
    # Replace this with Model
    if int(prediction_value) in performance_map:
        prediction_label = performance_map[int(prediction_value)]
    else:
        prediction_label = "Unknown"
    score = int(prediction_value) * 20

    return render_template(
         "third.html",
         name = name,
         gender = gender,
         prediction = prediction_label,
         score = score
    )

@app.route('/download_results/<filename>')
def download_results(filename):
    return send_file(filename, as_attachment=True)


@app.route('/predict_multiple', methods=['POST'])
def predict_multiple():

    try:
        file = request.files['file']

        # -------- READ FILE --------
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # -------- VALIDATION --------
        required_cols = [
            'Age', 'Years_At_Company', 'Monthly_Salary',
            'Work_Hours_Per_Week', 'Projects_Handled',
            'Overtime_Hours', 'Remote_Work_Frequency',
            'Promotions', 'Employee_Satisfaction_Score',
            'Department', 'Job_Title', 'Education_Level'
        ]

        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            return f"Missing columns: {missing}"

        # -------- CLEAN DATA --------
        df.fillna(0, inplace=True)

        df['Department'] = df['Department'].str.strip().str.title()
        df['Job_Title'] = df['Job_Title'].str.strip().str.title()
        df['Education_Level'] = df['Education_Level'].str.strip().str.title()

        original_df = df.copy()

        # -------- PROCESS DATA --------
        processed_data = pd.DataFrame(0, index=df.index, columns=columns)

        # Numerical
        num_cols = [
            'Age', 'Years_At_Company', 'Monthly_Salary',
            'Work_Hours_Per_Week', 'Projects_Handled',
            'Overtime_Hours', 'Remote_Work_Frequency',
            'Promotions', 'Employee_Satisfaction_Score'
        ]

        for col in num_cols:
            processed_data[col] = df[col]

        # Department
        for dept in ['Engineering','Finance','HR','IT','Legal','Marketing','Operations','Sales']:
            processed_data[f"Department_{dept}"] = (df['Department'] == dept).astype(int)

        # Job Title
        for job in ['Consultant','Developer','Engineer','Manager','Specialist','Technician']:
            processed_data[f"Job_Title_{job}"] = (df['Job_Title'] == job).astype(int)

        # Education (same logic as single prediction)
        edu_map = {
            "Bachelor": "High School",
            "Master": "Master",
            "PhD": "PhD"
        }

        df['Education_Level'] = df['Education_Level'].map(edu_map)

        for edu in ['High School', 'Master', 'PhD']:
            processed_data[f"Education_Level_{edu}"] = (df['Education_Level'] == edu).astype(int)

        # -------- PREDICT --------
        preds = model.predict(processed_data)

        performance_map = {
            1 : "Very Low Performer",
            2 : "Low Performer",
            3 : "Average Performer",
            4 : "Good Performer",
            5 : "High Performer" 
        }

        original_df['Prediction'] = [performance_map.get(int(p), "Unknown") for p in preds]
        original_df['Score (%)'] = [int(p) * 20 for p in preds]

        # -------- SAVE FILE --------
        
        output_file = f"predicted_{uuid.uuid4().hex}.xlsx"
        original_df.to_excel(output_file, index=False)

        high_count = sum(preds >= 4)
        medium_count = sum(preds == 3)
        low_count = sum(preds <= 2)

        return render_template(
            "multiple_result.html",
            file_name=file.filename,
            total_employees=len(df),
            output_file=output_file,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count
        )

    except Exception as e:
        return str(e)


























if __name__ == "__main__":
    app.run(debug=True)



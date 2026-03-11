from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['dataset']
    df = pd.read_csv(file)

    rows = df.shape[0]
    cols = df.shape[1]

    # Null values
    null_values = df.isnull().sum().sum()

    # Duplicate rows
    duplicates = df.duplicated().sum()

    # Describe summary
    describe_table = df.describe().to_html(classes='table')

    # Chart data (first column)
    column_name = df.columns[0]
    chart_data = df[column_name].value_counts().head(5)

    labels = chart_data.index.tolist()
    values = chart_data.values.tolist()

    # -------------------------------
    # Automated Insights
    # -------------------------------

    insights = []

    missing_percent = (null_values / (rows * cols)) * 100

    if missing_percent > 0:
        insights.append(f"Dataset contains {round(missing_percent,2)}% missing values.")

    if duplicates > 0:
        insights.append(f"There are {duplicates} duplicate rows in the dataset.")

    top_value = df[column_name].value_counts().idxmax()

    insights.append(f"Most frequent value in {column_name} is {top_value}.")


    # -------------------------------
    # Recommendations
    # -------------------------------

    recommendations = []

    if missing_percent > 5:
        recommendations.append("Handle missing values using mean or median imputation.")

    if duplicates > 0:
        recommendations.append("Remove duplicate rows to improve data quality.")

    recommendations.append("Normalize numeric columns before training ML models.")


    return render_template(
        "dashboard.html",
        rows=rows,
        cols=cols,
        null_values=null_values,
        duplicates=duplicates,
        describe_table=describe_table,
        labels=labels,
        values=values,
        insights=insights,
        recommendations=recommendations
    )


@app.route('/predict')
def predict():

    data = {
        "experience":[1,2,3,4,5],
        "salary":[30000,40000,50000,60000,70000]
    }

    df = pd.DataFrame(data)

    X = df[['experience']]
    y = df['salary']

    model = LinearRegression()
    model.fit(X,y)

    prediction = model.predict([[6]])

    return render_template("prediction.html", result=int(prediction[0]))


if __name__ == "__main__":
    app.run(debug=True)
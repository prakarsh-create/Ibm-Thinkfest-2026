from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)
df = None

@app.route('/')
def home():
    return render_template('login.html')


# authentication route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'password':
        return redirect(url_for('index'))
    else:
        return redirect(url_for('home'))


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    global df

    file = request.files['file']

    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    # Insights
    rows = df.shape[0]
    columns = df.shape[1]

    head = df.head().to_html()

    summary = df.describe().to_html()

    missing = df.isnull().sum().to_dict()

    return render_template(
        "dashboard.html",
        rows=rows,
        columns=columns,
        head=head,
        summary=summary,
        missing=missing,
        cols=df.columns.tolist()
    )
@app.route('/analyze', methods=['POST'])
def analyze():

    global df

    column = request.form['column']

    data = df[column]

    mean = data.mean()
    median = data.median()
    maximum = data.max()
    minimum = data.min()

    return render_template(
        "columns.html",
        column=column,
        mean=mean,
        median=median,
        maximum=maximum,
        minimum=minimum
    )

if __name__ == "__main__":
    app.run(debug=True)
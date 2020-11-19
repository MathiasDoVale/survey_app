from surveyapp import app

if __name__ == '__main__':
    app.secret_key = "abc123"
    app.run(debug=True)
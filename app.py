from website import create_app as application
if __name__ == "__main__":
    app = application
    app.run(debug=False, host='0.0.0.0')

if __name__ == '__main__':
    from routes.views import flask_app

    flask_app.run(debug=True, port=5000)

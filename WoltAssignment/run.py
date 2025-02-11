from app.controllers.delivery_controller import app


if __name__ == '__main__':
    app.run(debug=True, port=5003)  # Run the Flask application

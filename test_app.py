from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login_user', methods=['POST'])
def login_user():
    # Dummy user data for testing
    dummy_users = {
        '123456789': {'user_id': 1, 'name': 'John', 'hashed_password': 'hashed_password', 'salt': 'salt'}
    }

    # Get cell number and password from the form data
    cell_number = request.form.get('cell_number')
    password = request.form.get('password')

    # Check if the user exists and password matches
    if cell_number in dummy_users:
        user = dummy_users[cell_number]
        if password == user['hashed_password']:
            return jsonify({"message": "Login successful", "user_id": user['user_id'], "name": user['name']}), 200
    return jsonify({"message": "Login failed"}), 401

if __name__ == "__main__":
    app.run(debug=True)


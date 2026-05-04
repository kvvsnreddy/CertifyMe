from flask import Flask, render_template, request, jsonify
from models import db, User, Opportunity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certifyme.db'
app.config['SECRET_KEY'] = 'certifyme_secret'
db.init_app(app)

@app.route('/')
def index():
    return render_template('admin.html')

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_pw = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(name=data['name'], email=data['email'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Success"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful", "user": user.name}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/opportunities', methods=['POST'])
def add_opportunity():
    data = request.json
    new_opp = Opportunity(
        title=data['name'],
        duration=data['duration'],
        start_date=data['startDate'],
        description=data['description'],
        skills=data['skills']
    )
    db.session.add(new_opp)
    db.session.commit()
    return jsonify({"message": "Opportunity saved"}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

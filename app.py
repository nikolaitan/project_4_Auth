from flask import Flask, request, jsonify
from models import db, User, LoginHistory
from config import Config
import jwt
import datetime
import bcrypt
import redis

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
redis_client = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])

# Генерация JWT
def generate_tokens(user_id):
    access_payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'type': 'access'
    }
    refresh_payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
        'type': 'refresh'
    }
    access_token = jwt.encode(access_payload, app.config['SECRET_KEY'], algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, app.config['SECRET_KEY'], algorithm='HS256')
    return access_token, refresh_token

# Middleware для проверки токена
def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', '').split(' ')[-1]
        if not token:
            return jsonify({'message': 'Token missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if data['type'] != 'access':
                raise jwt.InvalidTokenError()
            kwargs['user_id'] = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Эндпоинты
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
    new_user = User(email=data['email'], password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.checkpw(data['password'].encode(), user.password_hash.encode()):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Запись истории входа
    history = LoginHistory(
        user_id=user.id,
        user_agent=request.headers.get('User-Agent'),
        ip=request.remote_addr
    )
    db.session.add(history)
    db.session.commit()
    
    access, refresh = generate_tokens(user.id)
    return jsonify({'access_token': access, 'refresh_token': refresh})

@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    try:
        data = jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if data['type'] != 'refresh' or redis_client.exists(refresh_token):
            raise jwt.InvalidTokenError()
        
        access_token, _ = generate_tokens(data['user_id'])
        return jsonify({'access_token': access_token})
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token'}), 401

@app.route('/user/update', methods=['PUT'])
@token_required
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
    db.session.commit()
    return jsonify({'message': 'User updated'})

@app.route('/user/history', methods=['GET'])
@token_required
def get_history(user_id):
    history = LoginHistory.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'datetime': h.login_time.isoformat(),
        'ip': h.ip,
        'user_agent': h.user_agent
    } for h in history])

@app.route('/logout', methods=['POST'])
def logout():
    refresh_token = request.json.get('refresh_token')
    if refresh_token:
        redis_client.setex(refresh_token, 2592000, 'revoked')  # 30 дней
    return jsonify({'message': 'Logged out'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
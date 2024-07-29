import jwt
from datetime import datetime, timedelta
from quart import Blueprint, request, jsonify, current_app
from sqlalchemy.future import select
from marshmallow import ValidationError  # Make sure to import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import async_session
from app.models import User
from app.schemas import UserSchema

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()

def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token valid for 24 hours
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

@auth_bp.route('/register', methods=['POST'])
async def register():
    user_data = await request.get_json()
    try:
        user = user_schema.load(user_data)
        user['password_hash'] = generate_password_hash(user['password'])
        del user['password']  # Remove password from user data
    except ValidationError as err:
        return jsonify(err.messages), 400

    async with async_session() as session:
        existing_user = await session.execute(select(User).where(User.username == user['username']))
        if existing_user.scalar_one_or_none():
            return jsonify({'message': 'Username already exists'}), 400

        session.add(User(**user))
        await session.commit()
        return jsonify(user_schema.dump(user)), 201

@auth_bp.route('/login', methods=['POST'])
async def login():
    data = await request.get_json()
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == data['username']))
        user = result.scalar_one_or_none()
        if user and check_password_hash(user.password_hash, data['password']):
            token = create_token(user.id)
            return jsonify({'token': token}), 200
        return jsonify({'message': 'Invalid credentials'}), 401

def token_required(f):
    async def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        else:
            token = token.split(" ")[1]

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            async with async_session() as session:
                result = await session.execute(select(User).where(User.id == payload['user_id']))
                current_user = result.scalar_one_or_none()
                if not current_user:
                    raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 403

        return await f(current_user, *args, **kwargs)

    return decorated_function

from functools import wraps
from flask import request, jsonify , current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None 
        if 'Authorization' in request.headers:
            auth_reader = request.headers['Authorization']
            try:
                token = auth_reader.split(" ")[1]
            except IndexError:
                return jsonify({' Error ': "Token mal formado!"}),401
        if not token:
            return jsonify({' Error ': "Token  não encontrado!)"}),401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({' Error ': "Token expirado!"}),401
        except jwt.InvalidTokenError:
            return jsonify({' Error ': "Token inválido!"}),401
       
       
        return f(data, *args, **kwargs)
       
    return decorated
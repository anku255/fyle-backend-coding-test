import os
import jwt
import datetime
from bankService.jwt.custom_errors import UnauthorizedError, InvalidOrExpiredTokenError

# Dummy User
dummyUser = {'id': 123, 'name': 'John Doe'}


def generateToken():
  secretKey = os.environ.get('SECRET_KEY')
  expiresIn = datetime.datetime.utcnow() + datetime.timedelta(seconds=432000)  # 5 days
  encoded = jwt.encode({'user': dummyUser, 'exp': expiresIn},
                       secretKey, algorithm='HS256')
  return encoded.decode()


def decodeToken(token):
  if not token:
    raise UnauthorizedError

  secretKey = os.environ.get('SECRET_KEY')
  try:
    decoded = jwt.decode(token, secretKey,  algorithms=['HS256'])
    user = decoded['user']
    return user
  except Exception:
    raise InvalidOrExpiredTokenError


def authorizeRequest(request):
  try:
    token = request.headers['Authorization']
    decodeToken(token)
  except KeyError:
    raise UnauthorizedError
  except Exception:
    raise InvalidOrExpiredTokenError

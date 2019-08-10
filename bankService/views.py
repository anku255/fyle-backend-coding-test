import jwt
import os
import datetime
import json
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from bankService.db.db_helpers import connectToDB
from bankService.jwt.jwt_helpers import authorizeRequest, generateToken
from bankService.jwt.custom_errors import UnauthorizedError, InvalidOrExpiredTokenError

conn, cur = connectToDB()


# GET Request
# Public
# Returns the list of available routes


def index(request):
  return HttpResponse("""
    You're at the index of bank service api.
    Try the following routes:
    1. GET -  /api/bank?ifsc="bank_ifsc_code"
    2. GET -  /api/branches?bank_name="bank_name"&city="city"
    3. GET - /api/token
    """)


# GET Request
# Public
# Returns the list of available routes


def getJWTToken(request):
  token = generateToken()
  return JsonResponse({'jwt': token})


# GET Request
# Private
# Returns the Bank details as JSON given an IFSC code


def getBankDetails(request):
  try:
    authorizeRequest(request)

    ifsc = request.GET.get('ifsc', '')
    limit = request.GET.get('limit', 10)  # Default limit = 10
    offset = request.GET.get('offset', 0)  # Default offset = 0

    if not ifsc:
      return HttpResponseBadRequest("Please provide ifsc code as query param.")

    cur.execute("""SELECT * FROM bank_branches WHERE ifsc=(%s) LIMIT (%s) OFFSET (%s);""",
                (ifsc, limit, offset,))
    json = getJSONResponseForBankDetails(cur.fetchall())
    return JsonResponse(json, safe=False)

  except UnauthorizedError:
    return HttpResponseBadRequest("You need to pass an authorization token with the request.")
  except InvalidOrExpiredTokenError:
    return HttpResponseBadRequest("Your JWT Token is either invalid or expired.")
  except Exception:
    return HttpResponseServerError("Something went wrong. Please try again.")


# GET Request
# Private
# Returns the Branch details as JSON given a bank name and a city


def getBranchDetails(request):
  try:
    authorizeRequest(request)

    bank_name = request.GET.get('bank_name', '')
    city = request.GET.get('city', '')
    limit = request.GET.get('limit', 10)  # Default limit = 10
    offset = request.GET.get('offset', 0)  # Default offset = 0

    if not bank_name:
      return HttpResponseBadRequest("Please provide bank_name as query param.")
    if not city:
      return HttpResponseBadRequest("Please provide city as query param.")

    cur.execute("""SELECT * FROM bank_branches WHERE bank_name=(%s) AND city=(%s) LIMIT (%s) OFFSET (%s);""",
                (bank_name, city, limit, offset,))
    json = getJSONResponseForBankDetails(cur.fetchall())
    return JsonResponse(json, safe=False)

  except UnauthorizedError:
    return HttpResponseBadRequest("You need to pass an authorization token with the request.")
  except InvalidOrExpiredTokenError:
    return HttpResponseBadRequest("Your JWT Token is either invalid or expired.")
  except Exception:
    return HttpResponseServerError("Something went wrong. Please try again.")


# Helper Functions


def getJSONResponseForBankDetails(queryResponse):
  colnames = {'ifsc': 0, 'bank_id': 1, 'branch': 2, 'address': 3,
              'city': 4, 'district': 5, 'state': 6, 'bank_name': 7}

  resultJson = []

  for row in queryResponse:
    jsonRow = {}
    jsonRow['bank_id'] = row[colnames['bank_id']]
    jsonRow['bank_name'] = row[colnames['bank_name']]
    jsonRow['ifsc'] = row[colnames['ifsc']]
    jsonRow['branch'] = row[colnames['branch']]
    jsonRow['address'] = row[colnames['address']]
    jsonRow['city'] = row[colnames['city']]
    jsonRow['district'] = row[colnames['district']]
    jsonRow['state'] = row[colnames['state']]

    resultJson.append(jsonRow)

  return resultJson

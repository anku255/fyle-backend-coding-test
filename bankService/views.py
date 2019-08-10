from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import psycopg2
import os
from psycopg2.extras import NamedTupleCursor


# Connect to an existing database
conn = psycopg2.connect("dbname={} user={}".format(
    os.environ.get('DB_NAME'), os.environ.get('DB_USER')))

# Open a cursor to perform database operations
cur = conn.cursor()


# TODO: Add available routes in the index
def index(request):
  return HttpResponse("Hello, world. You're at the index of bank service api.")


# GET Request
# Private
# Returns the Bank details as JSON given an IFSC code
def getBankDetails(request):
  ifsc = request.GET.get('ifsc', '')
  limit = request.GET.get('limit', 10)  # Default limit = 10
  offset = request.GET.get('offset', 0)  # Default offset = 0

  if not ifsc:
    return HttpResponseBadRequest("Please provide ifsc code as query param.")

  try:
    cur.execute("""SELECT * FROM bank_branches WHERE ifsc=(%s) LIMIT (%s) OFFSET (%s);""",
                (ifsc, limit, offset,))
    json = getJSONResponseForBankDetails(cur.fetchall())
    return JsonResponse(json, safe=False)
  except Exception as e:
    print('error', e)
    return HttpResponseServerError("Something went wrong. Please try again.")


# GET Request
# Private
# Returns the Branch details as JSON given a bank name and a city
def getBranchDetails(request):
  bank_name = request.GET.get('bank_name', '')
  city = request.GET.get('city', '')
  limit = request.GET.get('limit', 10)  # Default limit = 10
  offset = request.GET.get('offset', 0)  # Default offset = 0

  if not bank_name:
    return HttpResponseBadRequest("Please provide bank_name as query param.")
  if not city:
    return HttpResponseBadRequest("Please provide city as query param.")

  try:
    cur.execute("""SELECT * FROM bank_branches WHERE bank_name=(%s) AND city=(%s) LIMIT (%s) OFFSET (%s);""",
                (bank_name, city, limit, offset,))
    json = getJSONResponseForBankDetails(cur.fetchall())
    return JsonResponse(json, safe=False)
  except Exception as e:
    print('error', e)
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

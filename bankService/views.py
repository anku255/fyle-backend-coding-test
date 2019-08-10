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

  if not ifsc:
    return HttpResponseBadRequest("Please provide ifsc code as query param.")

  try:
    cur.execute("""SELECT * FROM bank_branches WHERE ifsc=(%s);""",
                (ifsc,))
    json = getJSONResponseForBankDetails(cur.fetchone())
    return JsonResponse(json)
  except:
    return HttpResponseServerError("Something went wrong. Please try again.")


# Helper Functions


def getJSONResponseForBankDetails(queryResponse):
  colnames = {'ifsc': 0, 'bank_id': 1, 'branch': 2, 'address': 3,
              'city': 4, 'district': 5, 'state': 6, 'bank_name': 7}

  resultJson = {}

  resultJson['bank_id'] = queryResponse[colnames['bank_id']]
  resultJson['bank_name'] = queryResponse[colnames['bank_name']]
  resultJson['ifsc'] = queryResponse[colnames['ifsc']]
  resultJson['branch'] = queryResponse[colnames['branch']]
  resultJson['address'] = queryResponse[colnames['address']]
  resultJson['city'] = queryResponse[colnames['city']]
  resultJson['district'] = queryResponse[colnames['district']]
  resultJson['state'] = queryResponse[colnames['state']]

  return resultJson

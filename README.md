### Fyle Backend Coding Test

This Django project contains `bankService` application which contains the required routes for this coding test.

[Heroku URL](https://pacific-thicket-36555.herokuapp.com/api)

### sample.env

The file sample.env provides the list of all the environment variables that are required to run this app.

### Routes

```
1. GET /api

It lists all the available routes.

Query - /api

Sample Response:
You're at the index of bank service api.
Try the following routes:
1. GET - /api/bank?ifsc="bank_ifsc_code"
2. GET - /api/branches?bank_name="bank_name"&city="city"
3. GET - /api/token

```

```
2. GET /api/token

Returns the JWT token which is required for authentication.

Query /api/token

Sample Response:

{
    "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c..."
}
```

```
3. /api/bank

Required query param - [ifsc]
Optional query param - [limit, offset]
Required Header - Authorization

Query = /api/bank?ifsc=ABHY0065001

Sample Response:

[
    {
        "bank_id": 60,
        "bank_name": "ABHYUDAYA COOPERATIVE BANK LIMITED",
        "ifsc": "ABHY0065001",
        "branch": "RTGS-HO",
        "address": "ABHYUDAYA BANK BLDG., B.NO.71, NEHRU NAGAR, KURLA (E), MUMBAI-400024",
        "city": "MUMBAI",
        "district": "GREATER MUMBAI",
        "state": "MAHARASHTRA"
    }
]
```

```
4. /api/branches

Required query param - [bank_name, city]
Optional query param - [limit, offset]
Required Header - Authorization

Query = /api/branches?bank_name=ABHYUDAYA COOPERATIVE BANK LIMITED&city=MUMBAI&limit=2

Sample Response:

[
    {
        "bank_id": 60,
        "bank_name": "ABHYUDAYA COOPERATIVE BANK LIMITED",
        "ifsc": "ABHY0065001",
        "branch": "RTGS-HO",
        "address": "ABHYUDAYA BANK BLDG., B.NO.71, NEHRU NAGAR, KURLA (E), MUMBAI-400024",
        "city": "MUMBAI",
        "district": "GREATER MUMBAI",
        "state": "MAHARASHTRA"
    },
    {
        "bank_id": 60,
        "bank_name": "ABHYUDAYA COOPERATIVE BANK LIMITED",
        "ifsc": "ABHY0065002",
        "branch": "ABHYUDAYA NAGAR",
        "address": "ABHYUDAYA EDUCATION SOCIETY, OPP. BLDG. NO. 18, ABHYUDAYA NAGAR, KALACHOWKY, MUMBAI - 400033",
        "city": "MUMBAI",
        "district": "GREATER MUMBAI",
        "state": "MAHARASHTRA"
    }
]
```

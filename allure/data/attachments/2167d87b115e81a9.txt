# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (47 ms)

Target `restful-booker`, correlation ID `95cd6c3d-cd45-4d2b-a1fd-47b56e21c1c6`, at 2026-11-14T10:45:09.967564+00:00

Request body:

```json
{
  "firstname": "qa-keep-aceaccaa",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-28",
    "checkout": "2026-12-01"
  },
  "additionalneeds": "Breakfast"
}
```

Response body:

```json
{
  "bookingid": 2214,
  "booking": {
    "firstname": "qa-keep-aceaccaa",
    "lastname": "Lovelace",
    "totalprice": 240,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2026-11-28",
      "checkout": "2026-12-01"
    },
    "additionalneeds": "Breakfast"
  }
}
```

## 2. PUT https://restful-booker.herokuapp.com/booking/2214 → 403 (4 ms)

Target `restful-booker`, correlation ID `e3e06a3d-b08b-4974-8f37-c25a71a2b17f`, at 2026-11-14T10:45:10.014857+00:00

Request body:

```json
{
  "firstname": "qa-changed-82859894",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-28",
    "checkout": "2026-12-01"
  },
  "additionalneeds": "Breakfast"
}
```

Response body:

```text
Forbidden
```

## 3. GET https://restful-booker.herokuapp.com/booking/2214 → 200 (4 ms)

Target `restful-booker`, correlation ID `69ee1db2-91b3-4aca-91ea-88269fae33b0`, at 2026-11-14T10:45:10.019277+00:00

Response body:

```json
{
  "firstname": "qa-keep-aceaccaa",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-28",
    "checkout": "2026-12-01"
  },
  "additionalneeds": "Breakfast"
}
```

## 4. GET https://restful-booker.herokuapp.com/booking/2214 → 200 (4 ms)

Target `restful-booker`, correlation ID `7d8cc052-e1fc-4b77-b1e2-ebcce39ab4d2`, at 2026-11-14T10:45:10.024208+00:00

Response body:

```json
{
  "firstname": "qa-keep-aceaccaa",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-28",
    "checkout": "2026-12-01"
  },
  "additionalneeds": "Breakfast"
}
```

## 5. DELETE https://restful-booker.herokuapp.com/booking/2214 → 201 (4 ms)

Target `restful-booker`, correlation ID `3d96cde7-30f9-4ef6-9940-bae835d9fcdd`, at 2026-11-14T10:45:10.028777+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/2214 → 404 (4 ms)

Target `restful-booker`, correlation ID `9eb55160-0e87-40e4-ab10-d80034494525`, at 2026-11-14T10:45:10.032957+00:00

Response body:

```text
Not Found
```


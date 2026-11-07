# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (195 ms)

Target `restful-booker`, correlation ID `6d47a84a-ab64-49a7-8a5d-1c3631aae207`, at 2026-11-07T10:32:26.667223+00:00

Request body:

```json
{
  "firstname": "qa-guest-0d81ca4d",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-21",
    "checkout": "2026-11-24"
  },
  "additionalneeds": "Breakfast"
}
```

Response body:

```json
{
  "bookingid": 808,
  "booking": {
    "firstname": "qa-guest-0d81ca4d",
    "lastname": "Lovelace",
    "totalprice": 240,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2026-11-21",
      "checkout": "2026-11-24"
    },
    "additionalneeds": "Breakfast"
  }
}
```

## 2. DELETE https://restful-booker.herokuapp.com/booking/808 → 201 (61 ms)

Target `restful-booker`, correlation ID `9b03e4cd-d436-4903-9d52-49448e589b21`, at 2026-11-07T10:32:26.863174+00:00

Response body:

```text
Created
```

## 3. GET https://restful-booker.herokuapp.com/booking/808 → 404 (61 ms)

Target `restful-booker`, correlation ID `c6bb45d0-40a3-47c5-bb7b-8c29eff9894b`, at 2026-11-07T10:32:26.924575+00:00

Response body:

```text
Not Found
```

## 4. GET https://restful-booker.herokuapp.com/booking/808 → 404 (61 ms)

Target `restful-booker`, correlation ID `affe7f84-89c6-4012-a43b-2596948757fc`, at 2026-11-07T10:32:26.986816+00:00

Response body:

```text
Not Found
```


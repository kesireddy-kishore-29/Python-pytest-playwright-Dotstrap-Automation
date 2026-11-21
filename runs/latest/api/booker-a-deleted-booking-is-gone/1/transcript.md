# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (29 ms)

Target `restful-booker`, correlation ID `cd108701-baab-4e8a-8525-8c9b8bf8f328`, at 2026-11-21T11:32:13.069733+00:00

Request body:

```json
{
  "firstname": "qa-guest-7cd6a19a",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-12-05",
    "checkout": "2026-12-08"
  },
  "additionalneeds": "Breakfast"
}
```

Response body:

```json
{
  "bookingid": 650,
  "booking": {
    "firstname": "qa-guest-7cd6a19a",
    "lastname": "Lovelace",
    "totalprice": 240,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2026-12-05",
      "checkout": "2026-12-08"
    },
    "additionalneeds": "Breakfast"
  }
}
```

## 2. DELETE https://restful-booker.herokuapp.com/booking/650 → 201 (5 ms)

Target `restful-booker`, correlation ID `cebc7a1b-9a12-406a-92a6-c0b947586ab0`, at 2026-11-21T11:32:13.099475+00:00

Response body:

```text
Created
```

## 3. GET https://restful-booker.herokuapp.com/booking/650 → 404 (5 ms)

Target `restful-booker`, correlation ID `04a0199a-6d1f-4f88-a40e-bfa74024f4bd`, at 2026-11-21T11:32:13.104428+00:00

Response body:

```text
Not Found
```

## 4. GET https://restful-booker.herokuapp.com/booking/650 → 404 (4 ms)

Target `restful-booker`, correlation ID `b3dbbf67-2174-41cc-ae70-684ac65c1c9f`, at 2026-11-21T11:32:13.109815+00:00

Response body:

```text
Not Found
```


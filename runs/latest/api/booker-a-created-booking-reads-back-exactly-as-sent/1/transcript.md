# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (29 ms)

Target `restful-booker`, correlation ID `df502150-7eaf-4872-9371-43469411f9af`, at 2026-11-14T10:45:09.900141+00:00

Request body:

```json
{
  "firstname": "qa-guest-dea5fc53",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-28",
    "checkout": "2026-12-01"
  },
  "additionalneeds": "Late check-in"
}
```

Response body:

```json
{
  "bookingid": 2210,
  "booking": {
    "firstname": "qa-guest-dea5fc53",
    "lastname": "Lovelace",
    "totalprice": 240,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2026-11-28",
      "checkout": "2026-12-01"
    },
    "additionalneeds": "Late check-in"
  }
}
```

## 2. GET https://restful-booker.herokuapp.com/booking/2210 → 200 (5 ms)

Target `restful-booker`, correlation ID `fb2b1fa4-5a4f-48c4-abc1-4df63d375c8e`, at 2026-11-14T10:45:09.929604+00:00

Response body:

```json
{
  "firstname": "qa-guest-dea5fc53",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-28",
    "checkout": "2026-12-01"
  },
  "additionalneeds": "Late check-in"
}
```

## 3. GET https://restful-booker.herokuapp.com/booking/2210 → 200 (5 ms)

Target `restful-booker`, correlation ID `90c1f095-2ed6-45c5-a759-a5ded2e6addc`, at 2026-11-14T10:45:09.935387+00:00

Response body:

```json
{
  "firstname": "qa-guest-dea5fc53",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-28",
    "checkout": "2026-12-01"
  },
  "additionalneeds": "Late check-in"
}
```

## 4. DELETE https://restful-booker.herokuapp.com/booking/2210 → 201 (4 ms)

Target `restful-booker`, correlation ID `61814912-b471-4cf6-adf7-6da38f9f78bd`, at 2026-11-14T10:45:09.941063+00:00

Response body:

```text
Created
```

## 5. GET https://restful-booker.herokuapp.com/booking/2210 → 404 (4 ms)

Target `restful-booker`, correlation ID `1d408d29-6bfe-4946-906f-d4cb32ce6040`, at 2026-11-14T10:45:09.945678+00:00

Response body:

```text
Not Found
```


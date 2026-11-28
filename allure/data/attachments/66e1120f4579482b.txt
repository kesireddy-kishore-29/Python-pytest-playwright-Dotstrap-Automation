# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (36 ms)

Target `restful-booker`, correlation ID `a6cccebf-9b32-48ad-a0ad-db3d69515f72`, at 2026-11-28T12:06:23.618689+00:00

Request body:

```json
{
  "firstname": "qa-guest-8a663d61",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-12-12",
    "checkout": "2026-12-15"
  },
  "additionalneeds": "Late check-in"
}
```

Response body:

```json
{
  "bookingid": 2691,
  "booking": {
    "firstname": "qa-guest-8a663d61",
    "lastname": "Lovelace",
    "totalprice": 240,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2026-12-12",
      "checkout": "2026-12-15"
    },
    "additionalneeds": "Late check-in"
  }
}
```

## 2. GET https://restful-booker.herokuapp.com/booking/2691 → 200 (8 ms)

Target `restful-booker`, correlation ID `054acd98-5f4c-4579-ae15-09fecc8bb1e6`, at 2026-11-28T12:06:23.655423+00:00

Response body:

```json
{
  "firstname": "qa-guest-8a663d61",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-12-12",
    "checkout": "2026-12-15"
  },
  "additionalneeds": "Late check-in"
}
```

## 3. GET https://restful-booker.herokuapp.com/booking/2691 → 200 (8 ms)

Target `restful-booker`, correlation ID `c4e381c8-f0fc-4dbb-abef-5b735ae171f5`, at 2026-11-28T12:06:23.664461+00:00

Response body:

```json
{
  "firstname": "qa-guest-8a663d61",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-12-12",
    "checkout": "2026-12-15"
  },
  "additionalneeds": "Late check-in"
}
```

## 4. DELETE https://restful-booker.herokuapp.com/booking/2691 → 201 (7 ms)

Target `restful-booker`, correlation ID `fc4817b8-b12c-4251-87ca-0bf9b8031bf2`, at 2026-11-28T12:06:23.672223+00:00

Response body:

```text
Created
```

## 5. GET https://restful-booker.herokuapp.com/booking/2691 → 404 (7 ms)

Target `restful-booker`, correlation ID `f4f08c42-2ed6-47b1-afe0-6f4ce14085c8`, at 2026-11-28T12:06:23.679716+00:00

Response body:

```text
Not Found
```


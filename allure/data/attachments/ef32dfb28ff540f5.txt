# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (30 ms)

Target `restful-booker`, correlation ID `5f348e0c-f83f-42ec-b000-c5e6d0a16993`, at 2026-11-21T11:32:13.070533+00:00

Request body:

```json
{
  "firstname": "qa-guest-35377785",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-12-05",
    "checkout": "2026-12-08"
  },
  "additionalneeds": "Late check-in"
}
```

Response body:

```json
{
  "bookingid": 651,
  "booking": {
    "firstname": "qa-guest-35377785",
    "lastname": "Lovelace",
    "totalprice": 240,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2026-12-05",
      "checkout": "2026-12-08"
    },
    "additionalneeds": "Late check-in"
  }
}
```

## 2. GET https://restful-booker.herokuapp.com/booking/651 → 200 (5 ms)

Target `restful-booker`, correlation ID `c12145b8-e7ab-4234-9d02-12e5a3d3c972`, at 2026-11-21T11:32:13.100772+00:00

Response body:

```json
{
  "firstname": "qa-guest-35377785",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-12-05",
    "checkout": "2026-12-08"
  },
  "additionalneeds": "Late check-in"
}
```

## 3. GET https://restful-booker.herokuapp.com/booking/651 → 200 (6 ms)

Target `restful-booker`, correlation ID `c2ac30da-5bd7-4ff4-9180-43e93fc11af5`, at 2026-11-21T11:32:13.107370+00:00

Response body:

```json
{
  "firstname": "qa-guest-35377785",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-12-05",
    "checkout": "2026-12-08"
  },
  "additionalneeds": "Late check-in"
}
```

## 4. DELETE https://restful-booker.herokuapp.com/booking/651 → 201 (5 ms)

Target `restful-booker`, correlation ID `d0c2fe26-9a88-4f10-9294-d63179e15791`, at 2026-11-21T11:32:13.113446+00:00

Response body:

```text
Created
```

## 5. GET https://restful-booker.herokuapp.com/booking/651 → 404 (5 ms)

Target `restful-booker`, correlation ID `5d7f161f-7911-45ab-a9aa-c5494c8893d6`, at 2026-11-21T11:32:13.118827+00:00

Response body:

```text
Not Found
```


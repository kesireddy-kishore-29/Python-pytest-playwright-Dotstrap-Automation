# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (24 ms)

Target `restful-booker`, correlation ID `187170e5-e4b6-4a75-9ee0-1ecb10526b28`, at 2026-11-21T11:32:13.133172+00:00

Request body:

```json
{
  "firstname": "qa-keep-7318e0e4",
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
  "bookingid": 653,
  "booking": {
    "firstname": "qa-keep-7318e0e4",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/653 → 403 (6 ms)

Target `restful-booker`, correlation ID `819c87a8-e159-4fe3-8322-338fc92ed14e`, at 2026-11-21T11:32:13.157616+00:00

Request body:

```json
{
  "firstname": "qa-changed-a4e03587",
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

```text
Forbidden
```

## 3. GET https://restful-booker.herokuapp.com/booking/653 → 200 (6 ms)

Target `restful-booker`, correlation ID `1ba76412-8456-45b1-ad93-632c3f6987ba`, at 2026-11-21T11:32:13.163415+00:00

Response body:

```json
{
  "firstname": "qa-keep-7318e0e4",
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

## 4. GET https://restful-booker.herokuapp.com/booking/653 → 200 (6 ms)

Target `restful-booker`, correlation ID `059e7bb0-2172-490b-a5cc-808b80f22075`, at 2026-11-21T11:32:13.170277+00:00

Response body:

```json
{
  "firstname": "qa-keep-7318e0e4",
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

## 5. DELETE https://restful-booker.herokuapp.com/booking/653 → 201 (6 ms)

Target `restful-booker`, correlation ID `3deb71dd-3f6b-4f49-9a9f-2a08269b1ade`, at 2026-11-21T11:32:13.176346+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/653 → 404 (5 ms)

Target `restful-booker`, correlation ID `657ab75f-59d0-4e41-8e77-cc903ef3f21a`, at 2026-11-21T11:32:13.182160+00:00

Response body:

```text
Not Found
```


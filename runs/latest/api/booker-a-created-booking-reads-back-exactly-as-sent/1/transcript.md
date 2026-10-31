# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (191 ms)

Target `restful-booker`, correlation ID `5a0c2201-1e77-4fab-94ee-90f73f345166`, at 2026-10-31T09:52:07.937627+00:00

Request body:

```json
{
  "firstname": "qa-guest-aa905587",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-14",
    "checkout": "2026-11-17"
  },
  "additionalneeds": "Late check-in"
}
```

Response body:

```json
{
  "bookingid": 724,
  "booking": {
    "firstname": "qa-guest-aa905587",
    "lastname": "Lovelace",
    "totalprice": 240,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2026-11-14",
      "checkout": "2026-11-17"
    },
    "additionalneeds": "Late check-in"
  }
}
```

## 2. GET https://restful-booker.herokuapp.com/booking/724 → 200 (57 ms)

Target `restful-booker`, correlation ID `33cae1cc-3d8e-4612-bd3a-45fffa5a88fe`, at 2026-10-31T09:52:08.128973+00:00

Response body:

```json
{
  "firstname": "qa-guest-aa905587",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-14",
    "checkout": "2026-11-17"
  },
  "additionalneeds": "Late check-in"
}
```

## 3. GET https://restful-booker.herokuapp.com/booking/724 → 200 (57 ms)

Target `restful-booker`, correlation ID `f92a9fa4-3c54-43e5-a61a-0389492342a8`, at 2026-10-31T09:52:08.187109+00:00

Response body:

```json
{
  "firstname": "qa-guest-aa905587",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-14",
    "checkout": "2026-11-17"
  },
  "additionalneeds": "Late check-in"
}
```

## 4. DELETE https://restful-booker.herokuapp.com/booking/724 → 201 (56 ms)

Target `restful-booker`, correlation ID `54a45290-e66a-4f3a-abf5-7dc06f577ea7`, at 2026-10-31T09:52:08.243976+00:00

Response body:

```text
Created
```

## 5. GET https://restful-booker.herokuapp.com/booking/724 → 404 (57 ms)

Target `restful-booker`, correlation ID `e7663fe9-5632-46cd-98f8-22bf3aa17a16`, at 2026-10-31T09:52:08.300668+00:00

Response body:

```text
Not Found
```


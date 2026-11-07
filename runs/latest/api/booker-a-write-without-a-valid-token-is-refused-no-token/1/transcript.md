# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (257 ms)

Target `restful-booker`, correlation ID `3d8257d9-344e-45f0-92cb-99a7d3a210ce`, at 2026-11-07T10:32:26.676769+00:00

Request body:

```json
{
  "firstname": "qa-keep-8358cb0e",
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
  "bookingid": 809,
  "booking": {
    "firstname": "qa-keep-8358cb0e",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/809 → 403 (61 ms)

Target `restful-booker`, correlation ID `b85f2e9e-ee04-4980-8bb4-764e79f9af37`, at 2026-11-07T10:32:26.934121+00:00

Request body:

```json
{
  "firstname": "qa-changed-cdbc73b6",
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

```text
Forbidden
```

## 3. GET https://restful-booker.herokuapp.com/booking/809 → 200 (61 ms)

Target `restful-booker`, correlation ID `eb5bcbcd-5529-4651-9eee-3408dcf1da55`, at 2026-11-07T10:32:26.995807+00:00

Response body:

```json
{
  "firstname": "qa-keep-8358cb0e",
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

## 4. GET https://restful-booker.herokuapp.com/booking/809 → 200 (62 ms)

Target `restful-booker`, correlation ID `812c5652-004e-4e74-8eff-1113745d4aa2`, at 2026-11-07T10:32:27.058616+00:00

Response body:

```json
{
  "firstname": "qa-keep-8358cb0e",
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

## 5. DELETE https://restful-booker.herokuapp.com/booking/809 → 201 (62 ms)

Target `restful-booker`, correlation ID `8edd4024-b83c-422c-946b-636e7c20b7e6`, at 2026-11-07T10:32:27.120910+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/809 → 404 (62 ms)

Target `restful-booker`, correlation ID `6c0d56c3-4df9-4b01-b095-e862a8ed33f2`, at 2026-11-07T10:32:27.183107+00:00

Response body:

```text
Not Found
```


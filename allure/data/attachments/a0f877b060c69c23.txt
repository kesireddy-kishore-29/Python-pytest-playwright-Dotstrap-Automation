# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (32 ms)

Target `restful-booker`, correlation ID `83a643f4-718d-4b28-8d1b-7f5bceb6bed1`, at 2026-11-14T10:45:09.898958+00:00

Request body:

```json
{
  "firstname": "qa-keep-e7738246",
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
  "bookingid": 2212,
  "booking": {
    "firstname": "qa-keep-e7738246",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/2212 → 403 (5 ms)

Target `restful-booker`, correlation ID `9e5dadc7-e190-4727-a1bc-012428d622b8`, at 2026-11-14T10:45:09.931959+00:00

Request body:

```json
{
  "firstname": "qa-changed-230f11eb",
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

## 3. GET https://restful-booker.herokuapp.com/booking/2212 → 200 (5 ms)

Target `restful-booker`, correlation ID `ac18ad19-3cde-4845-b835-7797d86e6f57`, at 2026-11-14T10:45:09.937426+00:00

Response body:

```json
{
  "firstname": "qa-keep-e7738246",
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

## 4. GET https://restful-booker.herokuapp.com/booking/2212 → 200 (5 ms)

Target `restful-booker`, correlation ID `e4c52b75-60ac-4c8f-b520-52d4f18256d9`, at 2026-11-14T10:45:09.943552+00:00

Response body:

```json
{
  "firstname": "qa-keep-e7738246",
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

## 5. DELETE https://restful-booker.herokuapp.com/booking/2212 → 201 (5 ms)

Target `restful-booker`, correlation ID `233a971f-299c-4633-b76a-fbf8e67b842a`, at 2026-11-14T10:45:09.949098+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/2212 → 404 (5 ms)

Target `restful-booker`, correlation ID `04b10400-c62e-4cd8-9f9a-8768666cb313`, at 2026-11-14T10:45:09.954394+00:00

Response body:

```text
Not Found
```


# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (263 ms)

Target `restful-booker`, correlation ID `3bd9c319-63d7-4983-ada8-5fe0d910654c`, at 2026-11-07T10:32:26.674563+00:00

Request body:

```json
{
  "firstname": "qa-guest-a8326010",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-21",
    "checkout": "2026-11-24"
  },
  "additionalneeds": "Late check-in"
}
```

Response body:

```json
{
  "bookingid": 810,
  "booking": {
    "firstname": "qa-guest-a8326010",
    "lastname": "Lovelace",
    "totalprice": 240,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2026-11-21",
      "checkout": "2026-11-24"
    },
    "additionalneeds": "Late check-in"
  }
}
```

## 2. GET https://restful-booker.herokuapp.com/booking/810 → 200 (61 ms)

Target `restful-booker`, correlation ID `39a8f05e-47f1-4e67-ba5f-245247400aa3`, at 2026-11-07T10:32:26.938251+00:00

Response body:

```json
{
  "firstname": "qa-guest-a8326010",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-21",
    "checkout": "2026-11-24"
  },
  "additionalneeds": "Late check-in"
}
```

## 3. GET https://restful-booker.herokuapp.com/booking/810 → 200 (61 ms)

Target `restful-booker`, correlation ID `c1ee4ddc-f495-4b98-bb07-99b934e49a7a`, at 2026-11-07T10:32:27.000518+00:00

Response body:

```json
{
  "firstname": "qa-guest-a8326010",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-21",
    "checkout": "2026-11-24"
  },
  "additionalneeds": "Late check-in"
}
```

## 4. DELETE https://restful-booker.herokuapp.com/booking/810 → 201 (61 ms)

Target `restful-booker`, correlation ID `e3e45cce-1170-455c-aa5d-c2519e5ce363`, at 2026-11-07T10:32:27.062068+00:00

Response body:

```text
Created
```

## 5. GET https://restful-booker.herokuapp.com/booking/810 → 404 (62 ms)

Target `restful-booker`, correlation ID `2baaf25a-9b03-42d3-83a6-4b4746349c95`, at 2026-11-07T10:32:27.123443+00:00

Response body:

```text
Not Found
```


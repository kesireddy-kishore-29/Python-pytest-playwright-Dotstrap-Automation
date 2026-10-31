# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (193 ms)

Target `restful-booker`, correlation ID `6d65ca45-7ce5-45a1-813f-6123f6cdfc58`, at 2026-10-31T09:52:08.363191+00:00

Request body:

```json
{
  "firstname": "qa-guest-048b6698",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-11-14",
    "checkout": "2026-11-17"
  },
  "additionalneeds": "Breakfast"
}
```

Response body:

```json
{
  "bookingid": 730,
  "booking": {
    "firstname": "qa-guest-048b6698",
    "lastname": "Lovelace",
    "totalprice": 240,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2026-11-14",
      "checkout": "2026-11-17"
    },
    "additionalneeds": "Breakfast"
  }
}
```

## 2. PUT https://restful-booker.herokuapp.com/booking/730 → 200 (57 ms)

Target `restful-booker`, correlation ID `b38021c6-e52b-4e98-8ff3-a23d2d52d9fe`, at 2026-10-31T09:52:08.556986+00:00

Request body:

```json
{
  "firstname": "qa-guest-a3d57a71",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-14",
    "checkout": "2026-11-17"
  },
  "additionalneeds": "None"
}
```

Response body:

```json
{
  "firstname": "qa-guest-a3d57a71",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-14",
    "checkout": "2026-11-17"
  },
  "additionalneeds": "None"
}
```

## 3. GET https://restful-booker.herokuapp.com/booking/730 → 200 (57 ms)

Target `restful-booker`, correlation ID `c1a2336c-00ab-40d9-acec-08093864f04e`, at 2026-10-31T09:52:08.614139+00:00

Response body:

```json
{
  "firstname": "qa-guest-a3d57a71",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-14",
    "checkout": "2026-11-17"
  },
  "additionalneeds": "None"
}
```

## 4. GET https://restful-booker.herokuapp.com/booking/730 → 200 (58 ms)

Target `restful-booker`, correlation ID `52798a01-0c0b-4c1b-8f95-8ea3dd990a69`, at 2026-10-31T09:52:08.671902+00:00

Response body:

```json
{
  "firstname": "qa-guest-a3d57a71",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-14",
    "checkout": "2026-11-17"
  },
  "additionalneeds": "None"
}
```

## 5. DELETE https://restful-booker.herokuapp.com/booking/730 → 201 (59 ms)

Target `restful-booker`, correlation ID `7fc77447-16f6-431c-b952-69f8428b0dd5`, at 2026-10-31T09:52:08.732816+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/730 → 404 (58 ms)

Target `restful-booker`, correlation ID `8de6eeb1-934d-4731-940a-6e934a38a6bd`, at 2026-10-31T09:52:08.792091+00:00

Response body:

```text
Not Found
```


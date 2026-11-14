# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (60 ms)

Target `restful-booker`, correlation ID `95675c4b-6ea3-4659-9aa8-7d73896f325f`, at 2026-11-14T10:45:09.960103+00:00

Request body:

```json
{
  "firstname": "qa-guest-5dff7ca1",
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
  "bookingid": 2215,
  "booking": {
    "firstname": "qa-guest-5dff7ca1",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/2215 → 200 (5 ms)

Target `restful-booker`, correlation ID `e6e89afd-37c9-48a2-889d-cfad36240439`, at 2026-11-14T10:45:10.020511+00:00

Request body:

```json
{
  "firstname": "qa-guest-6c899ee8",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-28",
    "checkout": "2026-12-01"
  },
  "additionalneeds": "None"
}
```

Response body:

```json
{
  "firstname": "qa-guest-6c899ee8",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-28",
    "checkout": "2026-12-01"
  },
  "additionalneeds": "None"
}
```

## 3. GET https://restful-booker.herokuapp.com/booking/2215 → 200 (5 ms)

Target `restful-booker`, correlation ID `deae5334-5fa0-4546-a48d-9ff2beb962fd`, at 2026-11-14T10:45:10.025858+00:00

Response body:

```json
{
  "firstname": "qa-guest-6c899ee8",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-28",
    "checkout": "2026-12-01"
  },
  "additionalneeds": "None"
}
```

## 4. GET https://restful-booker.herokuapp.com/booking/2215 → 200 (5 ms)

Target `restful-booker`, correlation ID `e7383663-b618-42e7-b2ee-9daad60f2646`, at 2026-11-14T10:45:10.031579+00:00

Response body:

```json
{
  "firstname": "qa-guest-6c899ee8",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-28",
    "checkout": "2026-12-01"
  },
  "additionalneeds": "None"
}
```

## 5. DELETE https://restful-booker.herokuapp.com/booking/2215 → 201 (4 ms)

Target `restful-booker`, correlation ID `d38db9fa-c875-4b60-b632-ceeeeb7ec569`, at 2026-11-14T10:45:10.036508+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/2215 → 404 (4 ms)

Target `restful-booker`, correlation ID `6d533cce-0689-47cd-b11a-4a541cbccf92`, at 2026-11-14T10:45:10.040997+00:00

Response body:

```text
Not Found
```


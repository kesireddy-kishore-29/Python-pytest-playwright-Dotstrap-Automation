# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (213 ms)

Target `restful-booker`, correlation ID `400db620-33f5-4910-855f-8699a39f9348`, at 2026-11-07T10:32:27.197343+00:00

Request body:

```json
{
  "firstname": "qa-guest-cbeaa45f",
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
  "bookingid": 814,
  "booking": {
    "firstname": "qa-guest-cbeaa45f",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/814 → 200 (62 ms)

Target `restful-booker`, correlation ID `51147710-d57f-4f0a-816b-ca6c1e2b38d7`, at 2026-11-07T10:32:27.411374+00:00

Request body:

```json
{
  "firstname": "qa-guest-f2342675",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-21",
    "checkout": "2026-11-24"
  },
  "additionalneeds": "None"
}
```

Response body:

```json
{
  "firstname": "qa-guest-f2342675",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-21",
    "checkout": "2026-11-24"
  },
  "additionalneeds": "None"
}
```

## 3. GET https://restful-booker.herokuapp.com/booking/814 → 200 (64 ms)

Target `restful-booker`, correlation ID `d1249cbb-4510-4ef0-a179-f039e8fed9ad`, at 2026-11-07T10:32:27.474449+00:00

Response body:

```json
{
  "firstname": "qa-guest-f2342675",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-21",
    "checkout": "2026-11-24"
  },
  "additionalneeds": "None"
}
```

## 4. GET https://restful-booker.herokuapp.com/booking/814 → 200 (64 ms)

Target `restful-booker`, correlation ID `80b9357c-9227-4de7-8bcc-02e392aa9d19`, at 2026-11-07T10:32:27.542371+00:00

Response body:

```json
{
  "firstname": "qa-guest-f2342675",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-11-21",
    "checkout": "2026-11-24"
  },
  "additionalneeds": "None"
}
```

## 5. DELETE https://restful-booker.herokuapp.com/booking/814 → 201 (62 ms)

Target `restful-booker`, correlation ID `f744ab49-99ae-4b10-b617-63ba4af7a2b2`, at 2026-11-07T10:32:27.606769+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/814 → 404 (63 ms)

Target `restful-booker`, correlation ID `95605b77-0972-4595-8cca-9279ac70a274`, at 2026-11-07T10:32:27.669097+00:00

Response body:

```text
Not Found
```


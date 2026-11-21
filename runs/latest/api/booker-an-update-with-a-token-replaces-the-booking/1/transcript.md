# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (29 ms)

Target `restful-booker`, correlation ID `85aaeab4-d444-44c3-bfd6-5033d8ba714d`, at 2026-11-21T11:32:13.135594+00:00

Request body:

```json
{
  "firstname": "qa-guest-d3de58a1",
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
  "bookingid": 654,
  "booking": {
    "firstname": "qa-guest-d3de58a1",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/654 → 200 (5 ms)

Target `restful-booker`, correlation ID `d803451b-10e4-4748-9b6c-17d5ec003fa1`, at 2026-11-21T11:32:13.164909+00:00

Request body:

```json
{
  "firstname": "qa-guest-26ac53db",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-12-05",
    "checkout": "2026-12-08"
  },
  "additionalneeds": "None"
}
```

Response body:

```json
{
  "firstname": "qa-guest-26ac53db",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-12-05",
    "checkout": "2026-12-08"
  },
  "additionalneeds": "None"
}
```

## 3. GET https://restful-booker.herokuapp.com/booking/654 → 200 (5 ms)

Target `restful-booker`, correlation ID `863f13f9-9518-4c51-aa42-96fea08b8b4d`, at 2026-11-21T11:32:13.170631+00:00

Response body:

```json
{
  "firstname": "qa-guest-26ac53db",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-12-05",
    "checkout": "2026-12-08"
  },
  "additionalneeds": "None"
}
```

## 4. GET https://restful-booker.herokuapp.com/booking/654 → 200 (5 ms)

Target `restful-booker`, correlation ID `eb2e9161-dc82-41ae-bcf2-83c82bc3b1df`, at 2026-11-21T11:32:13.176327+00:00

Response body:

```json
{
  "firstname": "qa-guest-26ac53db",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-12-05",
    "checkout": "2026-12-08"
  },
  "additionalneeds": "None"
}
```

## 5. DELETE https://restful-booker.herokuapp.com/booking/654 → 201 (5 ms)

Target `restful-booker`, correlation ID `f9efb9a7-cbb6-40b6-bcea-cdab703a8781`, at 2026-11-21T11:32:13.181437+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/654 → 404 (4 ms)

Target `restful-booker`, correlation ID `cc20625b-458a-43e8-a065-101ff207f835`, at 2026-11-21T11:32:13.186366+00:00

Response body:

```text
Not Found
```


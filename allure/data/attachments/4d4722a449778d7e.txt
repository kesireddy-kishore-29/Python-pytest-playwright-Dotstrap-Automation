# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (39 ms)

Target `restful-booker`, correlation ID `2fc7dd6b-1421-4fee-bce2-2e60d73a8b87`, at 2026-11-28T12:06:23.616952+00:00

Request body:

```json
{
  "firstname": "qa-guest-50f494fa",
  "lastname": "Lovelace",
  "totalprice": 240,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-12-12",
    "checkout": "2026-12-15"
  },
  "additionalneeds": "Breakfast"
}
```

Response body:

```json
{
  "bookingid": 2692,
  "booking": {
    "firstname": "qa-guest-50f494fa",
    "lastname": "Lovelace",
    "totalprice": 240,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2026-12-12",
      "checkout": "2026-12-15"
    },
    "additionalneeds": "Breakfast"
  }
}
```

## 2. DELETE https://restful-booker.herokuapp.com/booking/2692 → 201 (8 ms)

Target `restful-booker`, correlation ID `408b5b9c-26df-4271-b347-ace51e3e5ace`, at 2026-11-28T12:06:23.656470+00:00

Response body:

```text
Created
```

## 3. GET https://restful-booker.herokuapp.com/booking/2692 → 404 (7 ms)

Target `restful-booker`, correlation ID `f57aa879-b5ef-44a9-bf3b-ccc50c58bade`, at 2026-11-28T12:06:23.664265+00:00

Response body:

```text
Not Found
```

## 4. GET https://restful-booker.herokuapp.com/booking/2692 → 404 (8 ms)

Target `restful-booker`, correlation ID `508e5fb5-c6a9-4163-90f5-472948430bf6`, at 2026-11-28T12:06:23.672377+00:00

Response body:

```text
Not Found
```


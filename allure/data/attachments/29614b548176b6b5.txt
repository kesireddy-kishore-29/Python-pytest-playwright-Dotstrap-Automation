# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (30 ms)

Target `restful-booker`, correlation ID `7e4a96d3-f3a4-4e82-b947-10538947db52`, at 2026-11-14T10:45:09.899747+00:00

Request body:

```json
{
  "firstname": "qa-guest-302a0f1b",
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
  "bookingid": 2211,
  "booking": {
    "firstname": "qa-guest-302a0f1b",
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

## 2. DELETE https://restful-booker.herokuapp.com/booking/2211 → 201 (4 ms)

Target `restful-booker`, correlation ID `338e9efd-0b29-4ef7-822b-3d4e9a30ea59`, at 2026-11-14T10:45:09.930622+00:00

Response body:

```text
Created
```

## 3. GET https://restful-booker.herokuapp.com/booking/2211 → 404 (4 ms)

Target `restful-booker`, correlation ID `fa50ea25-bbdc-49ce-8192-2cd738ca5e7d`, at 2026-11-14T10:45:09.935285+00:00

Response body:

```text
Not Found
```

## 4. GET https://restful-booker.herokuapp.com/booking/2211 → 404 (4 ms)

Target `restful-booker`, correlation ID `2ca944f5-4723-46bf-9134-fda7bebc4008`, at 2026-11-14T10:45:09.940768+00:00

Response body:

```text
Not Found
```


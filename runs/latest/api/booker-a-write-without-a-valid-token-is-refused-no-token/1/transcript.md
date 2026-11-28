# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (40 ms)

Target `restful-booker`, correlation ID `c933ba9c-6330-458e-a0b3-e985af3931b7`, at 2026-11-28T12:06:23.617705+00:00

Request body:

```json
{
  "firstname": "qa-keep-1c1a28e2",
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
  "bookingid": 2693,
  "booking": {
    "firstname": "qa-keep-1c1a28e2",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/2693 → 403 (8 ms)

Target `restful-booker`, correlation ID `7510a08c-484f-4179-a932-3ae2894b0651`, at 2026-11-28T12:06:23.658447+00:00

Request body:

```json
{
  "firstname": "qa-changed-3608391c",
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

```text
Forbidden
```

## 3. GET https://restful-booker.herokuapp.com/booking/2693 → 200 (8 ms)

Target `restful-booker`, correlation ID `96593f96-0aee-4d7e-9afd-f641c1253ac6`, at 2026-11-28T12:06:23.666992+00:00

Response body:

```json
{
  "firstname": "qa-keep-1c1a28e2",
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

## 4. GET https://restful-booker.herokuapp.com/booking/2693 → 200 (8 ms)

Target `restful-booker`, correlation ID `a5f998a8-49f9-4a12-91b4-88cc72d2ad3e`, at 2026-11-28T12:06:23.676272+00:00

Response body:

```json
{
  "firstname": "qa-keep-1c1a28e2",
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

## 5. DELETE https://restful-booker.herokuapp.com/booking/2693 → 201 (8 ms)

Target `restful-booker`, correlation ID `7de3aa12-882f-409b-ac7f-08b3e529e7ac`, at 2026-11-28T12:06:23.684686+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/2693 → 404 (8 ms)

Target `restful-booker`, correlation ID `9d64d099-6023-43c4-a73c-13240428869f`, at 2026-11-28T12:06:23.693062+00:00

Response body:

```text
Not Found
```


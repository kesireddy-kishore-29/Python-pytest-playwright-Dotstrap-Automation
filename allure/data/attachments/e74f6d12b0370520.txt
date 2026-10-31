# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (189 ms)

Target `restful-booker`, correlation ID `e19ac85d-5300-463e-a80d-080dc667d3ec`, at 2026-10-31T09:52:07.937314+00:00

Request body:

```json
{
  "firstname": "qa-guest-26d35507",
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
  "bookingid": 722,
  "booking": {
    "firstname": "qa-guest-26d35507",
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

## 2. DELETE https://restful-booker.herokuapp.com/booking/722 → 201 (57 ms)

Target `restful-booker`, correlation ID `7b985e01-219a-44eb-aca7-e5e385d00c48`, at 2026-10-31T09:52:08.127071+00:00

Response body:

```text
Created
```

## 3. GET https://restful-booker.herokuapp.com/booking/722 → 404 (58 ms)

Target `restful-booker`, correlation ID `fd1d428a-7235-4e8a-8504-2d1f65a331f2`, at 2026-10-31T09:52:08.183802+00:00

Response body:

```text
Not Found
```

## 4. GET https://restful-booker.herokuapp.com/booking/722 → 404 (57 ms)

Target `restful-booker`, correlation ID `90832c2a-3580-4308-9745-093d32959106`, at 2026-10-31T09:52:08.242670+00:00

Response body:

```text
Not Found
```


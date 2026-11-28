# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (45 ms)

Target `restful-booker`, correlation ID `d67e120d-6bf1-4b03-a0b9-275802602db6`, at 2026-11-28T12:06:23.711040+00:00

Request body:

```json
{
  "firstname": "qa-keep-5852f65c",
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
  "bookingid": 2696,
  "booking": {
    "firstname": "qa-keep-5852f65c",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/2696 → 403 (8 ms)

Target `restful-booker`, correlation ID `a447fbf8-d3eb-4c2e-b4d4-756b1eb4f041`, at 2026-11-28T12:06:23.756574+00:00

Request body:

```json
{
  "firstname": "qa-changed-6c49819c",
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

## 3. GET https://restful-booker.herokuapp.com/booking/2696 → 200 (8 ms)

Target `restful-booker`, correlation ID `99ca0105-f21f-4eb6-9d10-93d507d84a39`, at 2026-11-28T12:06:23.764918+00:00

Response body:

```json
{
  "firstname": "qa-keep-5852f65c",
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

## 4. GET https://restful-booker.herokuapp.com/booking/2696 → 200 (8 ms)

Target `restful-booker`, correlation ID `67ee8898-cd75-4a67-8e09-a671344a3fc7`, at 2026-11-28T12:06:23.774221+00:00

Response body:

```json
{
  "firstname": "qa-keep-5852f65c",
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

## 5. DELETE https://restful-booker.herokuapp.com/booking/2696 → 201 (8 ms)

Target `restful-booker`, correlation ID `a33d14c3-4b94-41ff-8da2-78fd4517691f`, at 2026-11-28T12:06:23.782659+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/2696 → 404 (8 ms)

Target `restful-booker`, correlation ID `ee7a8c9a-c488-4d79-bf5d-9b282d592d8e`, at 2026-11-28T12:06:23.790974+00:00

Response body:

```text
Not Found
```


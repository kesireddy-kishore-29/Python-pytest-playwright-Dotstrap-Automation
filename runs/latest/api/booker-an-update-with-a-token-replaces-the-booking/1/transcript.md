# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (33 ms)

Target `restful-booker`, correlation ID `d0e5e05a-f606-4524-ba86-10874cc7adc7`, at 2026-11-28T12:06:23.693904+00:00

Request body:

```json
{
  "firstname": "qa-guest-42d2d5c2",
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
  "bookingid": 2694,
  "booking": {
    "firstname": "qa-guest-42d2d5c2",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/2694 → 200 (8 ms)

Target `restful-booker`, correlation ID `8f82a878-578a-4648-af53-4c168c82ef6b`, at 2026-11-28T12:06:23.727588+00:00

Request body:

```json
{
  "firstname": "qa-guest-fe0a3105",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-12-12",
    "checkout": "2026-12-15"
  },
  "additionalneeds": "None"
}
```

Response body:

```json
{
  "firstname": "qa-guest-fe0a3105",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-12-12",
    "checkout": "2026-12-15"
  },
  "additionalneeds": "None"
}
```

## 3. GET https://restful-booker.herokuapp.com/booking/2694 → 200 (8 ms)

Target `restful-booker`, correlation ID `71b0bc1e-0cf1-4804-9c90-09e7c1d8f0fa`, at 2026-11-28T12:06:23.736381+00:00

Response body:

```json
{
  "firstname": "qa-guest-fe0a3105",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-12-12",
    "checkout": "2026-12-15"
  },
  "additionalneeds": "None"
}
```

## 4. GET https://restful-booker.herokuapp.com/booking/2694 → 200 (8 ms)

Target `restful-booker`, correlation ID `4ea0d613-f363-4376-af9c-de92b0abc493`, at 2026-11-28T12:06:23.745302+00:00

Response body:

```json
{
  "firstname": "qa-guest-fe0a3105",
  "lastname": "Lovelace",
  "totalprice": 99,
  "depositpaid": false,
  "bookingdates": {
    "checkin": "2026-12-12",
    "checkout": "2026-12-15"
  },
  "additionalneeds": "None"
}
```

## 5. DELETE https://restful-booker.herokuapp.com/booking/2694 → 201 (8 ms)

Target `restful-booker`, correlation ID `b6588be9-7f1f-4ecf-bd1b-ad88e1557076`, at 2026-11-28T12:06:23.753505+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/2694 → 404 (10 ms)

Target `restful-booker`, correlation ID `90792b84-c0f9-4b5f-ac2d-62f3f0c31303`, at 2026-11-28T12:06:23.761229+00:00

Response body:

```text
Not Found
```


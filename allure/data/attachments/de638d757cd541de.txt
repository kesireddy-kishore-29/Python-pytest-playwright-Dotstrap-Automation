# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (190 ms)

Target `restful-booker`, correlation ID `271d6a4f-8035-4ff5-a7a3-face0cb85284`, at 2026-10-31T09:52:08.420070+00:00

Request body:

```json
{
  "firstname": "qa-keep-9c367d3b",
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
  "bookingid": 731,
  "booking": {
    "firstname": "qa-keep-9c367d3b",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/731 → 403 (59 ms)

Target `restful-booker`, correlation ID `781babb0-37b2-4399-adb1-3690c13a7e8d`, at 2026-10-31T09:52:08.611266+00:00

Request body:

```json
{
  "firstname": "qa-changed-e98f3f7c",
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

```text
Forbidden
```

## 3. GET https://restful-booker.herokuapp.com/booking/731 → 200 (60 ms)

Target `restful-booker`, correlation ID `5ef74a9d-9f5f-4dc1-bcd6-35264c5da8d7`, at 2026-10-31T09:52:08.670966+00:00

Response body:

```json
{
  "firstname": "qa-keep-9c367d3b",
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

## 4. GET https://restful-booker.herokuapp.com/booking/731 → 200 (60 ms)

Target `restful-booker`, correlation ID `dceee1a9-df88-4b59-925a-e718d0cda04c`, at 2026-10-31T09:52:08.733990+00:00

Response body:

```json
{
  "firstname": "qa-keep-9c367d3b",
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

## 5. DELETE https://restful-booker.herokuapp.com/booking/731 → 201 (59 ms)

Target `restful-booker`, correlation ID `715993cb-ebde-432b-901b-d8b054b786c7`, at 2026-10-31T09:52:08.793948+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/731 → 404 (60 ms)

Target `restful-booker`, correlation ID `8d60c919-88a2-4013-8d73-e91207ea7539`, at 2026-10-31T09:52:08.853614+00:00

Response body:

```text
Not Found
```


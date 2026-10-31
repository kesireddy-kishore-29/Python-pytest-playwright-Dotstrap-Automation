# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (192 ms)

Target `restful-booker`, correlation ID `e2bda839-854a-4be1-ab68-53521dccf8cf`, at 2026-10-31T09:52:07.936186+00:00

Request body:

```json
{
  "firstname": "qa-keep-af0dcec2",
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
  "bookingid": 723,
  "booking": {
    "firstname": "qa-keep-af0dcec2",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/723 → 403 (56 ms)

Target `restful-booker`, correlation ID `86ed6648-10b9-4415-8c09-02996616644f`, at 2026-10-31T09:52:08.128524+00:00

Request body:

```json
{
  "firstname": "qa-changed-9aa34d1f",
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

## 3. GET https://restful-booker.herokuapp.com/booking/723 → 200 (56 ms)

Target `restful-booker`, correlation ID `6a45d638-e3af-4552-b968-2733305b2b19`, at 2026-10-31T09:52:08.185206+00:00

Response body:

```json
{
  "firstname": "qa-keep-af0dcec2",
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

## 4. GET https://restful-booker.herokuapp.com/booking/723 → 200 (57 ms)

Target `restful-booker`, correlation ID `97555598-711f-4b05-bbb3-f1cddae04e3b`, at 2026-10-31T09:52:08.243116+00:00

Response body:

```json
{
  "firstname": "qa-keep-af0dcec2",
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

## 5. DELETE https://restful-booker.herokuapp.com/booking/723 → 201 (56 ms)

Target `restful-booker`, correlation ID `37967eb4-a088-4185-8e80-5808753bb3af`, at 2026-10-31T09:52:08.300128+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/723 → 404 (57 ms)

Target `restful-booker`, correlation ID `7720f249-9ee1-4a7f-b2af-569e0de07947`, at 2026-10-31T09:52:08.356634+00:00

Response body:

```text
Not Found
```


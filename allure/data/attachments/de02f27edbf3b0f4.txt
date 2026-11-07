# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (203 ms)

Target `restful-booker`, correlation ID `2893abca-9a22-4813-abf6-6abbca3266c4`, at 2026-11-07T10:32:27.257063+00:00

Request body:

```json
{
  "firstname": "qa-keep-41558243",
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
  "bookingid": 815,
  "booking": {
    "firstname": "qa-keep-41558243",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/815 → 403 (63 ms)

Target `restful-booker`, correlation ID `5210eea9-e0b8-4bab-9224-8cb59b411086`, at 2026-11-07T10:32:27.460915+00:00

Request body:

```json
{
  "firstname": "qa-changed-416cc27f",
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

```text
Forbidden
```

## 3. GET https://restful-booker.herokuapp.com/booking/815 → 200 (63 ms)

Target `restful-booker`, correlation ID `f1e8df49-fdef-49a7-a8aa-84711a304bc1`, at 2026-11-07T10:32:27.524201+00:00

Response body:

```json
{
  "firstname": "qa-keep-41558243",
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

## 4. GET https://restful-booker.herokuapp.com/booking/815 → 200 (63 ms)

Target `restful-booker`, correlation ID `09cd2772-b27c-46df-ba5a-c0e70712bf28`, at 2026-11-07T10:32:27.589209+00:00

Response body:

```json
{
  "firstname": "qa-keep-41558243",
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

## 5. DELETE https://restful-booker.herokuapp.com/booking/815 → 201 (62 ms)

Target `restful-booker`, correlation ID `24d0229f-00e6-4b94-b10d-e9de3eb499b4`, at 2026-11-07T10:32:27.652540+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/815 → 404 (63 ms)

Target `restful-booker`, correlation ID `43479a9b-1822-4c00-9a89-08389348580e`, at 2026-11-07T10:32:27.715113+00:00

Response body:

```text
Not Found
```


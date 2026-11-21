# API transcript

## 1. POST https://restful-booker.herokuapp.com/booking → 200 (27 ms)

Target `restful-booker`, correlation ID `2749b65c-40c6-4cde-8077-afb008dba329`, at 2026-11-21T11:32:13.070091+00:00

Request body:

```json
{
  "firstname": "qa-keep-f3bc79ee",
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
  "bookingid": 649,
  "booking": {
    "firstname": "qa-keep-f3bc79ee",
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

## 2. PUT https://restful-booker.herokuapp.com/booking/649 → 403 (4 ms)

Target `restful-booker`, correlation ID `bbcafbf8-c555-4663-8d90-06cb6f6a16c8`, at 2026-11-21T11:32:13.097706+00:00

Request body:

```json
{
  "firstname": "qa-changed-fcf86922",
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

```text
Forbidden
```

## 3. GET https://restful-booker.herokuapp.com/booking/649 → 200 (4 ms)

Target `restful-booker`, correlation ID `87f233c5-b42b-44fc-b6a8-9d108abddcd3`, at 2026-11-21T11:32:13.101971+00:00

Response body:

```json
{
  "firstname": "qa-keep-f3bc79ee",
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

## 4. GET https://restful-booker.herokuapp.com/booking/649 → 200 (5 ms)

Target `restful-booker`, correlation ID `c5f1fdb3-bca8-47fb-a3d8-fc8f7f687514`, at 2026-11-21T11:32:13.107645+00:00

Response body:

```json
{
  "firstname": "qa-keep-f3bc79ee",
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

## 5. DELETE https://restful-booker.herokuapp.com/booking/649 → 201 (4 ms)

Target `restful-booker`, correlation ID `a677844f-3cba-416a-9c5c-d5ecdb494fdb`, at 2026-11-21T11:32:13.113133+00:00

Response body:

```text
Created
```

## 6. GET https://restful-booker.herokuapp.com/booking/649 → 404 (5 ms)

Target `restful-booker`, correlation ID `c9028725-94c6-4086-94bc-d53f3e4593e2`, at 2026-11-21T11:32:13.117366+00:00

Response body:

```text
Not Found
```


# 3. pydantic for response contracts and for configuration

- Status: accepted
- Date: 2026-10-21

## Context

An API test that reads `response.json()["token"]` passes as long as that one field exists, even
when the rest of the response changed shape. Configuration read from environment variables with
`os.environ.get` fails late and one variable at a time.

## Decision

1. Every response a test relies on is parsed into a strict pydantic model (`extra="forbid"`): an
   added, removed or mistyped field is a `ContractViolationError` that names every field, before
   any assertion runs. The reference service's models follow its OpenAPI document; Restful-Booker's
   follow what it returns.
2. Errors are modelled too: the reference service's RFC 7807 `Problem`, so a test asserts the
   status **and** the problem shape.
3. Settings are a pydantic-settings model: defaults for the public targets, overrides from
   environment variables or `.env`, secrets as `SecretStr` (never printed), and validation at
   start-up that reports every invalid value at once.
4. The live page list is a validated pydantic model too: the sign-in page cannot be added, and a
   bad pattern is refused when the run starts.

## Consequences

- A contract change on a public target fails loudly as a contract change, not as a confusing
  assertion.
- Models are code, so mypy checks every field a test reads.
- Strictness has a cost on a public target that changes on its own: a new field fails the tests
  until the model is updated. That is the point.

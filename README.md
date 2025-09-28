## Fun Facts API

### About

Tells a different fun fact every day. Written in hexagonal architecture.

### Endpoints

- `/v1/fun-facts/today` returns today's fun fact.
- `/v1/fun-facts/recent` returns last 10 days' fun facts.

### Running locally
1. Add `MISTRAL_API_KEY` to `.env`
2. Run `docker-compose up`

### Running Tests
1. Install locally with `pip install -e .` on your venv.
2. Run with one of the following:
    - `pytest` runs all tests
    - `pytest test/unit/ -m unit` runs only the unit tests.
    - `pytest test/integration/ -m integration` runs only the integration tests.
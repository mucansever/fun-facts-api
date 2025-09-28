## Fun Facts API

### About
Tells a different fun fact every day. Written in hexagonal architecture. I deployed it so that you can try it out via:
- API: https://fun-facts-api-production.up.railway.app/v1/fun-facts/today
- Website: [https://mucansever.github.io/fun-facts](https://mucansever.github.io/#/v1/fun-facts/today)

### Endpoints
`/v1/fun-facts/today` returns today's fun fact.
```
{
    "date": "2025-09-28",
    "fact": "The Eiffel Tower can be seen from as far as 42 miles away on a clear day!"
}
```
`/v1/fun-facts/recent` returns last 10 days' fun facts.
```
[
    {
        "date": "2025-09-28",
        "fact": "The Eiffel Tower can be seen from as far as 42 miles away on a clear day!"
    },
    {
        "date": "2025-09-27",
        "fact": "Whales were once land animals but returned to the sea around 50 million years ago."
    },
    ...
]
```

### Running locally
1. Add `MISTRAL_API_KEY` to `.env`
2. Run `docker-compose up`

### Running Tests
1. Install locally with `pip install -e .` on your venv.
2. Run with one of the following:
    - `pytest` runs all tests
    - `pytest test/unit/ -m unit` runs only the unit tests.
    - `pytest test/integration/ -m integration` runs only the integration tests.

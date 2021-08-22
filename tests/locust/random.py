from locust import HttpUser, between, task
from data import gen_payload, gen_invalid_payload


class RandomizedTaxiUser(HttpUser):

    # wait between requests from one user for between 1 and 5 seconds.
    wait_time = between(0, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payloads = gen_payload()
        self.invalid_payload = gen_invalid_payload()

    @task(5)
    def test_valid_payload(self):
        payload = next(self.payloads)
        self.client.post("/predict", json=payload)

    @task(1)
    def test_invalid_payload(self):
        payload = next(self.invalid_payload)
        with self.client.post(
            "/predict", json=payload, catch_response=True
        ) as response:
            if response.status_code != 422:
                response.failure(
                    f"Wrong response. Expected status code 422, "
                    f"got {response.status_code}"
                )
            else:
                response.success()

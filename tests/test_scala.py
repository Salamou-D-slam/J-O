from locust import HttpUser, task, between

class JoUser(HttpUser):
    wait_time = between(1, 5)  # temps entre actions

    @task
    def browse_home(self):
        self.client.get("/")

    @task
    def login(self):
        self.client.post("/login", data={
            "email": "test@test.com",
            "password": "test19000"
        })

    @task
    def payment(self):
        self.client.post("/paiement/test_solo", data={
            "pers1_nom": "test",
            "pers1_prenom": "user",
            "pers1_email": "test@gmail.com",
            "nom_card": "test user",
            "card_number": 1234123412341234,
            "expiration_card": 229,
            "CVV_card": 111
        })

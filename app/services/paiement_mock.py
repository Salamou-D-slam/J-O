import random

class FakePaymentGateway:
    def __init__(self, force_result=None): # force_result: "success" ou "failure" ou None pour aléatoire

        self.force_result = force_result

    def process_paiement(self, card_number, montant):

        if self.force_result is not None:
            success = self.force_result == "success"
        else:
            success = random.choice([True, False])

        if success:
            return {"status": "success"}
        else:
            return {"status": "failure", "error": "Paiement refusé"}

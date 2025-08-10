import random
from ..models import Epreuve, Offre, User
from ..extensions import db, login_manager


class FakePaymentGateway:
    def __init__(self, force_result=None): # force_result: "success" ou "failure" ou None pour aléatoire

        self.force_result = force_result

    def process_paiement(self, card_number, montant):
        print(f"[MOCK] Simulation paiement de {montant}€ avec carte {card_number}")

        if self.force_result is not None:
            success = self.force_result == "success"
        else:
            success = random.choice([True, False])

        if success:
            return {"status": "success", "transaction_id": f"TXN{random.randint(100000, 999999)}"}
        else:
            return {"status": "failure", "error": "Paiement refusé"}

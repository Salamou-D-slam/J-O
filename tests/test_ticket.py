from configtest import client


def test_ajouter_ticket(client):
    # Se connecter d’abord
    client.post("/login", data={"email":"test@test.com","password":"test19000"}, follow_redirects=True)
    # Ajouter ticket
    response = client.post("/tickets/add", data={"type_offre": "solo", "id_epreuve": 1}, follow_redirects=True)
    assert b"Ticket ajouté" in response.data

def test_consulter_tickets(client):
    client.post("/login", data={"email":"test@test.com","password":"test19000"}, follow_redirects=True)
    response = client.get("/tickets")
    assert b"Mes tickets" in response.data

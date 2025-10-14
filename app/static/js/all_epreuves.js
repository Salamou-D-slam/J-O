document.addEventListener("DOMContentLoaded", async () => {
  const container = document.querySelector("#epreuves-card");
  const loader = document.querySelector("#loading");

  try {
    const res = await fetch("/api/epreuves");
    const epreuves = await res.json();

    // Supprimer le spinner
    loader.style.display = "none";

    // Afficher les cartes Bootstrap
    epreuves.forEach(e => {
      const card = document.createElement("div");
      card.className = "col-md-4 mb-3";
      card.innerHTML = `
        <section class="section-epreuves">
 
        {% for epreuve in epreuves %}

        
            <div class="card card-epreuve" style="width: 29rem;">

                {% if epreuve.image_filename %}
                <img src="{{ url_for('static', filename='uploads/image/' + epreuve.image_filename) }}"  alt="Image de l'épreuve">
                {% endif %}

                <div class="card-body">
                    <h5 class="card-title"><strong>{{ epreuve.nom_epreuve }}</strong></h5> 
                    <p class="card-text">Date de l'épreuve: ({{ epreuve.date_epreuve.strftime('%d/%m/%Y')}})</p>

                    <div class="d-grid gap-2 col-6 mx-auto">
                        <a href="{{ url_for('main.epreuve_details_front', nom_epreuve=epreuve.nom_epreuve) }}" class="btn btn-primary">Plus de détails</a>
                    </div>

                
                </div>
            </div>
            
            {% endfor %}
    </section>
      `;
      container.appendChild(card);
    });

  } catch (error) {
    loader.innerHTML = `<div class="alert alert-danger">Erreur de chargement 😢</div>`;
  }
});

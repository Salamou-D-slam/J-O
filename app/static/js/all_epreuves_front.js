document.addEventListener("DOMContentLoaded", () => {

  const loader = document.getElementById('loader');
  const section = document.getElementById('epreuves-card');


  section.innerHTML = '';
  if (loader) loader.style.display = 'block';

  fetch('/api/epreuves')
    .then(res => res.json())
    .then(epreuves => {

      if (loader) loader.style.display = 'none';

      epreuves.forEach(epreuve => {
        const card = document.createElement('div');
        card.className = 'card card-epreuve m-2';
        card.style.width = '29rem';
        card.innerHTML = `
          ${epreuve.image_filename ? `<img src="/static/uploads/image/${epreuve.image_filename}" class="card-img-top" alt="">` : ''}
          <div class="card-body">
            <h5 class="card-title"><strong>${epreuve.nom_epreuve}</strong></h5>
            <p class="card-text">Date : ${epreuve.date_epreuve}</p>
            <div class="d-grid gap-2 col-6 mx-auto">
              <a href="/epreuves-${encodeURIComponent(epreuve.nom_epreuve)}" class="btn btn-primary">Plus de détails</a>
            </div>
          </div>
        `;
        section.appendChild(card);
      });
    })
    .catch(error => console.error("Erreur :", error));
});

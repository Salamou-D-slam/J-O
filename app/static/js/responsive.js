function responsiveSection() {
  const zone = document.getElementById("section-card-zone");
  if (window.innerWidth > 1316) {
    zone.innerHTML = `
    <section class="section container-card section-infos">

        <div class="card-offre">
            <div class="card text-bg-info mb-3" style="max-width: 26rem; border-radius: 100%;">
              <div class="card-body">
                <h5 class="card-title">Offre solo</h5>
                <hr>
                  <p class="card-text">L'offre duo d'une épreuve est une offre contenient deux personnes. Parfait pour deux ami.e.s</p>
              </div>
              </div>

            <div class="card text-bg-dark mb-3" style="max-width: 26rem; border-radius: 100%;">
              <div class="card-body">
                <h5 class="card-title">Offre duo</h5>
                                <hr>

                  <p class="card-text">L'offre duo d'une épreuve est une offre contenient deux personnes. Parfait pour deux ami.e.s</p>
              </div>
              </div>


            <div class="card text-bg-danger mb-3" style="max-width: 26rem; border-radius: 100%;">
              <div class="card-body">
                  <h5 class="card-title">Offre family</h5>
                                  <hr>

                  <p class="card-text">L'offre family d'une épreuve est une offre qui contentient quatre personnes. Parfait pour une famille de ou un groupe d'ami.e.s </p>
              </div>
            </div>
        </div>

        <div class="card-info">
            <div class="card text-bg-warning  mb-3" style="max-width: 26rem; border-radius: 100%;">
              <div class="card-body">
                  <h5 class="card-title">Nous contacter</h5> 
                  <hr>
                  <p class="card-text">Vous pouvez nous contacter via la page de contact, veillez mettre un email valide pour qu'on puisse vous répondre. </p>
              </div>
              </div>

            <div class="card text-bg-success  mb-3" style="max-width: 26rem; border-radius: 100%;">
              <div class="card-body jour-epreuve">
                  <h5 class="card-title">Le jour de l'épreuve</h5>
                    <hr>
                  <p class="card-text">Veuillez vous munir de vos pieces d'identié ainsi que le QR code présent dans le ticket. 
                    Notez que le QR code ne peut être scanner qu'une seule fois, donc les personnes qui ont un billet d'une offre duo ou family doivent entrer TOUS en même temps.</p>
                    <a href="{{ url_for('main.contact')}}" type="button" class="btn btn-outline-primary btn-card-contact">Voir Contact</a>

              </div>
            </div>
        </div>

    </section>
    `;
  } else {
    zone.innerHTML = ` 
    <section>
        <h1 class="text-center"><strong>Informations</strong></h1>
      
      <div class="accordion" id="accordionExample">
    <div class="accordion-item">
      <h2 class="accordion-header">
        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
          <strong>Offre solo</strong>
        </button>
      </h2>
      <div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
        <div class="accordion-body">
                  <p class="card-text">L'offre duo d'une épreuve est une offre contenient deux personnes. Parfait pour deux ami.e.s</p>
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
         <strong>Offre duo</strong> 
        </button>
      </h2>
      <div id="collapseTwo" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
        <div class="accordion-body">
              <p class="card-text">L'offre duo d'une épreuve est une offre contenient deux personnes. Parfait pour deux ami.e.s</p>
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
          <strong>Offre family</strong>
        </button>
      </h2>
      <div id="collapseThree" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
        <div class="accordion-body">
                  <p class="card-text">L'offre family d'une épreuve est une offre qui contentient quatre personnes. Parfait pour une famille de ou un groupe d'ami.e.s </p>
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
          <strong>Nous contacter</strong>
        </button>
      </h2>
      <div id="collapseFour" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
        <div class="accordion-body">
            <p class="card-text">Vous pouvez nous contacter via la page de contact, veillez mettre un email valide pour qu'on puisse vous répondre. </p>
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFive" aria-expanded="false" aria-controls="collapseFive">
          <strong>Le jour de l'épreuve</strong>
        </button>
      </h2>
      <div id="collapseFive" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
        <div class="accordion-body">
              <p class="card-text">Veuillez vous munir de vos pieces d'identié ainsi que le QR code présent dans le ticket. 
                    Notez que le QR code ne peut être scanner qu'une seule fois, donc les personnes qui ont un billet d'une offre duo ou family doivent entrer TOUS en même temps.</p>
              <a href="{{ url_for('main.contact')}}" type="button" class="btn btn-outline-primary">Voir Contact</a>
      </div>
    </div>
  </div>
</section>
    `;
  }
}
responsiveSection();
window.addEventListener("resize", responsiveSection);
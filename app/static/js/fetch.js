// -----------------PAGE DE PAIEMENT-------------------------------

(() => {
  'use strict';
  const forms = document.querySelectorAll('.needs-validation');
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });
})();

//----------------------PAGE DE SCAN DE TICKET------------------------

  function simulateScan() {
      const ticketId = document.getElementById("ticket_id").value;
      fetch(`/api/validate_ticket/${ticketId}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("result").innerText = data.message;
        });
  }



const form = document.getElementById('form-singin');

const success = document.getElementById('sMessage');
const fail = document.getElementById('eMessage');

const sButton = document.getElementById('sButton');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const formData = new FormData(form);

  fetch('/AddEmail', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (response.ok) {
      success.style.display = 'block';
      sButton.style.display = 'none';
      form.reset();
    } else {
        throw new Error('¡Error Formulario!');
    }
  })
  .catch(error => {
    console.error(error);
    fail.style.display = 'block';
    sButton.style.display = 'none';
  });
});

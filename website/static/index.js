const alerts = document.querySelectorAll('.alert');

// Itera sobre cada alert y configura un temporizador
alerts.forEach(alert => {
  setTimeout(() => {
    alert.classList.add('fade'); // Agrega la animación de desvanecimiento
    alert.classList.remove('show'); // Elimina la clase 'show'

    // Elimina el elemento del DOM después de que la animación termina
    setTimeout(() => {
      alert.remove();
    }, 150); // Tiempo adicional para la animación
  }, 4000); // 3000ms = 3 segundos
});

function deleteNote(noteId){
  fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId})
  }).then((_res)=> {
    window.location.href = "/dashboard";
  })
}
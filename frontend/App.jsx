async function loadScore() {
  // Para prototipo: se carga JSON estático generado por worker.py
  const response = await fetch('../uploads/output/score.json');
  const hits = await response.json();
  const container = document.getElementById('score');
  container.innerHTML = '';

  hits.forEach(hit => {
    const div = document.createElement('div');
    div.className = 'note';
    div.textContent = `${hit.type} - ${hit.time}s`;
    container.appendChild(div);
  });

  // Resaltar golpes cada 500ms (simulación)
  let i = 0;
  const interval = setInterval(() => {
    if (i >= hits.length) { clearInterval(interval); return; }
    container.children[i].classList.add('hit');
    setTimeout(() => container.children[i].classList.remove('hit'), 400);
    i++;
  }, 500);
}

// Ejemplo: carga la partitura al abrir la página
window.onload = loadScore;

// Función de subir archivo
document.getElementById('send').onclick = async () => {
  const fileInput = document.getElementById('upload');
  if (!fileInput.files.length) return alert('Selecciona un MP3');
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('mp3', file);

  const res = await fetch('/upload', { method: 'POST', body: formData });
  if (res.ok) alert('Archivo subido correctamente. Procesa con el backend.');
  else alert('Error al subir el archivo');
};

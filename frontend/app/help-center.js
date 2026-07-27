(() => {
  const help = document.querySelector(".help-card");
  if (!help) return;

  help.id = "ayuda";
  help.classList.add("help-center");
  help.innerHTML = `
    <div class="help-center-heading">
      <div>
        <p class="eyebrow">Ayuda y transparencia</p>
        <h2>Cómo usar Mi Casa Segura</h2>
        <p>La aplicación traduce criterios técnicos a controles comprensibles para propietarios. No reemplaza planos, estudios, licencias ni una evaluación profesional del caso real.</p>
      </div>
      <span class="help-center-version">MVP 1.0</span>
    </div>

    <div class="help-center-grid">
      <section>
        <h3>Qué puedes hacer</h3>
        <ul>
          <li>Revisar tu obra por etapas.</li>
          <li>Buscar preguntas en lenguaje cotidiano.</li>
          <li>Consultar medidas y reglas técnicas.</li>
          <li>Reconocer señales para revisar o detener.</li>
          <li>Guardar localmente el avance de “Mi obra”.</li>
        </ul>
      </section>

      <section>
        <h3>Qué no hace</h3>
        <ul>
          <li>No calcula una estructura particular.</li>
          <li>No confirma la seguridad de una vivienda.</li>
          <li>No diagnostica grietas mediante una descripción.</li>
          <li>No sustituye al profesional responsable.</li>
          <li>No autoriza trabajos ni reemplaza trámites municipales.</li>
        </ul>
      </section>

      <section>
        <h3>Privacidad</h3>
        <p>El perfil “Mi obra” se guarda en este dispositivo. Puedes editarlo o eliminarlo desde la aplicación. Revisa cómo funcionan el buscador, la API y los canales de consulta.</p>
        <a href="/politica-privacidad.html">Leer política de privacidad</a>
      </section>

      <section>
        <h3>Fuentes y revisión</h3>
        <p>La base utiliza principalmente el Reglamento Nacional de Edificaciones y otras fuentes oficiales peruanas. Cada respuesta destacada indica clasificación y fecha de revisión.</p>
        <a href="/biblioteca-tecnica.html">Abrir biblioteca técnica</a>
      </section>
    </div>

    <div class="help-center-actions">
      <a class="primary-button" data-professional-help="general" href="/contacto.html?origen=mi-casa-segura">Solicitar orientación profesional</a>
      <a class="help-center-secondary" href="https://www.construccionsegura.org.pe/" target="_blank" rel="noopener noreferrer">Visitar Construcción Segura</a>
    </div>
  `;
})();

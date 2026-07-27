(() => {
  window.MI_CASA_SEGURA_PROBLEMS = [
    {
      id: "grietas-deformaciones",
      icon: "⌁",
      title: "Grietas, fisuras o deformaciones",
      summary: "Rajaduras que aparecieron, crecieron o afectan muros, columnas, vigas o techos.",
      questions: [
        { id: "growing", text: "¿La grieta creció, volvió a aparecer o aumentó después de un sismo o una excavación cercana?", severity: "red" },
        { id: "structural", text: "¿Atraviesa una columna, viga, losa o muro que soporta carga?", severity: "red" },
        { id: "movement", text: "¿También notas inclinación, hundimiento, puertas trabadas o deformación del techo?", severity: "red" },
        { id: "finish", text: "¿Parece limitarse al tarrajeo o acabado, sin otros cambios visibles?", severity: "yellow" }
      ],
      redAction: "No tapes ni resanes la grieta. Restringe el área si existe desprendimiento o deformación y solicita una evaluación profesional.",
      yellowAction: "Registra fecha, longitud aproximada y fotografías seguras. Comprueba si cambia antes de reparar el acabado.",
      greenAction: "Mantén observación y evita ocultar la zona hasta confirmar que se trata solamente de un acabado superficial."
    },
    {
      id: "suelo-hundimiento",
      icon: "▽",
      title: "Hundimiento o movimiento de tierra",
      summary: "Suelo que baja, talud que se mueve, excavación inestable o grietas en el terreno.",
      questions: [
        { id: "active", text: "¿Hay tierra desprendiéndose, grietas nuevas en el suelo o un talud que sigue moviéndose?", severity: "red" },
        { id: "foundation", text: "¿El movimiento está junto a una cimentación, muro de contención o vivienda vecina?", severity: "red" },
        { id: "water", text: "¿Apareció agua, filtración o barro dentro de la excavación?", severity: "yellow" },
        { id: "fill", text: "¿La zona fue rellenada o removida anteriormente y no conoces cómo se compactó?", severity: "yellow" }
      ],
      redAction: "Detén la excavación, aleja personas y materiales del borde y solicita evaluación del terreno y de las estructuras cercanas.",
      yellowAction: "No vacíes ni rellenes para ocultar el problema. Verifica drenaje, suelo encontrado y estabilidad antes de continuar.",
      greenAction: "Conserva vigilancia durante la excavación y protege el borde, especialmente ante lluvia o vibraciones."
    },
    {
      id: "elemento-intervenido",
      icon: "⚒",
      title: "Cortaron una columna, viga, muro o acero",
      summary: "Perforaciones, demoliciones o cortes realizados para abrir vanos o pasar instalaciones.",
      questions: [
        { id: "steel", text: "¿Cortaron barras de acero, estribos o una parte de una columna o viga?", severity: "red" },
        { id: "opening", text: "¿Abrieron un vano nuevo o retiraron un muro sin planos ni revisión previa?", severity: "red" },
        { id: "support", text: "¿El elemento sostiene techo, escalera, otro piso o una construcción vecina?", severity: "red" },
        { id: "pipe", text: "¿La intervención fue para colocar una tubería, ducto o caja eléctrica?", severity: "yellow" }
      ],
      redAction: "Suspende la demolición o perforación. No improvises un resane ni vuelvas a cargar el elemento hasta contar con una evaluación estructural.",
      yellowAction: "Comprueba en planos la ruta de instalaciones y la función del elemento antes de ampliar la perforación.",
      greenAction: "Aun en elementos no estructurales, verifica que la intervención no afecte instalaciones ocultas ni seguridad de uso."
    },
    {
      id: "humedad-salitre",
      icon: "≈",
      title: "Humedad, filtración o salitre",
      summary: "Manchas, pintura levantada, moho, eflorescencia o agua en muros y techos.",
      questions: [
        { id: "electrical", text: "¿La humedad alcanza el tablero, tomacorrientes, cables o artefactos eléctricos?", severity: "red" },
        { id: "ceiling", text: "¿Hay cielo raso abombado, material suelto o riesgo de desprendimiento?", severity: "red" },
        { id: "activeLeak", text: "¿La filtración continúa activa o aumenta cuando llueve o se usa una instalación?", severity: "yellow" },
        { id: "recurring", text: "¿Ya pintaron o resanaron antes y el problema reapareció?", severity: "yellow" }
      ],
      redAction: "Corta la energía del circuito afectado solo desde un punto seguro y evita permanecer bajo materiales abombados. Atiende primero la fuente de agua.",
      yellowAction: "Identifica si proviene de lluvia, tubería, desagüe o ascenso desde el suelo. No apliques pintura ni ácido antes de corregir la causa.",
      greenAction: "Mantén ventilación y observación, pero confirma que no exista una fuente oculta antes de renovar el acabado."
    },
    {
      id: "concreto-defectuoso",
      icon: "▦",
      title: "Concreto con vacíos, segregación o acero visible",
      summary: "Cangrejeras, desprendimientos, mezcla lavada, grietas tempranas o refuerzo expuesto.",
      questions: [
        { id: "steelVisible", text: "¿Se ve acero, hay barras sueltas o falta concreto alrededor del refuerzo?", severity: "red" },
        { id: "deepVoid", text: "¿Los vacíos son profundos, atraviesan el elemento o están en una unión de columna y viga?", severity: "red" },
        { id: "deformation", text: "¿El elemento presenta deformación, grietas crecientes o desprendimiento?", severity: "red" },
        { id: "surface", text: "¿El defecto parece superficial y localizado, sin acero visible?", severity: "yellow" }
      ],
      redAction: "No cubras el defecto con mortero ni cargues el elemento. Solicita evaluación antes de decidir reparación, refuerzo o retiro.",
      yellowAction: "Delimita el área, registra profundidad y extensión, y verifica la causa antes de resanar.",
      greenAction: "Controla el curado y revisa la superficie antes de aplicar acabados."
    },
    {
      id: "desague",
      icon: "⇣",
      title: "Desagüe lento, gorgoteo, olor o retorno",
      summary: "Mal olor, sonidos, rebose, atoros frecuentes o aguas residuales que regresan.",
      questions: [
        { id: "return", text: "¿Están retornando aguas residuales o rebosando dentro de la vivienda?", severity: "red" },
        { id: "multiple", text: "¿El problema aparece en varios aparatos al mismo tiempo?", severity: "yellow" },
        { id: "trap", text: "¿El olor aparece en un punto poco usado o con posible trampa seca?", severity: "yellow" },
        { id: "recent", text: "¿Empezó después de una remodelación o cambio de tuberías?", severity: "yellow" }
      ],
      redAction: "Evita contacto con aguas residuales, restringe el área y no continúes usando los aparatos conectados hasta controlar el retorno.",
      yellowAction: "Revisa ventilación, trampas, registros, pendiente y posibles obstrucciones. No selles una ventilación para eliminar el olor.",
      greenAction: "Mantén agua en las trampas y observa si el problema vuelve a presentarse."
    },
    {
      id: "electricidad",
      icon: "⚡",
      title: "Chispas, calentamiento o llave que se dispara",
      summary: "Tomacorriente caliente, olor a quemado, zumbido, descarga o interrupciones repetidas.",
      questions: [
        { id: "sparks", text: "¿Hay chispas, humo, olor a quemado o partes derretidas?", severity: "red" },
        { id: "shock", text: "¿Alguien recibió una descarga o un artefacto tiene tensión en su carcasa?", severity: "red" },
        { id: "heat", text: "¿Un tomacorriente, cable, extensión o tablero se calienta?", severity: "red" },
        { id: "trip", text: "¿La llave se dispara repetidamente al conectar una carga?", severity: "yellow" }
      ],
      redAction: "Desconecta la energía desde un punto seguro, no toques partes dañadas ni uses agua y solicita revisión de un electricista competente.",
      yellowAction: "No reemplaces la llave por otra de mayor capacidad sin revisar el circuito, conductores, conexiones y carga.",
      greenAction: "Mantén libres los tableros, evita extensiones permanentes y revisa periódicamente conexiones y protecciones."
    },
    {
      id: "gas-combustion",
      icon: "◉",
      title: "Olor a gas o combustión deficiente",
      summary: "Olor, llama inusual, hollín, mareo o artefacto instalado en espacio poco ventilado.",
      questions: [
        { id: "smell", text: "¿Percibes olor a gas o escuchas una posible fuga?", severity: "red" },
        { id: "symptoms", text: "¿Alguien presenta mareo, dolor de cabeza, náusea o somnolencia cerca del artefacto?", severity: "red" },
        { id: "flame", text: "¿La llama es amarilla, produce hollín o se apaga con frecuencia?", severity: "red" },
        { id: "ventilation", text: "¿El artefacto está en un ambiente cerrado o sin ventilación suficiente?", severity: "yellow" }
      ],
      redAction: "No enciendas ni apagues interruptores. Cierra la válvula solo si puedes hacerlo sin riesgo, ventila, evacúa y solicita atención especializada desde un lugar seguro.",
      yellowAction: "No uses el artefacto hasta verificar ventilación, conexión, regulador y evacuación de gases.",
      greenAction: "Mantén ventilación permanente y revisiones según fabricante y condiciones de uso."
    },
    {
      id: "desprendimiento",
      icon: "▱",
      title: "Desprendimiento o riesgo de caída",
      summary: "Tarrajeo, ladrillo, vidrio, baranda, revestimiento o elemento que está suelto.",
      questions: [
        { id: "overhead", text: "¿El material está sobre una zona de paso, cama, escalera o vía pública?", severity: "red" },
        { id: "loose", text: "¿Se mueve, suena hueco, presenta abombamiento o ya cayó una parte?", severity: "red" },
        { id: "railing", text: "¿Se trata de una baranda, ventana, vidrio o elemento de protección?", severity: "red" },
        { id: "small", text: "¿Es un acabado pequeño y accesible, sin riesgo de caer sobre personas?", severity: "yellow" }
      ],
      redAction: "Aísla la zona inferior y no intentes retirar el elemento desde una posición insegura. Organiza una intervención con protección adecuada.",
      yellowAction: "Revisa extensión, adherencia y causa antes de parchar solamente la parte visible.",
      greenAction: "Mantén inspección y corrige oportunamente piezas sueltas antes de que aumente el riesgo."
    },
    {
      id: "post-evento",
      icon: "!",
      title: "Daño después de sismo, incendio o inundación",
      summary: "Cambios observados después de un evento que pudo afectar la vivienda.",
      questions: [
        { id: "structuralDamage", text: "¿Aparecieron grietas nuevas en columnas, vigas, muros o escaleras?", severity: "red" },
        { id: "instability", text: "¿Hay inclinación, deformación, desprendimientos o partes que pueden caer?", severity: "red" },
        { id: "utilities", text: "¿Existe olor a gas, cables mojados, humo o tuberías rotas?", severity: "red" },
        { id: "minor", text: "¿Solo observas daños menores en pintura o acabados, sin otras señales?", severity: "yellow" }
      ],
      redAction: "No reingreses ni restablezcas servicios si existen señales de inestabilidad, gas o electricidad. Sigue las indicaciones de emergencia y solicita evaluación.",
      yellowAction: "Documenta los daños y revisa la vivienda completa antes de reparar acabados o volver a cargar áreas afectadas.",
      greenAction: "Mantén observación durante los días siguientes y registra cualquier cambio nuevo."
    }
  ];
})();

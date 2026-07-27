(() => {
  if (typeof modules === "undefined" || typeof renderModule !== "function") return;

  Object.assign(modules, {
    "terreno-movimiento": {
      eyebrow: "Antes de cimentar",
      title: "Terreno y movimiento de tierras",
      intro: "Excavar cambia el equilibrio del suelo y puede afectar al propio lote, a una ladera o a las viviendas vecinas. Revisa el terreno y la secuencia antes de retirar material.",
      topics: [
        {
          id: "reconocimiento-terreno",
          title: "Reconoce el terreno real",
          subtitle: "Natural, relleno, húmedo, inclinado o previamente intervenido.",
          blocks: [
            ["info", "Qué debes revisar", "Observa rellenos, basura enterrada, cambios de color o textura, humedad, grietas, desniveles y antecedentes de excavaciones o deslizamientos."],
            ["warning", "Señal de alerta", "Detén la excavación si aparece suelo muy blando, cavidades, agua, material orgánico, relleno no previsto o diferencias importantes entre puntos cercanos."],
            ["design", "El estudio manda", "La profundidad y solución de cimentación deben responder al suelo encontrado y al proyecto, no a una medida repetida por costumbre."]
          ],
          checks: [
            "Identifiqué si el terreno es natural, rellenado o removido.",
            "Registré humedad, grietas, cambios de suelo y construcciones vecinas.",
            "La información encontrada coincide con el estudio y los planos."
          ]
        },
        {
          id: "excavacion-segura",
          title: "Excavación y estabilidad temporal",
          subtitle: "No dejes cortes o zanjas expuestos sin control.",
          blocks: [
            ["info", "Planifica la secuencia", "Define por dónde se excava, cómo se retira el material, dónde se acopia y cómo se protege el borde. Mantén cargas y tránsito lejos de zonas inestables."],
            ["warning", "No ingreses", "No permitas personas dentro de una excavación con paredes inestables, desprendimientos, filtraciones o material acumulado junto al borde."],
            ["design", "Protección necesaria", "La necesidad de taludes, entibados, apuntalamientos o ejecución por tramos depende de la profundidad, suelo, agua y entorno."]
          ],
          checks: [
            "La excavación tiene una secuencia y acceso definidos.",
            "El material retirado no sobrecarga el borde.",
            "No existen paredes inestables ni filtraciones sin evaluar."
          ]
        },
        {
          id: "agua-drenaje-terreno",
          title: "Agua y drenaje provisional",
          subtitle: "El agua puede debilitar el fondo y desestabilizar cortes.",
          blocks: [
            ["info", "Desvía el agua", "Evita que lluvias, fugas o escorrentía ingresen a excavaciones. Protege el fondo para que no se ablande o erosione antes del vaciado."],
            ["warning", "No vacíes sobre barro", "Retirar agua superficial no basta si el fondo quedó alterado. No cubras con concreto un suelo reblandecido sin revisión."],
            ["design", "Solución del proyecto", "Drenajes permanentes, subdrenes, muros de contención y bombeo deben responder a una solución técnica coordinada."]
          ],
          checks: [
            "La lluvia y las fugas están desviadas de la excavación.",
            "El fondo conserva la condición prevista antes del vaciado.",
            "El drenaje permanente está coordinado con cimentación y vecinos."
          ]
        }
      ]
    },
    sanitarias: {
      eyebrow: "Antes de tapar",
      title: "Instalaciones sanitarias",
      intro: "Agua, desagüe y ventilación deben coordinarse antes de vaciar, rellenar o tarrajear. Una tubería oculta debe probarse antes de quedar inaccesible.",
      topics: [
        {
          id: "trazado-sanitario",
          title: "Trazado y cruces",
          subtitle: "Coordina tuberías con estructura y arquitectura.",
          blocks: [
            ["info", "Revisa el plano", "Confirma montantes, registros, aparatos, válvulas, pendientes y recorridos antes de abrir zanjas o colocar pases."],
            ["warning", "No cortes estructura", "No atravieses vigas, columnas, muros portantes o acero para resolver un cruce improvisado."],
            ["design", "El plano manda", "Diámetros, presiones, ventilación y ubicación de registros dependen del proyecto sanitario y de los aparatos servidos."]
          ],
          checks: [
            "Los recorridos coinciden con los planos.",
            "Los pases fueron previstos antes del vaciado.",
            "No se cortó acero ni se debilitó un elemento estructural."
          ]
        },
        {
          id: "pendiente-ventilacion",
          title: "Pendiente, registros y ventilación",
          subtitle: "El desagüe necesita caída uniforme y entrada de aire.",
          blocks: [
            ["info", "Mínimos de referencia", "La IS.010 establece pendiente mínima de 1 % para tuberías de 100 mm o mayores y 1,5 % para tuberías de 75 mm o menores. La descarga del inodoro requiere como mínimo 100 mm."],
            ["warning", "Evita contrapendientes", "No corrijas un tramo mal ejecutado reduciendo diámetro ni ocultes hundimientos o uniones forzadas."],
            ["design", "Ventilación sanitaria", "La ventilación debe continuar hasta el exterior y conservar el sello de agua de los aparatos. No la selles para ocultar olores."]
          ],
          checks: [
            "La pendiente fue medida en todo el tramo.",
            "Los registros quedan accesibles para mantenimiento.",
            "La ventilación sanitaria llega al exterior."
          ]
        },
        {
          id: "pruebas-sanitarias",
          title: "Prueba antes de cerrar",
          subtitle: "Detecta fugas cuando todavía se pueden corregir.",
          blocks: [
            ["info", "Prueba la instalación", "Realiza las pruebas previstas antes de cubrir tuberías, colocar pisos o cerrar ductos. Registra fecha, tramo y resultado."],
            ["warning", "No aceptes humedad", "Una unión que gotea, pierde presión o humedece el entorno no se soluciona cubriéndola con mortero."],
            ["design", "Accesibilidad", "Válvulas, registros, bombas y equipos deben conservar acceso para inspección y mantenimiento."]
          ],
          checks: [
            "Las redes fueron probadas antes de quedar ocultas.",
            "No existen fugas, uniones forzadas ni piezas dañadas.",
            "Válvulas y registros permanecen accesibles."
          ]
        }
      ]
    },
    electricas: {
      eyebrow: "Protección de personas",
      title: "Instalaciones eléctricas",
      intro: "La instalación debe responder a cargas, circuitos, protecciones y puesta a tierra. No existe un calibre universal válido para cualquier vivienda.",
      topics: [
        {
          id: "circuitos-cargas",
          title: "Circuitos y cargas",
          subtitle: "Define qué alimentará cada circuito antes de comprar cable.",
          blocks: [
            ["info", "Cuadro de cargas", "Identifica iluminación, tomacorrientes y equipos de alta potencia. La sección del conductor y la protección dependen de carga, longitud, instalación y caída de tensión."],
            ["warning", "No aumentes la llave", "No coloques una protección de mayor amperaje para evitar disparos sin comprobar que el conductor y el circuito puedan soportarla."],
            ["design", "Diseño coordinado", "Duchas, cocinas, hornos, bombas y otros equipos pueden requerir circuitos independientes y condiciones especiales."]
          ],
          checks: [
            "Cada circuito y su carga están identificados.",
            "La protección corresponde al conductor instalado.",
            "Los equipos de alta potencia tienen solución prevista."
          ]
        },
        {
          id: "protecciones-tierra",
          title: "Termomagnético, diferencial y tierra",
          subtitle: "Cumplen funciones distintas y complementarias.",
          blocks: [
            ["info", "Protecciones básicas", "El termomagnético protege frente a sobrecargas y cortocircuitos; el diferencial reduce el riesgo por fugas de corriente. La puesta a tierra complementa la protección."],
            ["warning", "No puentes", "No anules, puentes ni reemplaces una protección por otra. Un disparo repetido indica una condición que debe investigarse."],
            ["design", "Tablero", "Los circuitos deben estar identificados y el tablero debe permitir operación y mantenimiento seguros."]
          ],
          checks: [
            "El tablero identifica cada circuito.",
            "Existen protección diferencial y puesta a tierra verificables.",
            "No hay puentes, conexiones expuestas ni calentamiento."
          ]
        },
        {
          id: "antes-de-energizar",
          title: "Antes de energizar",
          subtitle: "Revisa continuidad, aislamiento, polaridad y terminaciones.",
          blocks: [
            ["info", "Inspección final", "Confirma que cajas, canalizaciones, conductores, empalmes, tapas, tablero y equipos estén terminados y secos antes de energizar."],
            ["warning", "Detén y desconecta", "Olor a quemado, chispas, tomacorrientes calientes, partes energizadas o descargas requieren cortar la energía de forma segura y solicitar revisión."],
            ["design", "Pruebas", "Las mediciones y verificaciones deben realizarse con instrumentos y por una persona competente."]
          ],
          checks: [
            "Las cajas y empalmes están cerrados y protegidos.",
            "No hay humedad cerca de partes eléctricas.",
            "La instalación fue verificada antes de energizar."
          ]
        }
      ]
    },
    impermeabilizacion: {
      eyebrow: "Control de humedad",
      title: "Impermeabilización y humedad",
      intro: "Una mancha o salitre es un síntoma. La reparación duradera empieza identificando el origen del agua y preparando correctamente el soporte.",
      topics: [
        {
          id: "origen-humedad",
          title: "Identifica el origen",
          subtitle: "Lluvia, fuga, suelo, condensación o detalle mal resuelto.",
          blocks: [
            ["info", "Observa el patrón", "Registra cuándo aparece, hasta qué altura llega, si cambia con lluvia o uso de instalaciones y qué existe al otro lado del muro o techo."],
            ["warning", "No ocultes", "Pintar, tarrajear o sellar sin detener el ingreso de agua puede encerrar humedad y deteriorar nuevamente el acabado."],
            ["design", "Solución compatible", "El tratamiento depende del material, exposición, movimiento y origen. No existe un producto universal."]
          ],
          checks: [
            "Identifiqué cuándo y dónde aparece la humedad.",
            "Revisé fugas, lluvia, terreno y condensación.",
            "La fuente de agua se corrigió antes del acabado."
          ]
        },
        {
          id: "techos-zonas-humedas",
          title: "Techos, baños y terrazas",
          subtitle: "Pendientes, encuentros y penetraciones son puntos críticos.",
          blocks: [
            ["info", "Antes del acabado", "Verifica pendientes hacia sumideros, encuentros con muros, bordes, juntas, tuberías y pases antes de colocar revestimientos finales."],
            ["warning", "No perfores después", "Una nueva perforación puede romper la continuidad del sistema impermeable. Coordina soportes, equipos y tuberías antes de terminar."],
            ["design", "Sistema completo", "Imprimación, membrana, refuerzos, protección y compatibilidad con el acabado deben seguir la especificación del sistema."]
          ],
          checks: [
            "Las pendientes conducen el agua hacia el punto previsto.",
            "Esquinas, juntas y penetraciones tienen detalle continuo.",
            "No se perforará el sistema después de terminado."
          ]
        },
        {
          id: "prueba-impermeable",
          title: "Prueba antes de cubrir",
          subtitle: "Comprueba el sistema cuando todavía es visible.",
          blocks: [
            ["info", "Control previo", "Realiza la prueba indicada para el sistema y observa ambientes inferiores, bordes y penetraciones antes de colocar el acabado que lo ocultará."],
            ["warning", "No aceptes filtraciones", "Una prueba con pérdida o mancha no se aprueba por secado aparente. Corrige la causa y repite la verificación."],
            ["design", "Registra", "Conserva fotos, fecha, zona probada y reparación realizada para mantenimiento futuro."]
          ],
          checks: [
            "El sistema fue probado antes de cubrirse.",
            "No aparecieron pérdidas ni manchas.",
            "La prueba y reparaciones quedaron registradas."
          ]
        }
      ]
    },
    acabados: {
      eyebrow: "Antes de recibir",
      title: "Acabados",
      intro: "Los acabados no deben ocultar humedad, fisuras activas ni defectos de instalaciones. Revisa el soporte y acepta por zonas antes de pagar la etapa.",
      topics: [
        {
          id: "soporte-preparacion",
          title: "Preparación del soporte",
          subtitle: "Limpio, firme, compatible y con humedad controlada.",
          blocks: [
            ["info", "Antes de aplicar", "Retira polvo, material suelto, grasas y restos incompatibles. Revisa planeidad, juntas, humedad y adherencia del soporte."],
            ["warning", "No cubras fallas", "No uses tarrajeo, enchape o pintura para ocultar una grieta activa, una fuga o concreto deteriorado."],
            ["design", "Compatibilidad", "Morteros, selladores, adhesivos y pinturas deben ser compatibles con el soporte y la exposición."]
          ],
          checks: [
            "El soporte está limpio y firme.",
            "No hay humedad ni fisuras activas ocultas.",
            "Los productos son compatibles con la superficie."
          ]
        },
        {
          id: "alineamiento-juntas",
          title: "Alineamiento, niveles y juntas",
          subtitle: "Revisa antes de que el trabajo avance por todo el ambiente.",
          blocks: [
            ["info", "Muestra inicial", "Aprueba un paño o zona de muestra para revisar color, textura, nivel, alineamiento, juntas y encuentros."],
            ["warning", "No aceptes correcciones tardías", "Un error repetido en toda la vivienda será más costoso de retirar y puede dañar instalaciones o impermeabilización."],
            ["design", "Juntas necesarias", "Respeta juntas de movimiento, cambios de material y separaciones previstas; no las rellenes rígidamente por estética."]
          ],
          checks: [
            "Aprobé una muestra antes de continuar.",
            "Niveles, alineamientos y encuentros son uniformes.",
            "Las juntas previstas se conservaron."
          ]
        },
        {
          id: "recepcion-acabados",
          title: "Recepción por ambientes",
          subtitle: "Registra observaciones antes del pago final.",
          blocks: [
            ["info", "Lista de pendientes", "Revisa puertas, ventanas, pisos, enchapes, pintura, aparatos, griferías y limpieza por ambiente. Anota ubicación y responsable."],
            ["warning", "No cierres sin probar", "Prueba agua, desagüe, electricidad, herrajes y sellos antes de considerar terminada la etapa."],
            ["design", "Entrega documentada", "Conserva garantías, fichas, colores, lotes, repuestos y recomendaciones de mantenimiento."]
          ],
          checks: [
            "Cada ambiente tiene una lista de observaciones.",
            "Instalaciones y herrajes fueron probados.",
            "Recibí garantías y datos de los productos."
          ]
        }
      ]
    },
    ampliaciones: {
      eyebrow: "No improvises sobre lo existente",
      title: "Ampliaciones y remodelaciones",
      intro: "Modificar una vivienda puede cambiar cargas, rigidez, evacuación e instalaciones. Antes de demoler o añadir pisos, identifica cómo fue construida y qué puede soportar.",
      topics: [
        {
          id: "evaluar-existente",
          title: "Conoce la estructura existente",
          subtitle: "Planos, número de pisos, daños y modificaciones previas.",
          blocks: [
            ["info", "Reúne antecedentes", "Busca planos, licencias, fotografías de obra, edad de la vivienda y datos de ampliaciones anteriores."],
            ["warning", "No confíes solo en la apariencia", "Que una casa no tenga grietas visibles no demuestra que soporte otro piso o una nueva carga."],
            ["design", "Evaluación necesaria", "Cimentación, columnas, muros, vigas y losas deben revisarse antes de una ampliación vertical o cambio estructural."]
          ],
          checks: [
            "Reuní planos y antecedentes disponibles.",
            "Registré grietas, corrosión, humedad y modificaciones.",
            "La capacidad existente fue evaluada antes de ampliar."
          ]
        },
        {
          id: "demoliciones-vanos",
          title: "Demoliciones y nuevos vanos",
          subtitle: "Una pared puede formar parte del sistema resistente.",
          blocks: [
            ["info", "Identifica antes", "Confirma si el muro, viga o columna cumple función estructural y qué instalaciones pasan por la zona."],
            ["warning", "Detén el corte", "No retires muros portantes, cortes barras ni abras pases en vigas o columnas sin solución diseñada."],
            ["design", "Secuencia y soporte", "La intervención puede necesitar apuntalamiento, refuerzo y una secuencia específica antes de retirar material."]
          ],
          checks: [
            "La función del elemento fue identificada.",
            "Instalaciones ocultas fueron localizadas.",
            "Existe detalle y secuencia antes de demoler."
          ]
        },
        {
          id: "coordinar-ampliacion",
          title: "Coordina proyecto y permisos",
          subtitle: "La ampliación debe integrarse con toda la vivienda.",
          blocks: [
            ["info", "Proyecto completo", "Coordina arquitectura, estructura, agua, desagüe, electricidad, ventilación, escaleras y evacuación."],
            ["warning", "No construyas por partes inconexas", "Comprar acero o levantar columnas sin definir el conjunto puede generar incompatibilidades y desperdicio."],
            ["design", "Trámite aplicable", "Revisa licencia, propiedad, parámetros urbanos y autorizaciones antes de ejecutar trabajos que las requieran."]
          ],
          checks: [
            "La ampliación está coordinada entre especialidades.",
            "El número final de pisos está definido.",
            "Revisé permisos y condiciones municipales aplicables."
          ]
        }
      ]
    },
    seguridad: {
      eyebrow: "Durante toda la obra",
      title: "Seguridad durante la construcción",
      intro: "Una vivienda pequeña también puede producir caídas, derrumbes, electrocución, golpes y exposición a polvo. La seguridad debe planificarse desde el inicio.",
      topics: [
        {
          id: "caidas-excavaciones",
          title: "Caídas y excavaciones",
          subtitle: "Protege bordes, huecos, escaleras y zonas inestables.",
          blocks: [
            ["info", "Control del área", "Delimita excavaciones, bordes de losa, huecos y zonas de carga. Mantén accesos firmes e iluminados."],
            ["warning", "No improvises altura", "No uses pilas de ladrillos, tablones sueltos o escaleras dañadas como plataforma de trabajo."],
            ["design", "Protección colectiva", "Barandas temporales, plataformas y sostenimientos deben ser estables y adecuados para la tarea."]
          ],
          checks: [
            "Bordes, huecos y excavaciones están delimitados.",
            "Los accesos y plataformas son estables.",
            "No hay materiales acumulados en zonas de caída."
          ]
        },
        {
          id: "electricidad-temporal",
          title: "Electricidad y herramientas",
          subtitle: "La instalación provisional también debe proteger.",
          blocks: [
            ["info", "Revisa antes de usar", "Cables, extensiones, enchufes, herramientas y tableros deben estar íntegros, secos y protegidos del tránsito y agua."],
            ["warning", "Retira de servicio", "No uses cables pelados, empalmes expuestos, herramientas sin guarda o equipos que producen chispas, olor o descarga."],
            ["design", "Protección", "La alimentación temporal debe contar con protecciones adecuadas y puesta a tierra cuando corresponda."]
          ],
          checks: [
            "Cables y herramientas están íntegros.",
            "La energía está protegida de agua y golpes.",
            "Los equipos defectuosos fueron retirados."
          ]
        },
        {
          id: "orden-proteccion-personal",
          title: "Orden y protección personal",
          subtitle: "Reduce tropiezos, cortes, polvo y golpes.",
          blocks: [
            ["info", "Organiza", "Mantén rutas libres, apila materiales de forma estable, retira clavos y residuos, y separa zonas de mezcla, corte y almacenamiento."],
            ["warning", "Protección según tarea", "Casco, calzado, guantes, protección ocular, auditiva y respiratoria deben corresponder al riesgo; no sustituyen una condición insegura."],
            ["design", "Responsabilidad", "Define quién controla accesos, emergencias, primeros auxilios y cierre seguro al terminar la jornada."]
          ],
          checks: [
            "Las rutas están libres y los materiales estables.",
            "Cada tarea tiene protección adecuada.",
            "Existe responsable y procedimiento ante emergencias."
          ]
        }
      ]
    },
    mantenimiento: {
      eyebrow: "Después de construir",
      title: "Recepción, mantenimiento y vida útil",
      intro: "La seguridad no termina con la entrega. Conserva documentos, inspecciona cambios y atiende la causa de los deterioros antes de que avancen.",
      topics: [
        {
          id: "entrega-documentos",
          title: "Entrega y documentación",
          subtitle: "Guarda planos, pruebas, garantías y cambios realizados.",
          blocks: [
            ["info", "Archivo de la vivienda", "Conserva planos finales, fotos antes de tapar, pruebas, fichas, garantías, contactos y ubicación de válvulas, registros y tableros."],
            ["warning", "No pierdas los cambios", "Una perforación, ampliación o nueva carga debe registrarse para futuras intervenciones."],
            ["design", "Base para mantener", "La documentación permite localizar instalaciones y comparar cambios sin destruir acabados."]
          ],
          checks: [
            "Tengo planos y fotos de elementos ocultos.",
            "Guardé pruebas, garantías y fichas técnicas.",
            "Registré modificaciones realizadas durante la obra."
          ]
        },
        {
          id: "inspeccion-periodica",
          title: "Inspección preventiva",
          subtitle: "Observa antes y después de lluvias, sismos y cambios de uso.",
          blocks: [
            ["info", "Qué observar", "Revisa fisuras, deformaciones, humedad, corrosión, desprendimientos, sellos, canaletas, desagües, tableros y equipos."],
            ["warning", "Atiende la causa", "Pintar, resanar o sellar no basta si continúa una fuga, movimiento, sobrecarga o corrosión."],
            ["design", "Prioriza", "Atiende primero condiciones que afectan estructura, electricidad, gas, evacuación o caída de elementos."]
          ],
          checks: [
            "Realizo inspecciones y conservo fotografías comparables.",
            "Corrijo la causa antes de reparar el acabado.",
            "Priorizo riesgos para personas y estructura."
          ]
        },
        {
          id: "despues-evento",
          title: "Después de un evento",
          subtitle: "Sismo, incendio, inundación, impacto o excavación vecina.",
          blocks: [
            ["info", "Primera revisión", "Antes de reocupar o continuar obras, observa inclinaciones, grietas nuevas, deformaciones, desprendimientos, fugas, olor a gas y daños eléctricos."],
            ["warning", "No ingreses", "Si hay daño visible importante, movimiento, olor a gas, partes energizadas o riesgo de caída, limita el acceso y solicita evaluación."],
            ["design", "Registro", "Anota fecha, evento, zonas afectadas y cambios observados. No alteres evidencias salvo acciones necesarias para proteger personas."]
          ],
          checks: [
            "Revisé la vivienda después del evento.",
            "Restringí áreas con señales de peligro.",
            "Registré daños y solicité evaluación cuando corresponde."
          ]
        }
      ]
    }
  });

  const roofModule = modules["vigas-techos"];
  if (roofModule && !roofModule.topics.some((topic) => topic.id === "escaleras")) {
    roofModule.title = "Vigas, escaleras y techos";
    roofModule.topics.push({
      id: "escaleras",
      title: "Escaleras de concreto",
      subtitle: "Geometría, apoyo, garganta y barandas deben estar definidas antes de ejecutar.",
      blocks: [
        ["info", "Revisa en planos", "Confirma ancho, número de pasos, huella, contrapaso, descansos, altura libre, apoyo y barandas antes de armar el acero."],
        ["warning", "No cortes para hacerla entrar", "No cortes vigas, losas, columnas ni acero porque la escalera no coincide con el espacio. Corrige el diseño antes de vaciar."],
        ["design", "Garganta y refuerzo", "El espesor de garganta, acero y anclajes dependen de luz, apoyos, geometría y cargas. No existe un espesor universal válido para todas las escaleras."]
      ],
      checks: [
        "La geometría completa coincide con arquitectura y estructura.",
        "El acero y apoyos siguen el plano.",
        "Las barandas y bordes abiertos tienen solución prevista.",
        "No se cortó estructura para ajustar la escalera."
      ]
    });
  }

  const stageGrid = document.getElementById("stageGrid");
  if (!stageGrid) return;

  const stages = [
    ["antes-construir", "⌂", "Antes de construir", "Terreno, planos, presupuesto y permisos"],
    ["terreno-movimiento", "◩", "Terreno y movimiento de tierras", "Rellenos, laderas, excavaciones y drenaje"],
    ["cimentaciones", "▦", "Bases y cimentaciones", "Zapatas, vigas, acero y concreto"],
    ["columnas-muros", "▥", "Columnas y muros", "Confinamiento, continuidad y uniones"],
    ["vigas-techos", "⌂", "Vigas, escaleras y techos", "Soleras, losas, escaleras y vaciado"],
    ["sanitarias", "≋", "Instalaciones sanitarias", "Agua, desagüe, ventilación y pruebas"],
    ["electricas", "↯", "Instalaciones eléctricas", "Circuitos, protecciones y puesta a tierra"],
    ["impermeabilizacion", "◇", "Impermeabilización y humedad", "Techos, baños, filtraciones y pruebas"],
    ["acabados", "▧", "Acabados", "Soportes, juntas, recepción y calidad"],
    ["ampliaciones", "+", "Ampliaciones y remodelaciones", "Evaluación, demoliciones y coordinación"],
    ["seguridad", "!", "Seguridad durante la obra", "Caídas, excavaciones, electricidad y orden"],
    ["mantenimiento", "↻", "Recepción y mantenimiento", "Entrega, inspecciones y vida útil"]
  ];

  stageGrid.innerHTML = stages.map(([id, icon, title, subtitle]) => `
    <button class="stage-card available" type="button" data-module="${id}">
      <span class="stage-icon">${icon}</span>
      <span><strong>${title}</strong><small>${subtitle}</small></span>
      <span class="status-pill">Disponible</span>
    </button>
  `).join("");

  stageGrid.querySelectorAll("[data-module]").forEach((button) => {
    button.addEventListener("click", () => renderModule(button.dataset.module));
  });
})();

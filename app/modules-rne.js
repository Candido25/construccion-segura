Object.assign(modules, {
  "columnas-muros": {
    eyebrow: "Mínimos prácticos del RNE",
    title: "Columnas y muros",
    intro: "Estas recomendaciones ayudan al propietario a reconocer mínimos normativos antes de continuar. Si los planos exigen dimensiones, refuerzos o resistencias mayores, se debe cumplir lo indicado en los planos.",
    topics: [
      {
        id: "sistema-estructural",
        title: "Primero identifica el sistema",
        subtitle: "No mezcles albañilería confinada, pórticos y muros de concreto por intuición.",
        blocks: [
          ["info", "Regla práctica", "Antes de levantar muros confirma si la vivienda está diseñada con albañilería confinada, pórticos de concreto, muros estructurales u otro sistema. Cada sistema tiene detalles distintos de columnas, vigas, anclajes y continuidad."],
          ["warning", "No permitas esto", "No agregues o elimines columnas, no cambies un muro portante por un tabique y no abras vanos nuevos sin revisar el proyecto estructural."],
          ["design", "El plano manda", "La ubicación, sección, acero y empalmes de columnas y muros deben coincidir con los planos estructurales firmados."]
        ],
        checks: [
          "Sé qué sistema estructural tiene mi vivienda.",
          "Las columnas y muros están ubicados como indican los planos.",
          "No se han eliminado elementos para ganar espacio."
        ]
      },
      {
        id: "muros-portantes",
        title: "Muros portantes",
        subtitle: "Deben continuar hasta la cimentación y trabajar en conjunto.",
        blocks: [
          ["info", "Mínimo RNE", "En albañilería, un muro portante debe tener continuidad vertical hasta la cimentación. Para ser considerado como aporte a la resistencia frente a fuerzas horizontales, su longitud debe ser como mínimo 1,20 m."],
          ["warning", "Cuidado con puertas y ventanas", "Los vanos dividen el muro. Un tramo corto al costado de una puerta o ventana no debe asumirse automáticamente como muro resistente."],
          ["design", "Revisa en planos", "El espesor, tipo de ladrillo o bloque, mortero, ubicación y cantidad de muros resistentes dependen del diseño y de la zona sísmica."]
        ],
        checks: [
          "Los muros portantes continúan verticalmente hasta la cimentación.",
          "Los vanos coinciden con los planos.",
          "No se han hecho rozas profundas o cortes que debiliten el muro."
        ]
      },
      {
        id: "columnas-confinamiento",
        title: "Columnas de confinamiento",
        subtitle: "Mínimos aplicables a viviendas de albañilería confinada.",
        blocks: [
          ["info", "Mínimos RNE", "La columna de confinamiento debe tener un espesor igual al espesor efectivo del muro y un peralte mínimo de 15 cm. El concreto de confinamiento debe alcanzar por lo menos 17,15 MPa, equivalente a 175 kg/cm²."],
          ["info", "Acero y estribos", "La columna debe formar un núcleo confinado con un mínimo de cuatro barras verticales. Los estribos deben ser cerrados y llevar ganchos de 135°. El plano puede exigir barras mayores y estribos más cercanos."],
          ["warning", "Separación entre columnas", "Como condición general de albañilería confinada, la distancia entre ejes de columnas no debe superar 5 m ni dos veces la distancia entre elementos horizontales de refuerzo. No uses este límite para separar columnas sin revisar los planos."],
          ["design", "El plano puede exigir más", "La sección, diámetros, anclajes, empalmes y distribución de estribos se definen por cálculo. Estos valores son mínimos de referencia, no una receta de diseño."]
        ],
        checks: [
          "La columna tiene al menos el espesor del muro y no menos de 15 cm de peralte.",
          "El concreto especificado no es menor de 175 kg/cm².",
          "Los estribos están cerrados con ganchos de 135°.",
          "La cantidad y diámetro de barras coinciden con el plano."
        ]
      },
      {
        id: "union-muro-columna",
        title: "Unión entre muro y columna",
        subtitle: "La conexión debe quedar limpia y preparada para trabajar junta.",
        blocks: [
          ["info", "Conexión dentada", "Cuando se use una conexión dentada, la parte saliente del ladrillo no debe exceder 5 cm y debe quedar limpia de mortero suelto antes de vaciar la columna."],
          ["info", "Secuencia correcta", "En albañilería confinada, primero se construye el muro y luego se vacía la columna. El concreto de la columna debe iniciar desde el borde superior del cimiento, no desde el sobrecimiento."],
          ["warning", "No ocultes suciedad", "Retira polvo, restos de mortero y material suelto. Una unión sucia o con vacíos no se corrige cubriéndola con tarrajeo."]
        ],
        checks: [
          "La conexión muro-columna coincide con el detalle del plano.",
          "Los dientes no sobresalen más de 5 cm.",
          "La zona está limpia antes del encofrado y vaciado."
        ]
      },
      {
        id: "tuberias-en-muros",
        title: "Tuberías y cajas empotradas",
        subtitle: "Las instalaciones no deben debilitar columnas ni muros portantes.",
        blocks: [
          ["info", "Coordina antes", "Define tuberías, cajas eléctricas y ductos antes de levantar el muro. Las montantes deben ir por ductos previstos cuando sea necesario."],
          ["warning", "No piques estructura", "No cortes barras, estribos, columnas, vigas o muros portantes para hacer pasar instalaciones. Si existe una interferencia, detén el trabajo y revisa los planos."],
          ["design", "Depende del proyecto", "La ubicación y profundidad de rozas debe coordinarse con arquitectura, estructuras e instalaciones."]
        ],
        checks: [
          "Las instalaciones fueron coordinadas antes de tarrajear.",
          "No se cortó acero ni se picaron columnas o vigas.",
          "Las cajas y tuberías no atraviesan elementos estructurales sin detalle aprobado."
        ]
      }
    ]
  },

  "vigas-techos": {
    eyebrow: "Antes de encofrar y vaciar",
    title: "Vigas y techos",
    intro: "El usuario debe revisar medidas, apoyos, acero, instalaciones y concreto antes de que queden ocultos. Los mínimos dependen del tipo de viga o losa y de la luz entre apoyos.",
    topics: [
      {
        id: "concreto-estructural",
        title: "Concreto de vigas y losas",
        subtitle: "No reemplaces la resistencia indicada por una mezcla aproximada.",
        blocks: [
          ["info", "Mínimo RNE", "La resistencia del concreto estructural no debe ser menor de 17 MPa, aproximadamente 175 kg/cm². Si el plano especifica 210, 245 kg/cm² u otra resistencia mayor, se debe cumplir el plano."],
          ["warning", "No agregues agua", "No añadas agua para hacer más fluida la mezcla ni piedra grande para hacerla rendir. Esto cambia la dosificación, produce segregación y puede reducir la resistencia."],
          ["design", "Antes del vaciado", "Confirma volumen, resistencia, vibrado, personal, acceso, protección y curado antes de iniciar."]
        ],
        checks: [
          "La resistencia del concreto coincide con los planos.",
          "Está disponible el equipo de compactación.",
          "No se agregará agua ni materiales no previstos.",
          "El curado está planificado."
        ]
      },
      {
        id: "viga-solera",
        title: "Viga solera en albañilería confinada",
        subtitle: "Debe cerrar y confinar los muros en la parte superior.",
        blocks: [
          ["info", "Mínimo RNE", "El espesor de la viga solera debe ser igual al espesor efectivo del muro. Su peralte mínimo debe ser igual al espesor de la losa de techo."],
          ["warning", "No la interrumpas sin detalle", "Ductos, escaleras, cajas o cambios de nivel no deben cortar la continuidad de la solera sin una solución estructural indicada en planos."],
          ["design", "Acero y anclaje", "El número de barras, estribos, empalmes y anclajes depende del diseño. Comprueba el detalle antes de cerrar el encofrado."]
        ],
        checks: [
          "La solera tiene al menos el espesor del muro.",
          "Su peralte no es menor que el espesor de la losa.",
          "El acero y los anclajes coinciden con el plano.",
          "No existen ductos que interrumpan la viga sin detalle aprobado."
        ]
      },
      {
        id: "vigas-porticos",
        title: "Vigas de pórticos de concreto",
        subtitle: "Aplicable cuando la viga forma parte del sistema sismorresistente.",
        blocks: [
          ["info", "Referencia mínima", "En vigas de determinados pórticos sismorresistentes, la Norma E.060 exige un ancho no menor que la cuarta parte del peralte ni menor de 25 cm, además de refuerzo continuo superior e inferior. El proyectista debe confirmar si esta disposición aplica a tu vivienda."],
          ["warning", "No copies una sección", "Una viga de 20 × 20, 20 × 25 u otra medida repetida por costumbre no necesariamente cumple para la luz, cargas y sistema estructural de tu casa."],
          ["design", "Revisa el detalle", "Comprueba sección, barras superiores e inferiores, estribos, zonas de confinamiento, empalmes y anclajes en los nudos."]
        ],
        checks: [
          "La sección de la viga coincide con el plano.",
          "Las barras superiores e inferiores son continuas donde corresponde.",
          "Los empalmes y estribos están en las zonas indicadas.",
          "No se cortó acero para colocar tuberías."
        ]
      },
      {
        id: "losas-aligeradas",
        title: "Losas aligeradas y nervadas",
        subtitle: "El espesor depende de la luz y de cómo está apoyado el techo.",
        blocks: [
          ["info", "Mínimos geométricos", "En losas nervadas, el ancho de cada nervio no debe ser menor de 10 cm, su altura no debe superar 3,5 veces ese ancho y el espacio libre entre nervios no debe exceder 75 cm."],
          ["info", "Espesor según la luz", "Cuando no se calcula específicamente la deformación, la E.060 relaciona el peralte con la luz: como referencia, luz/16 si está simplemente apoyada, luz/18,5 con un extremo continuo, luz/21 con ambos extremos continuos y luz/8 en voladizo."],
          ["warning", "No retires puntales antes de tiempo", "El desencofrado y desapuntalamiento deben responder a la resistencia alcanzada por el concreto, la luz y la secuencia de obra. No se decide solo por número de días."],
          ["design", "El plano puede exigir más", "Cargas, tabiques, tanque elevado, voladizos y futuras ampliaciones pueden exigir mayor espesor, vigas adicionales o refuerzo especial."]
        ],
        checks: [
          "El ancho y separación de nervios cumplen el plano y los mínimos aplicables.",
          "El espesor del techo corresponde a su luz y apoyos.",
          "Los ladrillos de techo están íntegros y correctamente apoyados.",
          "La secuencia de desencofrado está definida."
        ]
      },
      {
        id: "acero-temperatura",
        title: "Acero por temperatura y distribución",
        subtitle: "Ayuda a controlar fisuras y distribuir esfuerzos.",
        blocks: [
          ["info", "Separación máxima", "En losas, el espaciamiento del refuerzo principal y del acero por retracción y temperatura no debe exceder tres veces el espesor de la losa ni 40 cm. En losas nervadas con bloques de relleno, el acero perpendicular a los nervios puede llegar hasta cinco veces el espesor, sin superar 40 cm."],
          ["warning", "No lo omitas", "Que el ladrillo de techo ocupe gran parte del paño no significa que pueda eliminarse el acero de temperatura o distribución indicado en planos."],
          ["design", "Cantidad de acero", "El diámetro, área y posición exactos deben provenir del diseño estructural."]
        ],
        checks: [
          "El acero de temperatura está colocado antes del vaciado.",
          "La separación no supera el límite indicado en el plano y la norma.",
          "El acero está amarrado y no se desplazará durante el vaciado."
        ]
      }
    ]
  },

  instalaciones: {
    eyebrow: "Sanitarias y eléctricas",
    title: "Instalaciones de la vivienda",
    intro: "Las instalaciones deben planificarse antes de vaciar o tarrajear. La norma exige cálculos, planos, registros, ventilación y sistemas de protección; no basta con que una tubería o cable simplemente 'funcione'.",
    topics: [
      {
        id: "desague-pendiente",
        title: "Desagüe: diámetro y pendiente",
        subtitle: "Una pendiente uniforme evita atoros y acumulaciones.",
        blocks: [
          ["info", "Mínimos RNE", "La tubería que recibe la descarga de un inodoro debe tener como mínimo 100 mm (4 pulgadas). Los colectores y ramales deben mantener una pendiente uniforme no menor de 1% para diámetros de 100 mm o mayores, y no menor de 1,5% para diámetros de 75 mm o menores."],
          ["warning", "No hagas contras pendientes", "Un tramo que sube, se hunde o cambia de pendiente puede retener sólidos y generar atoros. No corrijas una mala pendiente reduciendo el diámetro."],
          ["design", "Empalmes", "Los ramales deben conectarse a colectores con un ángulo no mayor de 45°, salvo que la unión se realice dentro de una caja de registro o buzón."]
        ],
        checks: [
          "El desagüe del inodoro es de al menos 4 pulgadas.",
          "La pendiente es uniforme en todo el tramo.",
          "Los empalmes no forman ángulos bruscos.",
          "La tubería no atraviesa vigas o columnas sin detalle aprobado."
        ]
      },
      {
        id: "registros-desague",
        title: "Registros y cajas de inspección",
        subtitle: "Todo sistema debe poder limpiarse y mantenerse.",
        blocks: [
          ["info", "Dónde colocar registros", "Se requieren al comienzo de cada ramal horizontal, cada 15 m como máximo, al pie de cada montante —salvo que descargue a una caja ubicada a no más de 10 m— y cada dos cambios de dirección."],
          ["info", "Red exterior", "Las cajas de registro deben colocarse en cambios de dirección, pendiente, material o diámetro, y también cada 15 m como máximo en tramos rectos."],
          ["warning", "Deben quedar accesibles", "No entierres ni tapes registros con pisos, muebles fijos o acabados. Un registro oculto no cumple su función de mantenimiento."]
        ],
        checks: [
          "Hay registros en los puntos de limpieza necesarios.",
          "Las cajas exteriores quedan accesibles.",
          "No hay más de 15 m de tramo sin punto de registro."
        ]
      },
      {
        id: "ventilacion-sanitaria",
        title: "Ventilación sanitaria",
        subtitle: "Evita malos olores, pérdida de sellos de agua y fallas de descarga.",
        blocks: [
          ["info", "Mínimo RNE", "La ventilación individual debe tener un diámetro igual a la mitad del desagüe al que sirve y nunca menor de 50 mm (2 pulgadas). La tubería principal debe subir al exterior sin reducir su diámetro."],
          ["info", "Distancia al sello", "La distancia máxima entre el sello de agua y su ventilación es 1,10 m para desagüe de 40 mm, 1,50 m para 50 mm, 1,80 m para 75 mm y 3,00 m para 100 mm."],
          ["warning", "No reemplaces todo con una válvula", "Aunque se usen válvulas de admisión de aire, la edificación debe conservar por lo menos una ventilación primaria directa al exterior."]
        ],
        checks: [
          "Los aparatos sanitarios tienen ventilación prevista.",
          "La tubería de ventilación no es menor de 2 pulgadas cuando corresponde.",
          "Existe al menos una ventilación primaria al exterior.",
          "La salida del techo está protegida contra filtraciones."
        ]
      },
      {
        id: "agua-potable",
        title: "Agua potable y desagüe",
        subtitle: "Deben mantenerse separados y accesibles para mantenimiento.",
        blocks: [
          ["info", "Separación mínima", "Las tuberías enterradas de agua potable deben separarse por lo menos 50 cm horizontalmente del desagüe y colocarse al menos 15 cm por encima. Cuando se crucen, el agua potable siempre debe pasar por encima con una separación vertical mínima de 15 cm."],
          ["info", "Ductos", "Si una montante de agua comparte ducto con una montante de desagüe o lluvia, debe existir una separación mínima de 20 cm entre sus caras exteriores."],
          ["warning", "No comprometas la estructura", "Las tuberías deben ubicarse sin cortar o reducir la resistencia de columnas, vigas, losas o muros estructurales."]
        ],
        checks: [
          "El agua potable está separada y por encima del desagüe.",
          "Las montantes están en ductos accesibles.",
          "No existen uniones ocultas imposibles de revisar.",
          "Las tuberías no debilitan elementos estructurales."
        ]
      },
      {
        id: "instalacion-electrica",
        title: "Instalación eléctrica segura",
        subtitle: "Debe contar con circuitos, tablero y protecciones definidos en proyecto.",
        blocks: [
          ["info", "Qué exige el proyecto", "La instalación debe mostrar acometida, tablero general, tableros de distribución, alimentadores, circuitos de alumbrado, tomacorrientes, fuerza, cargas especiales y cuadro de cargas."],
          ["info", "Protecciones", "El proyecto debe considerar puesta a tierra y protección contra sobrecorrientes y sobretensiones. Los calibres de conductores y protecciones se determinan según la carga y el Código Nacional de Electricidad, no por costumbre."],
          ["warning", "No mezcles circuitos", "Evita alimentar cocina, ducha eléctrica, bomba, lavadora u otras cargas importantes desde un circuito improvisado de alumbrado o tomacorrientes comunes."],
          ["design", "Construcción por etapas", "Si la vivienda crecerá después, el proyecto debe prever circuitos de reserva, canalizaciones y capacidad futura en el tablero."]
        ],
        checks: [
          "Existe plano eléctrico y cuadro de cargas.",
          "El tablero identifica cada circuito.",
          "La vivienda cuenta con sistema de puesta a tierra.",
          "Las cargas especiales tienen circuitos y protecciones definidos.",
          "No hay empalmes improvisados ocultos dentro de muros o techos."
        ]
      }
    ]
  }
});

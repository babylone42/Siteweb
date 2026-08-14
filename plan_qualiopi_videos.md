# Plan de Trabajo - Actualizaciones Qualiopi y Formación Vídeo IA Pro

Este documento detalla las tareas específicas para el agente de desarrollo web y contenidos para actualizar el sitio web y crear los recursos de calidad exigidos.

---

## 🌐 1. Actualización del Sitio Web (Siteweb)

### index.html
- Habilitar el enlace del curso "Vidéo IA Pro" en el menú de navegación (quitar la clase `link-disabled` y redirigir a `formation-video-ia-pro.html`).
- Activar la tarjeta de formación de vídeo en el carrusel de soluciones (quitar `card-disabled` y añadir el enlace).
- Activar el enlace de pie de página correspondiente.

### images/qualiopi_logo.svg
- Crear un logotipo de Qualiopi conforme a la carta gráfica sobre un fondo blanco sólido.
- El logotipo debe incluir la mención oficial y no debe modificarse su escala de colores ni transparencia.

### update_qualiopi.py
- Actualizar el banner HTML de information legal en el script para cambiar *"Démarche de certification Qualiopi en cours"* por *"Organisme certifié Qualiopi pour la catégorie d'actions : ACTIONS DE FORMATION."*.
- Incluir la imagen del logotipo `qualiopi_logo.svg` en este banner.
- Ejecutar el script `python update_qualiopi.py` para propagar el nuevo banner a todas las páginas de formación registradas.

### sync_layout.js
- Una vez modificado `index.html` con la barra de navegación y el pie de página activos para Vídeo IA, ejecutar `node sync_layout.js` para propagar estos cambios de forma homogénea a todos los archivos HTML del sitio web.

---

## ✉️ 2. Firma de Correo Electrónico Profesional
- Crear un archivo `Qualiopi/8. Signaure/firma_email_qualiopi.html` con una firma HTML profesional para Eulalio Torres.
- Debe incluir el logotipo de Babylone 42, enlaces al sitio web, redes sociales y, en la parte inferior, el logotipo de Qualiopi junto con la mención de certificación obligatoria:
  *« La certification qualité a été délivrée au titre de la catégorie d'action suivante : ACTIONS DE FORMATION. »*

---

## 🎓 3. Guía de Aprendizaje de ElevenLabs
- Crear `Elevenlabs/guide_apprentissage.md` detallando la ruta para aprender a usar ElevenLabs (Text-to-Speech, Voice Cloning, Audio Dubbing, AI Voice Agents).
- Incluir información sobre cursos externos con certificación (como Codecademy o Elevify) y enlaces útiles.

---

## 📋 4. Materiales y Evaluaciones de Vídeo IA Pro (Normativa Qualiopi)

### Escenario Pedagógico Detallado
- Crear `Qualiopi/2. Avant formation/Programme detaille/Scenario_Pedagogique_Detaille_VIDEOIA.md` (3 días / 21 horas).
- Definir objetivos operativos **O1-O5** (Guionización, Avatares, B-Roll, Edición IA, Ética).

### Diapositivas
- Crear `Qualiopi/2. Avant formation/Programme detaille/Contenu_Detaille_Diapositives_VIDEOIA.md` detallando las diapositivas de soporte.

### Cuestionario de Positionamiento
- Crear `Qualiopi/2. Avant formation/Positionnement et prerequis/Questionnaire_Positionnement_VIDEOIA.md` para verificar requisitos antes del inicio de la formación.

### Prueba Práctica Final
- Crear `Qualiopi/4. Apres formation/Evaluation acquis/Epreuve_Pratique_Type_VIDEOIA.md` detallando la prueba final (proyecto de vídeo de 30-60 segundos con IA) y la rúbrica de evaluación.

import streamlit as st
import random

# Preguntas y respuestas almacenadas directamente en el código
preguntas = [
     ("¿Qué es la pedagogía?", 
     ["Es la disciplina que estudia la filosofía de la educación.",
      "Es la disciplina que estudia la educación y los métodos de enseñanza.",
      "Es la disciplina que se ocupa de las políticas educativas.",
      "Es la ciencia que estudia el comportamiento de los estudiantes."], 1),
     
    ("¿Quién es considerado el padre de la pedagogía moderna?", 
     ["Juan Amos Comenio.", "Paulo Freire.", "Lev Vygotsky.", "Jean Piaget."], 0),
     
    ("¿Qué método de enseñanza se basa en la exploración y el descubrimiento guiado?", 
     ["El aprendizaje por descubrimiento de Jerome Bruner.", "El método de enseñanza directa.",
      "El aprendizaje cooperativo.", "El método Montessori."], 0),
     
    ("¿Qué es el aprendizaje significativo según David Ausubel?", 
     ["Es el aprendizaje que se basa en la memorización.",
      "Es aquel en el que el estudiante relaciona nuevos conocimientos con los que ya posee.",
      "Es el aprendizaje que ocurre solo a través de la práctica.",
      "Es el aprendizaje que se realiza en entornos virtuales."], 1),
     
    ("¿Cuál es el principal objetivo de la educación según la UNESCO?", 
     ["Garantizar el acceso a la educación básica.",
      "Garantizar el acceso a una educación de calidad, inclusiva y equitativa para todos.",
      "Proveer formación para trabajos específicos.",
      "Enseñar a los estudiantes sobre el patrimonio cultural."], 1),
     
    ("¿Qué tipo de aprendizaje fomenta la teoría de Jean Piaget?", 
     ["Aprendizaje por descubrimiento.",
      "Aprendizaje colaborativo.",
      "Aprendizaje constructivista basado en el desarrollo cognitivo del niño.",
      "Aprendizaje basado en competencias."], 2),
     
    ("¿Qué es la educación inclusiva?", 
     ["Es un modelo educativo que se centra solo en los estudiantes con discapacidad.",
      "Es un modelo educativo que busca garantizar el aprendizaje de todos los estudiantes, sin exclusión.",
      "Es un enfoque que solo acepta a estudiantes con altos logros académicos.",
      "Es una metodología educativa para estudiantes adultos."], 1),
     
    ("¿Cuál es la diferencia entre enseñanza y aprendizaje?", 
     ["La enseñanza es el proceso de transmitir conocimientos, mientras que el aprendizaje es la adquisición de los mismos.",
      "La enseñanza es la actividad realizada por los alumnos, mientras que el aprendizaje es el proceso que llevan a cabo los maestros.",
      "La enseñanza es más importante que el aprendizaje.",
      "No hay diferencia entre enseñanza y aprendizaje."], 0),

    ("¿Cuál?", 
     ["La enseñanza es el proceso de transmitir conocimientos, mientras qrendizaje es la adquisición de los mismos.",
      "La enseñanza es la actividad realizada por los alumnos,  el aprendizaje es el proceso que llevan a cabo los maestros.",
      "La enseñanza es más importante rendizaje.",
      "No hay diferencia entre enseñanzaprendizaje."], 3)
]

# Lista de planteles
planteles = ["Plantel Iztapalapa", "Plantel Netzahualcóyotl", "Plantel Guillermo Prieto", "Plantel Manuel Cañas"]

# Inicializar el estado de la sesión
if 'preguntas_restantes' not in st.session_state:
    st.session_state.preguntas_restantes = list(range(len(preguntas)))
if 'puntajes' not in st.session_state:
    st.session_state.puntajes = {plantel: 0 for plantel in planteles}
if 'mostrar_respuesta' not in st.session_state:
    st.session_state.mostrar_respuesta = False
if 'opcion_seleccionada' not in st.session_state:
    st.session_state.opcion_seleccionada = None
if 'plantel_seleccionado' not in st.session_state:
    st.session_state.plantel_seleccionado = None
if 'pregunta_actual' not in st.session_state and st.session_state.preguntas_restantes:
    st.session_state.pregunta_actual = st.session_state.preguntas_restantes.pop(0)

# Verificar si quedan preguntas
if not st.session_state.preguntas_restantes and not st.session_state.mostrar_respuesta:
    st.title("Trivia Pedagógica")
    st.write("¡La trivia ha terminado!")
    
    # Determinar el plantel ganador
    plantel_ganador = max(st.session_state.puntajes, key=st.session_state.puntajes.get)
    max_puntos = st.session_state.puntajes[plantel_ganador]
    
    st.markdown(f"""
        <div style="border: 2px solid #4CAF50; padding: 20px; border-radius: 10px; text-align: center; background-color: #F0FFF0; color: #2E7D32; font-size: 24px; font-weight: bold;">
            🏆 ¡Felicidades, {plantel_ganador}! 🏆<br>
            Han ganado la trivia con {max_puntos} puntos.
        </div>
    """, unsafe_allow_html=True)
else:
    pregunta, opciones, respuesta_correcta = preguntas[st.session_state.pregunta_actual]
    st.title("Trivia Pedagógica")
    
    # Mostrar el número de la pregunta en texto pequeño antes de la pregunta
    st.markdown(f"""
        <div style="font-size: 14px; text-align: left; color: #757575;">
            Pregunta {len(preguntas) - len(st.session_state.preguntas_restantes)}/{len(preguntas)}
        </div>
        <div style="text-align: center; font-size: 35px; font-weight: bold; padding: 10px; border: 2px solid #1976D2; background-color: #E3F2FD; border-radius: 10px; color: #0D47A1;">
            {pregunta}
        </div>
    """, unsafe_allow_html=True)

    # Seleccionar plantel
    st.session_state.plantel_seleccionado = st.selectbox("Selecciona el plantel que responde:", planteles)

    # Crear botones de opción múltiple
    opcion_seleccionada = st.radio("Selecciona una respuesta:", opciones, index=None)

    # Botón para validar la respuesta
    if st.button("Responder"):
        if opcion_seleccionada is not None and st.session_state.plantel_seleccionado:
            st.session_state.mostrar_respuesta = True
            st.session_state.opcion_seleccionada = opciones.index(opcion_seleccionada)
            if st.session_state.opcion_seleccionada == respuesta_correcta:
                st.success("¡Correcto! 🎉")
                st.session_state.puntajes[st.session_state.plantel_seleccionado] += 1
            else:
                st.error(f"Incorrecto. La respuesta correcta es: {opciones[respuesta_correcta]}")

    # Botón para siguiente pregunta
    if st.session_state.mostrar_respuesta:
        if st.button("Siguiente pregunta"):
            if st.session_state.preguntas_restantes:
                st.session_state.pregunta_actual = st.session_state.preguntas_restantes.pop(0)
                st.session_state.mostrar_respuesta = False
                st.session_state.opcion_seleccionada = None
                st.session_state.plantel_seleccionado = None
                st.rerun()
            else:
                st.session_state.mostrar_respuesta = False
                st.rerun()

# Mostrar puntajes
st.sidebar.header("Puntajes por Plantel")
for plantel, puntaje in st.session_state.puntajes.items():
    st.sidebar.write(f"{plantel}: {puntaje} puntos")

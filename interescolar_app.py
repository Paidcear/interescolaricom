import streamlit as st
import time
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
      "El aprendizaje cooperativo.", "El método Montessori."], 0)
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
if 'pantalla_seleccionada' not in st.session_state:
    st.session_state.pantalla_seleccionada = "Panel Principal"
if 'cronometro_iniciado' not in st.session_state:
    st.session_state.cronometro_iniciado = False

# Función para reiniciar el temporizador
def reiniciar_temporizador():
    st.session_state.tiempo_inicio = time.time()

# Panel lateral con lista desplegable para elegir pantalla
st.sidebar.title("Menú Principal")
pantalla_anterior = st.session_state.pantalla_seleccionada
st.session_state.pantalla_seleccionada = st.sidebar.selectbox(
    "Selecciona una pantalla:",
    ["Panel Principal", "Trivia Pedagógica"]
)

# Si se cambia a la pantalla de trivia, iniciar cronómetro
if pantalla_anterior != "Trivia Pedagógica" and st.session_state.pantalla_seleccionada == "Trivia Pedagógica":
    if st.session_state.preguntas_restantes:
        st.session_state.pregunta_actual = st.session_state.preguntas_restantes.pop(0)
    st.session_state.mostrar_respuesta = False
    st.session_state.cronometro_iniciado = True
    reiniciar_temporizador()

# Pantalla de bienvenida
if st.session_state.pantalla_seleccionada == "Panel Principal":
    st.title("Bienvenido a la Trivia Pedagógica 🎓")
    
    st.markdown("""
    <div style="text-align: center; font-size: 24px; padding: 20px; border: 2px solid #1976D2; background-color: #E3F2FD; border-radius: 10px; color: #0D47A1;">
        💡 Pon a prueba tus conocimientos en pedagogía.<br>
        Selecciona "Trivia Pedagógica" en el menú lateral para comenzar.
    </div>
    """, unsafe_allow_html=True)
    
    st.image("https://www.uclm.es/-/media/Images/C01-Centros/Fac-Educacion-Albacete/Noticias/2021/trivia.ashx", use_container_width=True)

# Pantalla de trivia pedagógica
elif st.session_state.pantalla_seleccionada == "Trivia Pedagógica":
    if not st.session_state.preguntas_restantes and not st.session_state.mostrar_respuesta:
        st.title("Trivia Pedagógica")
        st.write("¡La trivia ha terminado!")

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

        st.markdown(f"""
            <div style="text-align: center; font-size: 35px; font-weight: bold; padding: 10px; border: 2px solid #1976D2; background-color: #E3F2FD; border-radius: 10px; color: #0D47A1;">
                {pregunta}
            </div>
        """, unsafe_allow_html=True)

        # Mostrar el temporizador en el panel lateral solo si la trivia ha comenzado
        if st.session_state.cronometro_iniciado:
            tiempo_restante = max(0, 15 - int(time.time() - st.session_state.tiempo_inicio))
            st.sidebar.header("⏳ Tiempo restante:")
            st.sidebar.write(f"**{tiempo_restante} segundos**")

        st.session_state.plantel_seleccionado = st.selectbox("Selecciona el plantel que responde:", planteles)

        opcion_seleccionada = st.radio("Selecciona una respuesta:", opciones, index=None)

        if tiempo_restante == 0 and not st.session_state.mostrar_respuesta:
            st.session_state.mostrar_respuesta = True
            st.session_state.opcion_seleccionada = None
            st.warning(f"⏳ ¡Tiempo agotado! La respuesta correcta es: {opciones[respuesta_correcta]}")

        if st.button("Responder") and not st.session_state.mostrar_respuesta:
            if opcion_seleccionada is not None and st.session_state.plantel_seleccionado:
                st.session_state.mostrar_respuesta = True
                st.session_state.opcion_seleccionada = opciones.index(opcion_seleccionada)
                if st.session_state.opcion_seleccionada == respuesta_correcta:
                    st.success("¡Correcto! 🎉")
                    st.session_state.puntajes[st.session_state.plantel_seleccionado] += 1
                else:
                    st.error(f"Incorrecto. La respuesta correcta es: {opciones[respuesta_correcta]}")

        if st.session_state.mostrar_respuesta:
            if st.button("Siguiente pregunta"):
                if st.session_state.preguntas_restantes:
                    st.session_state.pregunta_actual = st.session_state.preguntas_restantes.pop(0)
                    st.session_state.mostrar_respuesta = False
                    st.session_state.opcion_seleccionada = None
                    st.session_state.plantel_seleccionado = None
                    reiniciar_temporizador()
                    st.rerun()
                else:
                    st.session_state.mostrar_respuesta = False
                    st.rerun()

    st.sidebar.header("Puntajes por Plantel")
    for plantel, puntaje in st.session_state.puntajes.items():
        st.sidebar.write(f"{plantel}: {puntaje} puntos")

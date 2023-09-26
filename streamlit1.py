import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
#import os
#import tempfile

st.title('Pronósticos :chart_with_upwards_trend:')

st.set_option('deprecation.showPyplotGlobalUse', False)

#desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

data_file = st.file_uploader("Upload XLSX", type=["XLSX"])

# Variable para almacenar los datos originales
datos_originales = None

if data_file is not None:
    datos = pd.read_excel(data_file, dtype={'Año natural/Semana': str, 'Material': str, 'Año natural/Mes': str})
    datos['Año natural/Semana'] = datos['Año natural/Semana'].apply(str)
    datos['Año natural/Mes'] = datos['Año natural/Mes'].apply(str)

    # Realiza un seguimiento de los datos originales
    datos_originales = datos.copy()

    materiales = datos['Material'].drop_duplicates().tolist()
    centros = datos['Centro'].drop_duplicates().tolist()
    sel_mat = st.selectbox('Material', materiales)
    sel_ce = st.selectbox('Centro', centros)

    sns.set(style="darkgrid", palette="pastel", rc={'figure.figsize': (12, 8)})

    if 'edited_df' not in st.session_state:
        st.session_state['edited_df'] = datos.copy()

    def update_graph():
        edited_df = st.session_state['edited_df']

        # Filtra los datos según las selecciones de Material y Centro
        filtered_df = edited_df[(edited_df['Material'] == sel_mat) & (edited_df['Centro'] == sel_ce)]

        # Crear gráfico con plotly
        fig = px.line(filtered_df, x='Año natural/Semana', y='Ajuste Plan final Línea', color='tipo_dato',
                      markers=True, title=f'Pronósticos para {sel_mat} en {sel_ce}')

        # Muestra los valores al pasar el cursor sobre los puntos
        fig.update_traces(mode='lines+markers', text=filtered_df['Ajuste Plan final Línea'])
        fig.update_traces(marker=dict(size=10))

        # Actualiza el formato de las etiquetas de datos
        fig.update_traces(hovertemplate='%{y:.2f}')

        st.plotly_chart(fig)

    update_graph()

    edit_df = st.data_editor(data=datos[(datos['Material'] == sel_mat) & (datos['Centro'] == sel_ce)],
                             disabled=['Año natural/Semana', 'Mes', 'Año natural/Mes', 'Material', 'DescMat', 'Centro',
                                       'DescCe', 'tipo_dato'],
                             hide_index=True, width=1080, height=400)

    col1, col2, col3 = st.columns(3)

    if 'edited_df' not in st.session_state:
        st.session_state['edited_df'] = datos.copy()

    with col1:
        if st.button("Guardar cambios :floppy_disk:"):
            st.session_state['edited_df'].update(edit_df, overwrite=True)
            update_graph()
            st.text("Cambios guardados🎈")
'''
    with col2:
        if st.button('Descargar cambios :printer:'):
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file_path = temp_file.name
                st.session_state['edited_df'].to_excel(temp_file_path, index=False)

            st.markdown(
                f'<a href="{temp_file_path}" download="Pronosticos.xlsx">Descargar Pronosticos.xlsx</a>',
                unsafe_allow_html=True
            )

            st.text("Descargado🎈")

    with col3:
        if st.button('Borrar cambios :wastebasket:'):
            st.session_state['edited_df'] = datos.copy()
            st.text("Cambios borrados")
'''

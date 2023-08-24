import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import mplcursors 
st.title('Pronósticos :chart_with_upwards_trend:')

#traemos los datos
st.set_option('deprecation.showPyplotGlobalUse', False) #para evitar el warning alert

data_file = st.file_uploader("Upload XLSX", type=["XLSX"])



if data_file is not None:
    
  
  datos=pd.read_excel(r'Planes.xlsx',dtype={'Año natural/Semana':str,'Material':str,'Año natural/Mes':str})
  datos['Año natural/Semana']=datos['Año natural/Semana'].apply(str)
  datos['Año natural/Mes']=datos['Año natural/Mes'].apply(str)
  materiales=datos['Material'].drop_duplicates().tolist() #creamos lista de materiales
  centros=datos['Centro'].drop_duplicates().tolist()
  sel_mat=st.selectbox('Material', materiales)#datos['Material'].drop_duplicates) seleccionar material
  sel_ce=st.selectbox('Centro',centros) #seleccionar centro
  
  sns.set(style="darkgrid",palette="pastel",rc={'figure.figsize':(12,8)})
  
  sns.lineplot(data=datos[(datos['Material']==sel_mat) & (datos['Centro']==sel_ce)],x='Año natural/Semana',y='Ajuste Plan final Línea',hue=datos['tipo_dato'],sort=True,style=datos['tipo_dato'],errorbar=None,palette=['purple','blue'], markers=True,)
  sns.axes_style({'ytick.direction': 'in'})
  fig=sns.mpl.pyplot.show()
  st.pyplot()
  
  cursor = mplcursors.cursor(fig, hover=True)
  cursor.connect("add", lambda sel: st.write(f'({sel.target[0]:.2f}, {sel.target[1]:.2f})'))
  
  edit_df=st.data_editor(data=datos[(datos['Material']==sel_mat) & (datos['Centro']==sel_ce)],disabled=['Año natural/Semana','Mes','Año natural/Mes','Material','DescMat','Centro','DescCe','tipo_dato']
                         ,hide_index=True,width=1080, height=400)
  
  col1, col2, col3 = st.columns(3)
  
  if 'edited_df' not in st.session_state:
      st.session_state['edited_df']=datos.copy()
  
  with col1:
      if st.button("Guardar cambios :floppy_disk:"): 
          #edited_df=edit_df.copy()
          st.session_state['edited_df'].update(edit_df,overwrite=True)
          st.text("Cambios guardados🎈")
  
  #st.write("Contenido de edited_df:")
  #st.write(edited_df)  # Imprime el contenido de edited_df
  
  with col2:
      if st.button('Descargar cambios :printer:'):
          #datos.update(edit_df,overwrite=True)
          st.session_state['edited_df'].to_excel('Pronosticos.xlsx', index=False) #exporta el original con los cambios
          del st.session_state['edited_df']
          st.text("Descargado🎈")

  with col3:
    if st.button('Borrar cambios :wastebasket:'):
        st.session_state['edited_df']=datos.copy()
        st.text("Cambios borrados")

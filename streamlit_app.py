import streamlit as st
import pandas as pd
import os
import datetime
import base64

def process_file(uploaded_file, filename):
    df = pd.read_excel(uploaded_file)
    #drop rows with DIRECCION empty
    df.dropna(subset=['DIRECCION'], inplace=True)
    

    # Check if the columns have the expected names
    try:
        assert 'CIS' in df.columns
        assert 'IDENTIFICACION' in df.columns
        assert 'DIRECCION' in df.columns
        assert 'COMUNA' in df.columns
        assert 'BARRIO' in df.columns
    except AssertionError:
        st.error("The Excel file is not in the correct format.")
        return

    # Rest of your processing here...
    # ...

    # Create a column of DEPARTAMENTO in which all cells are 'ANTIOQUIA'
    df['DEPARTAMENTO'] = 'ANTIOQUIA'
    # Join in a single column the address, the commune and the department
    df['DIRECCION COMPLETA'] = df['DIRECCION'] + ", " + df['COMUNA'] + ", " + df['DEPARTAMENTO']

    ## Treatment of the template
    # Load the Excel file
    plantilla = df[['IDENTIFICACION', 'DIRECCION COMPLETA']].copy()  # Select specific columns and create a copy
    plantilla[['Carga','Hora inicial','Hora final','Tiempo de servicio','Notas', 'Longitud', 'Fecha programada','Tipo de visita']] = ''
    plantilla['Carga'] = 0
    plantilla['Hora inicial'] = '0:01'
    plantilla['Hora final'] = '23:59'
    plantilla['Tiempo de servicio'] = 0.1
    # 'Notas' is a growing integer
    plantilla['Notas'] = range(1, len(plantilla) + 1)

    # Convert DataFrame to CSV for download
    csv = plantilla.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings
    linko= f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download CSV File</a>'
    
    st.markdown(linko, unsafe_allow_html=True)

st.title('Conversor de IPS a plataforma de rutas')

uploaded_file = st.file_uploader("Suba el archivo Excel recibido de la IPS")
# Filename = uploaded_file.name + date

if uploaded_file is not None:
    filename = uploaded_file.name
    #delete extension
    filename = os.path.splitext(filename)[0]
    filename = filename+ datetime.datetime.now().strftime("%Y%m%d")

    process_file(uploaded_file, filename)

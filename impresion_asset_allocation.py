import pandas as pd
import numpy as np 
import streamlit as st
import base64 # Para incrustar imágenes si fuera necesario

# --- 1. Configuración inicial ---

# Opciones de visualización de Pandas (afectan cómo se muestran en la consola/terminal, no directamente en Streamlit)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Reporte Asset Allocation BVC",
    page_icon="📊",
    layout="wide", # Usa todo el ancho de la pantalla
    initial_sidebar_state="collapsed" # El sidebar inicia colapsado
)

# --- 2. Configuración de archivos ---
#file_path = '/Users/matiasgonzalez/Library/CloudStorage/GoogleDrive-mgonzalez@buenavistacapital.com/.shortcut-targets-by-id/1Lbjcks5sDTC17AftNR6mDxW8bwAA7EaA/BVC/Asset Allocation/Comite y asset allocation bvc 2025 (version 1).xlsx'
sheets_names = ["Resumen portafolio", "Renta variable", "Renta_fija", "Alternativos"]

# --- 3. Funciones auxiliares ---

# Función auxiliar para aplicar la multiplicación
def multiply_numeric_cols(df, start_col_index=0):
    # Selecciona solo las columnas numéricas a partir del índice especificado
    numeric_cols = df.select_dtypes(include=np.number).columns
    # Filtra para incluir solo las columnas numéricas que están en el rango deseado
    cols_to_multiply = [col for col in numeric_cols if df.columns.get_loc(col) >= start_col_index]
    df[cols_to_multiply] = df[cols_to_multiply] * 100
    return df

def clean_nan_percent(value):
    # Check if the value is 'nan%' and replace it with an empty string
    if value == "nan%":
        return ""
    return value

# --- 4. Funciones de procesamiento de datos ---
def tabla_resumen_portfolio(temp_df_res1):
    # Check if DataFrame is empty
    if temp_df_res1.empty:
        print("Warning: The DataFrame is empty.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Collect rows in a list
    rows = []
    for i, row in temp_df_res1.iterrows():
        # Ensure columns exist before accessing
        if all(col in row for col in ["Asset class", "AA Relativo", "AA Absoluto", "1 Week", "MTD", "YTD"]):
            rows.append([row["Asset class"], f"{row['AA Relativo']:.2f}%",f"{row['AA Absoluto']:.2f}%", f"{row['1 Week']:.2f}%", f"{row['MTD']:.2f}%", f"{row['YTD']:.2f}%"])
        else:
            print("Error: One or more columns are missing in the DataFrame.")
            return pd.DataFrame()  # Return an empty DataFrame if columns are missing

    # Create a DataFrame from the list
    table = pd.DataFrame(rows, columns=["Asset class", "AA Relativo", "AA Absoluto", "1 Week", "MTD", "YTD"])
    df_cleaned = table.map(clean_nan_percent)  # Clean 'nan%' values
    
    return df_cleaned

# Example function to process DataFrame
def tabla_attribution_portfolio(temp_df_res2):
    # Check if DataFrame is empty
    if temp_df_res2.empty:
        print("Warning: The DataFrame is empty.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Collect rows in a list
    rows = []
    for i, row in temp_df_res2.iterrows():
        # Ensure columns exist before accessing
        if all(col in row for col in ['Tipo', 'Asset Class', 'Benchmark', 'Posición Total Activo', 'AA Absoluto BVC', 'AA Relativo BVC',
                                    'MSCI RV / JPM RF', 'Retorno BVC Período', 'Retorno Benchmark Período', 'Att. Geo', 'Att. Fondos']):
            rows.append([row["Tipo"], row['Asset Class'], row['Benchmark'], f"{row['Posición Total Activo']:.2f}%", f"{row['AA Absoluto BVC']:.2f}%",
                        f"{row['AA Relativo BVC']:.2f}%", f"{row['MSCI RV / JPM RF']:.2f}%", f"{row['Retorno BVC Período']:.2f}%",
                        f"{row['Retorno Benchmark Período']:.2f}%", f"{row['Att. Geo']:.2f}%", f"{row['Att. Fondos']:.2f}%"])
        else:
            print("Error: One or more columns are missing in the DataFrame.")
            return pd.DataFrame()  # Return an empty DataFrame if columns are missing

    # Create a DataFrame from the list
    table = pd.DataFrame(rows, columns=['Tipo', 'Asset Class', 'Benchmark', 'Posición Total Activo', 'AA Absoluto BVC', 'AA Relativo BVC',
                                    'MSCI RV / JPM RF', 'Retorno BVC Período', 'Retorno Benchmark Período', 'Att. Geo', 'Att. Fondos'])
    df_cleaned = table.map(clean_nan_percent)  # Clean 'nan%' values
    
    return df_cleaned

def tablas_asset_allocation(temp_df_rv1, temp_df_rv2, temp_df_rf1, temp_df_rf2, temp_df_al1, temp_df_al2):
    # Check if DataFrame is empty
    if temp_df_rv1.empty:
        print("Warning: The DataFrame 1 is empty.")
        return pd.DataFrame()  # Return an empty DataFrame
    
    if temp_df_rv2.empty:
        print("Warning: The DataFrame 2 is empty.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Collect rows in a list
    rowsrv1 = []
    for i, row in temp_df_rv1.iterrows():
        # Ensure columns exist before accessing
        if all(col in row for col in ['Asset class', 'AA Relativo', 'AA Absoluto', '1 Week', 'MTD', 'YTD']):
            rowsrv1.append([row["Asset class"], f"{row['AA Relativo']:.2f}%", f"{row['AA Absoluto']:.2f}%",
                        f"{row['1 Week']:.2f}%", f"{row['MTD']:.2f}%", f"{row['YTD']:.2f}%"])
        else:
            print("Error: One or more columns are missing in the DataFrame.")
            return pd.DataFrame()  # Return an empty DataFrame if columns are missing

    rowsrv2 = []
    for i, row in temp_df_rv2.iterrows():
        # Ensure columns exist before accessing
        if all(col in row for col in ['Equities', 'AA Relativo', 'AA Absoluto', '1 Week', 'MTD', 'YTD']):
            rowsrv2.append([row["Equities"], f"{row['AA Relativo']:.2f}%", f"{row['AA Absoluto']:.2f}%",
                        f"{row['1 Week']:.2f}%", f"{row['MTD']:.2f}%", f"{row['YTD']:.2f}%"])
        else:
            print("Error: One or more columns are missing in the DataFrame.")
            return pd.DataFrame()  # Return an empty DataFrame if columns are missing
        
    rowsrf1 = []
    for i, row in temp_df_rf1.iterrows():
        # Ensure columns exist before accessing
        if all(col in row for col in ['Asset class', 'AA Relativo', 'AA Absoluto', '1 Week', 'MTD', 'YTD']):
            rowsrf1.append([row["Asset class"], f"{row['AA Relativo']:.2f}%", f"{row['AA Absoluto']:.2f}%",
                        f"{row['1 Week']:.2f}%", f"{row['MTD']:.2f}%", f"{row['YTD']:.2f}%"])
        else:
            print("Error: One or more columns are missing in the DataFrame rf1.")
            return pd.DataFrame()  
    
    rowsrf2 = []
    for i, row in temp_df_rf2.iterrows():
        # Ensure columns exist before accessing
        if all(col in row for col in ['Renta Fija', 'AA Relativo', 'AA Absoluto', '1 Week', 'MTD', 'YTD']):
            rowsrf2.append([row["Renta Fija"], f"{row['AA Relativo']:.2f}%", f"{row['AA Absoluto']:.2f}%",
                        f"{row['1 Week']:.2f}%", f"{row['MTD']:.2f}%", f"{row['YTD']:.2f}%"])
        else:
            print("Error: One or more columns are missing in the DataFrame rf2.")
            return pd.DataFrame()

    rowsal1 = []
    for i, row in temp_df_al1.iterrows():
        # Ensure columns exist before accessing
        if all(col in row for col in ['Asset class', 'AA Relativo', 'AA Absoluto', 'LAST MONTH', 'YTD']):
            rowsal1.append([row["Asset class"], f"{row['AA Relativo']:.2f}%", f"{row['AA Absoluto']:.2f}%",
                         f"{row['LAST MONTH']:.2f}%", f"{row['YTD']:.2f}%"])
        else:
            print("Error: One or more columns are missing in the DataFrame al1.")
            return pd.DataFrame()  
    
    rowsal2 = []
    for i, row in temp_df_al2.iterrows():
        # Ensure columns exist before accessing
        if all(col in row for col in ['Alternativos', 'AA Relativo', 'AA Absoluto', 'LAST MONTH', 'YTD']):
            rowsal2.append([row["Alternativos"], f"{row['AA Relativo']:.2f}%", f"{row['AA Absoluto']:.2f}%",
                         f"{row['LAST MONTH']:.2f}%", f"{row['YTD']:.2f}%"])
        else:
            print("Error: One or more columns are missing in the DataFrame al2.")
            return pd.DataFrame()

    # Create a DataFrame from the list
    table1 = pd.DataFrame(rowsrv1, columns=['Asset class', 'AA Relativo', 'AA Absoluto', '1 Week', 'MTD', 'YTD'])
    df_cleaned1 = table1.map(clean_nan_percent)  
    table2 = pd.DataFrame(rowsrv2, columns=['Equities', 'AA Relativo', 'AA Absoluto', '1 Week', 'MTD', 'YTD'])
    df_cleaned2 = table2.map(clean_nan_percent)
    table3 = pd.DataFrame(rowsrf1, columns=['Asset class', 'AA Relativo', 'AA Absoluto', '1 Week', 'MTD', 'YTD'])
    df_cleaned3 = table3.map(clean_nan_percent)  
    table4 = pd.DataFrame(rowsrf2, columns=['Renta Fija', 'AA Relativo', 'AA Absoluto', '1 Week', 'MTD', 'YTD'])
    df_cleaned4 = table4.map(clean_nan_percent)
    table5 = pd.DataFrame(rowsal1, columns=['Asset class', 'AA Relativo', 'AA Absoluto', 'LAST MONTH', 'YTD'])
    df_cleaned5 = table5.map(clean_nan_percent)  
    table6 = pd.DataFrame(rowsal2, columns=['Alternativos', 'AA Relativo', 'AA Absoluto', 'LAST MONTH', 'YTD'])
    df_cleaned6 = table6.map(clean_nan_percent)

    return df_cleaned1, df_cleaned2, df_cleaned3, df_cleaned4, df_cleaned5, df_cleaned6

# --- 5. Lógica principal de la aplicación Streamlit ---

def main():
    st.title("📊 Reporte de Asset Allocation BVC")
    st.markdown("---") # Línea divisoria

    # 1. AGREGAR EL WIDGET DE CARGA DE ARCHIVOS
    uploaded_file = st.file_uploader(
        "Sube tu archivo Excel de Asset Allocation",
        type=['xlsx'],
        help="El archivo debe contener las hojas: Resumen portafolio, Renta variable, Renta_fija, y Alternativos."
    )
    
    # 2. DETENER LA EJECUCIÓN SI NO HAY ARCHIVO CARGADO
    if uploaded_file is None:
        st.info("⬆️ Por favor, sube el archivo Excel para iniciar el análisis.")
        return # Detiene la ejecución si no hay archivo

    # --- Cargar y procesar datos ---
    data_loaded = False
    temp_df_res1 = pd.DataFrame()
    temp_df_res2 = pd.DataFrame()
    temp_df_rv1 = pd.DataFrame()
    temp_df_rv2 = pd.DataFrame()
    temp_df_rf1 = pd.DataFrame()
    temp_df_rf2 = pd.DataFrame()
    temp_df_al1 = pd.DataFrame()
    temp_df_al2 = pd.DataFrame()

    # La variable file_path ahora será el objeto uploaded_file
    file_to_process = uploaded_file

    try:
        with st.spinner("Cargando y procesando datos del Excel..."):
            for sheet_name in sheets_names:
                if sheet_name == "Resumen portafolio":
                    temp_df_res1 = pd.read_excel(file_to_process, sheet_name=sheet_name, usecols='B:G', nrows=5, skiprows=1)
                    # Necesitas reiniciar el puntero del archivo para cada lectura de hoja si usas el mismo objeto
                    uploaded_file.seek(0)
                    temp_df_res2 = pd.read_excel(file_to_process, sheet_name=sheet_name, usecols='H:S', nrows=22, skiprows=1)
                
                # SIEMPRE REINICIA EL PUNTERO DEL ARCHIVO ANTES DE LEER LA SIGUIENTE HOJA
                uploaded_file.seek(0)
                if sheet_name == "Renta variable":
                    temp_df_rv1 = pd.read_excel(file_to_process, sheet_name=sheet_name, usecols='B:G', nrows=7, skiprows=1)
                    uploaded_file.seek(0)
                    temp_df_rv2 = pd.read_excel(file_to_process, sheet_name=sheet_name, usecols='I:N', nrows=30, skiprows=1)
                
                uploaded_file.seek(0)
                if sheet_name == "Renta_fija":
                    temp_df_rf1 = pd.read_excel(file_to_process, sheet_name=sheet_name, usecols='B:G', nrows=7, skiprows=1)
                    uploaded_file.seek(0)
                    temp_df_rf2 = pd.read_excel(file_to_process, sheet_name=sheet_name, usecols='I:N', nrows=21, skiprows=1)

                uploaded_file.seek(0)
                if sheet_name == "Alternativos":
                    temp_df_al1 = pd.read_excel(file_to_process, sheet_name=sheet_name, usecols='B:F', nrows=5, skiprows=1)
                    uploaded_file.seek(0)
                    temp_df_al2 = pd.read_excel(file_to_process, sheet_name=sheet_name, usecols='I:M', nrows=12, skiprows=1)

            # Renombrar columnas para evitar conflictos
            temp_df_rv2.rename(columns={'Equities': 'Equities', 'AA Relativo.1': 'AA Relativo', 'AA Absoluto.1': 'AA Absoluto', '1 Week.1': '1 Week', 'MTD.1': 'MTD', 'YTD.1': 'YTD'}, inplace=True)
            temp_df_rf2.rename(columns={'Renta Fija': 'Renta Fija', 'AA Relativo.1': 'AA Relativo', 'AA Absoluto.1': 'AA Absoluto', '1 Week.1': '1 Week', 'MTD.1': 'MTD', 'YTD.1': 'YTD'}, inplace=True)
            temp_df_al2.rename(columns={'Alternativos ': 'Alternativos', 'AA Relativo.1': 'AA Relativo', 'AA Absoluto.1': 'AA Absoluto', 'LAST MONTH.1': 'LAST MONTH', 'YTD.1': 'YTD'}, inplace=True)

            # Rellenar hacia adelante los valores de la columna "Tipo" en temp_df_res2
            if 'Tipo' in temp_df_res2.columns:
                temp_df_res2['Tipo'] = temp_df_res2['Tipo'].ffill()
            
            # Aplicar la multiplicación solo a columnas numéricas
            temp_df_res1 = multiply_numeric_cols(temp_df_res1, start_col_index=1)
            temp_df_res2 = multiply_numeric_cols(temp_df_res2, start_col_index=3)
            temp_df_rv1 = multiply_numeric_cols(temp_df_rv1, start_col_index=1)
            temp_df_rv2 = multiply_numeric_cols(temp_df_rv2, start_col_index=1)
            temp_df_rf1 = multiply_numeric_cols(temp_df_rf1, start_col_index=1)
            temp_df_rf2 = multiply_numeric_cols(temp_df_rf2, start_col_index=1)
            temp_df_al1 = multiply_numeric_cols(temp_df_al1, start_col_index=1)
            temp_df_al2 = multiply_numeric_cols(temp_df_al2, start_col_index=1)
            
            data_loaded = True
            st.success("Datos cargados y procesados correctamente.")

    except FileNotFoundError:
        st.error(f"Error: El archivo no se encontró en la ruta: {file_path}")
        data_loaded = False
    except ValueError as e:
        st.error(f"Error al leer el archivo o la hoja: {e}. Por favor, verifica el nombre de las hojas y el formato del archivo.")
        data_loaded = False
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al cargar los datos: {e}")
        data_loaded = False

    if data_loaded:
        # --- Mostrar tablas de Resumen Portafolio ---
        st.header("📈 Resumen del Portafolio")
        col1_res, col2_res = st.columns(2) # Dos columnas para las tablas de resumen

        with col1_res:
            st.subheader("Resumen General")
            df_res1_formatted = tabla_resumen_portfolio(temp_df_res1)
            if not df_res1_formatted.empty:
                st.dataframe(df_res1_formatted, use_container_width=True, hide_index=True)
            else:
                st.info("No hay datos para mostrar en Resumen General.")

        with col2_res:
            st.subheader("Atribución del Portafolio")
            df_res2_formatted = tabla_attribution_portfolio(temp_df_res2)
            if not df_res2_formatted.empty:
                st.dataframe(df_res2_formatted, use_container_width=True, hide_index=True)
            else:
                st.info("No hay datos para mostrar en Atribución del Portafolio.")

        st.markdown("---")

        # --- Mostrar tablas de Renta Variable ---
        st.header("💰 Renta Variable")
        col1_rv, col2_rv = st.columns(2)

        try:
            result = tablas_asset_allocation(temp_df_rv1, temp_df_rv2, temp_df_rf1, temp_df_rf2, temp_df_al1, temp_df_al2)
            if isinstance(result, tuple) and len(result) == 6:
                temp_df_rv1, temp_df_rv2, temp_df_rf1, temp_df_rf2, temp_df_al1, temp_df_al2 = result
            else:
                st.error("Error al procesar las tablas de Asset Allocation. Por favor, revisa los datos.")
                temp_df_rv1 = temp_df_rf2 = temp_df_al1 = temp_df_al2 = temp_df_rf2 = temp_df_rf1 = pd.DataFrame()  # Asignar DataFrames vacíos si hay error
        except Exception as e:
            st.error(f"Error al procesar als tablas de Asset Allocation: {e}")
            temp_df_rv1 = temp_df_rf2 = temp_df_al1 = temp_df_al2 = temp_df_rf2 = temp_df_rf1 = pd.DataFrame()
        
        #temp_df_rv1, temp_df_rv2, temp_df_rf1, temp_df_rf2, temp_df_al1, temp_df_al2 = tablas_asset_allocation(temp_df_rv1,
                                                            #temp_df_rv2, temp_df_rf1, temp_df_rf2, temp_df_al1, temp_df_al2)
        with col1_rv:
            st.subheader("Resumen de Renta Variable")
            # Asumiendo que quieres un formato similar o puedes crear una nueva función para RV1
            # Por ahora, solo mostramos el DF directamente si no necesitas un formato especial de texto
            if not temp_df_rv1.empty:
                st.dataframe(temp_df_rv1, use_container_width=True, hide_index=True)
            else:
                st.info("No hay datos para mostrar en Renta Variable - Parte 1.")

        with col2_rv:
            st.subheader("Desglose de Renta Variable")
            if not temp_df_rv2.empty:
                st.dataframe(temp_df_rv2, use_container_width=True, hide_index=True)
            else:
                st.info("No hay datos para mostrar en Renta Variable - Parte 2.")

        st.markdown("---")

        # --- Mostrar tablas de Renta Fija ---
        st.header("💳 Renta Fija")
        col1_rf, col2_rf = st.columns(2)

        with col1_rf:
            st.subheader("Resumen Renta Fija")
            if not temp_df_rf1.empty:
                st.dataframe(temp_df_rf1, use_container_width=True, hide_index=True)
            else:
                st.info("No hay datos para mostrar en Renta Fija - Parte 1.")

        with col2_rf:
            st.subheader("Desglose de Renta Fija")
            if not temp_df_rf2.empty:
                st.dataframe(temp_df_rf2, use_container_width=True, hide_index=True)
            else:
                st.info("No hay datos para mostrar en Renta Fija - Parte 2.")

        st.markdown("---")

        # --- Mostrar tablas de Alternativos ---
        st.header("💎 Alternativos")
        col1_al, col2_al = st.columns(2)

        with col1_al:
            st.subheader("Resumen de Alternativos")
            if not temp_df_al1.empty:
                st.dataframe(temp_df_al1, use_container_width=True, hide_index=True)
            else:
                st.info("No hay datos para mostrar en Alternativos - Parte 1.")

        with col2_al:
            st.subheader("Desglose de Alternativos")
            if not temp_df_al2.empty:
                st.dataframe(temp_df_al2, use_container_width=True, hide_index=True)
            else:
                st.info("No hay datos para mostrar en Alternativos - Parte 2.")

    else:
        st.error("No se pudieron cargar los datos. Por favor, revisa la ruta del archivo y los logs de error.")

    st.markdown("---")
    st.markdown("© 2025 BVC - Reporte Automático de Asset Allocation")

# Ejecutar la aplicación
if __name__ == "__main__":
    main()



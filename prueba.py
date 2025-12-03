# Copyright 2025 Snowflake Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import numpy as np
import pandas as pd
import math
import random
from streamlit_slickgrid import (
    add_tree_info,
    slickgrid,
    Formatters,
    Filters,
    FieldType,
    OperatorType,
    ExportServices,
    StreamlitSlickGridFormatters,
    StreamlitSlickGridSorters,
)

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

file_path = '/Users/matiasgonzalez/Library/CloudStorage/GoogleDrive-mgonzalez@buenavistacapital.com/.shortcut-targets-by-id/1Lbjcks5sDTC17AftNR6mDxW8bwAA7EaA/BVC/Asset Allocation/Comite y asset allocation bvc 2025 (version 1).xlsx'
sheets_names = ["Resumen portafolio", "Renta variable", "Renta_fija", "Alternativos"]

try:
    for sheet in sheets_names:
        if sheet == "Resumen portafolio" :
            temp_df_res1 = pd.read_excel(
                file_path,
                sheet_name=sheet,
                usecols='B:F',
                nrows=5,
                skiprows=1  
            )

            temp_df_res2 = pd.read_excel(
                file_path,
                sheet_name=sheet,
                usecols='H:R',
                nrows=22,
                skiprows=1  
            )

        if sheet == "Renta variable" :
            temp_df_rv1 = pd.read_excel(
                file_path,
                sheet_name=sheet,
                usecols='B:G',
                nrows=7,
                skiprows=1 
            )
            temp_df_rv2 = pd.read_excel(
                file_path,
                sheet_name=sheet,
                usecols='I:N',
                nrows=30,
                skiprows=1
            )

        if sheet == "Renta_fija" :
            temp_df_rf1 = pd.read_excel(
                file_path,
                sheet_name=sheet,
                usecols='B:G',
                nrows=7,
                skiprows=1 
            )
            temp_df_rf2 = pd.read_excel(
                file_path,
                sheet_name=sheet,
                usecols='I:N',
                nrows=21,
                skiprows=1 
            )

        if sheet == "Alternativos" :
            temp_df_al1 = pd.read_excel(
                file_path,
                sheet_name=sheet,
                usecols='B:F',
                nrows=5,
                skiprows=1 
            )
            temp_df_al2 = pd.read_excel(
                file_path,
                sheet_name=sheet,
                usecols='I:M',
                nrows=12,
                skiprows=1 
            )

except FileNotFoundError:
    print(f"Error: El archivo no se encontró en la ruta: {file_path}")
except ValueError as e:
    print(f"Error al leer el archivo o la hoja: {e}")
    print("Por favor, verifica el nombre de la hoja ('Resumen portafolio') y el formato del archivo.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")



"""
# Streamlit-SlickGrid demo

For more info, see https://github.com/streamlit/streamlit-slickgrid.
"""

# streamlit-slickgrid requires the data to be a list of dicts.
#
# For example:
#
#   data = [
#     {"id": 0, "continent": "america", "revenue": 20000, "paused": False},
#     {"id": 1, "continent": "africa",  "revenue": 40100, "paused": False},
#     {"id": 2, "continent": "asia",    "revenue": 10300, "paused": True},
#     {"id": 3, "continent": "europe",  "revenue": 30200, "paused": False},
#     ...
#   ]
#
# Here we're just building a random dataset:
data = mockData(1000)

# Coalesce the milestone, epic, and task fields into a single one called title.
data = add_tree_info(
    data,
    tree_fields=["milestone", "epic", "task"],
    join_fields_as="asset class",
    id_field="id",
)

# Some nice colors to use in the table.
red = "#ff4b4b"
orange = "#ffa421"
yellow = "#ffe312"
green = "#21c354"
teal = "#00c0f2"
blue = "#1c83e1"
violet = "#803df5"
white = "#fafafa"
gray = "#808495"
black = "#262730"

# Declare SlickGrid columns.
#
# See full list of options at:
# - https://github.com/ghiscoding/slickgrid-universal/blob/master/packages/common/src/interfaces/column.interface.ts#L40
#
# Not all column options are supported, though!
columns = [
    {
        "id": "title",
        "name": "Title",
        "field": "title",
        "sortable": True,
        "minWidth": 50,
        "type": FieldType.string,
        "filterable": True,
        "formatter": Formatters.tree,
        "exportCustomFormatter": Formatters.treeExport,
    },
    {
        "id": "duration",
        "name": "Duration (days)",
        "field": "duration",
        "sortable": True,
        "minWidth": 100,
        "type": FieldType.number,
        "filterable": True,
        "filter": {
            "model": Filters.slider,
            "operator": ">=",
        },
        "formatter": StreamlitSlickGridFormatters.numberFormatter,
        "params": {
            "colors": [
                # [maxValue, foreground, background]
                [20, blue, None],  # None is the same as leaving out
                [50, green],
                [100, gray],
            ],
            "minDecimal": 0,
            "maxDecimal": 2,
            "numberSuffix": "d",
            # You can pass your own styles here.
            # "style": {"text-align": "left", "padding": "0 0.5ch"},
        },
    },
    {
        "id": "stages",
        "name": "Stages",
        "field": "stages",
        "sortable": True,
        "sorter": StreamlitSlickGridSorters.numberArraySorter,
        "minWidth": 100,
        # Sorry, the "stages" field contains arrays, which aren't filterable.
        "filterable": False,
        "formatter": StreamlitSlickGridFormatters.stackedBarFormatter,
        "params": {
            "colors": [
                # [maxValue, foreground, background]
                [20, white, red],
                [70, black, orange],
                [100, white, green],
            ],
            "minDecimal": 0,
            "maxDecimal": 2,
            "min": 0,
            "max": 300,
            # You can pass your own styles here.
            # "style": {"text-align": "left", "padding": "0 0.5ch"},
        },
    },
    {
        "id": "%",
        "name": "% Complete",
        "field": "percentComplete",
        "sortable": True,
        "minWidth": 100,
        "type": FieldType.number,
        "filterable": True,
        "filter": {
            "model": Filters.sliderRange,
            "maxValue": 100,
            "operator": OperatorType.rangeInclusive,
            "filterOptions": {"hideSliderNumbers": False, "min": 0, "step": 5},
        },
        # Use the default progress bar formatter:
        # "formatter": Formatters.progressBar,
        #
        # Or use this fancy one that's ultra-configurable:
        "formatter": StreamlitSlickGridFormatters.barFormatter,
        "params": {
            "colors": [[50, white, red], [100, white, green]],
            "minDecimal": 0,
            "maxDecimal": 2,
            "numberSuffix": "%",
            # You can pass your own styles here.
            # "style": {"text-align": "left", "padding": "0 0.5ch"},
        },
    },
    {
        "id": "start",
        "name": "Start",
        "field": "start",
        "type": FieldType.date,
        "filterable": True,
        "filter": {"model": Filters.compoundDate},
        "formatter": Formatters.dateIso,
    },
    {
        "id": "finish",
        "name": "Finish",
        "field": "finish",
        "type": FieldType.date,
        "filterable": True,
        "filter": {"model": Filters.dateRange},
        "formatter": Formatters.dateIso,
    },
    {
        "id": "effort-driven",
        "name": "Effort Driven",
        "field": "effortDriven",
        "sortable": True,
        "minWidth": 100,
        "type": FieldType.boolean,
        "filterable": True,
        "filter": {
            "model": Filters.singleSelect,
            "collection": [
                {"value": "", "label": ""},
                {"value": True, "label": "True"},
                {"value": False, "label": "False"},
            ],
        },
        "formatter": Formatters.checkmarkMaterial,
    },
]


# Configure additional options streamlit-slickgrid.
#
# See full list of options at:
# - https://github.com/ghiscoding/slickgrid-universal/blob/master/packages/common/src/interfaces/gridOption.interface.ts#L76
#
# Not all grid options are supported, though!
options = {
    #
    # Allow filtering (based on column filter* properties)
    "enableFiltering": True,
    # --
    #
    # Debounce/throttle the input text filter if you have lots of data
    # filterTypingDebounce: 250,
    # --
    #
    # Set up export options.
    "enableTextExport": True,
    "enableExcelExport": True,
    "excelExportOptions": {"sanitizeDataExport": True},
    "textExportOptions": {"sanitizeDataExport": True},
    "externalResources": [
        ExportServices.ExcelExportService,
        ExportServices.TextExportService,
    ],
    # --
    #
    # Pin columns.
    # "frozenColumn": 0,
    # --
    #
    # Pin rows.
    # "frozenRow": 0,
    # --
    #
    # Don't scroll table when too big. Instead, just let it grow.
    # "autoHeight": True,
    # --
    #
    "autoResize": {
        "minHeight": 500,
    },
    # --
    #
    # Set up tree.
    "enableTreeData": True,
    "multiColumnSort": False,
    "treeDataOptions": {
        "columnId": "title",
        "indentMarginLeft": 15,
        "initiallyCollapsed": True,
        # This is a field that add_tree_info() inserts in your data:
        "parentPropName": "__parent",
        # This is a field that add_tree_info() inserts in your data:
        "levelPropName": "__depth",
        #
        # If you're building your own tree (without add_tree_info),
        # you should configure the props above accordingly.
        #
        # See below for more info:
        # - https://ghiscoding.github.io/slickgrid-react-demos/#/example27
        # - https://ghiscoding.github.io/slickgrid-react-demos/#/example28
    },
}

out = slickgrid(data, columns, options, key="mygrid", on_click="rerun")


@st.dialog("Details", width="large")
def show_dialog(item):
    st.write("Congrats! You clicked on the row below:")
    st.write(item)

    st.write("Here's a random chart for you:")
    st.write("")

    st.scatter_chart(np.random.randn(100, 5))


if out is not None:
    row, col = out
    show_dialog(data[row])
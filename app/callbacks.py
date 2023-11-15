# callbacks.py
from dash.dependencies import Input, Output, State
import pyodbc
import pandas as pd
from app import app
from dash import html
import requests  # Importa la biblioteca requests

def register_callbacks():
    @app.callback(
        [Output('tabla-ventas', 'children'),
         Output('sql-statement', 'children'),
         Output('graph', 'figure')],
        Input('button-sql', 'n_clicks'),
        State('sql-query', 'value')
    )
    def ejecutar_consulta(n_clicks, sql_query):
        # Verificar si sql_query no es None y no está vacío antes de ejecutar la consulta
        if sql_query is not None and sql_query.strip():
            # Asegurarse de que sql_query sea una cadena
            sql_query_str = str(sql_query)

            # Hacer una solicitud a tu API de chat con la pregunta
            pregunta = {"pregunta": sql_query}
            api_url = "http://127.0.0.1:3002/chat"  # la URL de tu API
            respuesta_api = requests.post(api_url, json=pregunta).json()

            # Obtener la respuesta de la API
            respuesta_chat = respuesta_api.get("Respuesta", "")

            # Conectar a la base de datos y realizar la consulta
            with pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                                'Server=W10MGTC105\\SQLEXPRESS;'
                                'Database=AdventureWorks2019;'
                                'Trusted_Connection=yes;'
                                'LoginTimeout=30;'
                                'encrypt=no;'
                                ) as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(respuesta_chat)
                    resultado = cursor.fetchall()

            # Resto del código...

            # Construir la tabla con pandas DataFrame solo si resultado no es None
            if resultado is not None:
                df = pd.DataFrame.from_records(resultado, columns=[col[0] for col in cursor.description])

                # Convertir DataFrame a una tabla HTML
                tabla_html = df.to_html(index=False, classes='table table-striped table-hover')

                # Construir la sentencia SQL
                sql_statement = f'Sentencia SQL: {respuesta_chat}'

                # Crear un gráfico de ejemplo (reemplazar con tus datos y configuraciones reales)
                graph_figure = {
                    'data': [{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'}],
                    'layout': {'title': 'Gráfico de ejemplo'}
                }

                # Retornar la tabla, la sentencia SQL y el gráfico
                return [tabla_html, f'Formato SQL: {sql_query_str}', graph_figure]
            else:
                return [], [], {'data': [], 'layout': {}}  # Devolver listas vacías si resultado es None
        else:
            return [], [], {'data': [], 'layout': {}}  # Devolver listas vacías si sql_query es None



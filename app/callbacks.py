# callbacks.py
from dash.dependencies import Input, Output, State
import pyodbc
import pandas as pd
from app import app
from dash import html, dcc
import requests

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

            try:
                # Intentar obtener la respuesta de la API
                respuesta_api = requests.post(api_url, json=pregunta).json()
                # Obtener la respuesta de la API y eliminar espacios en blanco al principio y al final
                respuesta_chat = respuesta_api.get("Respuesta").strip()
                print(f'Respuesta de la API: {respuesta_chat}')

                # Conectar a la base de datos y realizar la consulta
                with pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                                    'Server=W10MGTC105\\SQLEXPRESS;'
                                    'Database=Chinook;'
                                    'Trusted_Connection=yes;'
                                    'LoginTimeout=30;'
                                    'encrypt=no;'
                                    ) as conexion:
                    with conexion.cursor() as cursor:
                        cursor.execute(respuesta_chat)
                        resultado = cursor.fetchall()

            except requests.exceptions.JSONDecodeError as json_error:
                print(f"Error al decodificar la respuesta JSON de la API: {json_error}")
                return [], [], {'data': [], 'layout': {}}

            except ValueError as value_error:
                # Mostrar un mensaje específico cuando la IA no genera bien la consulta
                return [html.Div(value_error, style={'color': 'red'})], [], {'data': [], 'layout': {}}

            except Exception as e:
                print(f"Error al ejecutar la consulta SQL: {e}")
                return [], [], {'data': [], 'layout': {}}  # Devolver listas vacías en caso de error

            # Construir la tabla con pandas DataFrame solo si resultado no es None
            if resultado is not None:
                df = pd.DataFrame.from_records(resultado, columns=[col[0] for col in cursor.description])

                # Convertir DataFrame a una tabla HTML
                tabla_html = df.to_html(index=False, classes='table table-striped table-hover')

                # Utilizar html.Div para mostrar la tabla en 'tabla-ventas'
                tabla_div = html.Div([html.Table([html.Tr([html.Th(col) for col in df.columns])] +
                                                [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))])],
                                              style={'overflowY': 'scroll', 'height': '300px'})
                # Construir la sentencia SQL
                sql_statement = f'Sentencia SQL: {respuesta_chat}'

                # Crear un gráfico de ejemplo (reemplazar con tus datos y configuraciones reales)
                graph_figure = {
                    'data': [{'x': df.columns, 'y': df.iloc[0], 'type': 'bar', 'name': 'SF'}],
                    'layout': {'title': 'Gráfico de ejemplo'}
                }

                # Retornar la tabla, la sentencia SQL y el gráfico
                return [tabla_div, f'Formato SQL: {sql_statement}', graph_figure]
            else:
                return [], [], {'data': [], 'layout': {}}  # Devolver listas vacías si resultado es None
        else:
            return [], [], {'data': [], 'layout': {}}  # Devolver listas vacías si sql_query es None

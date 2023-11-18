# layout.py
from dash import dcc, html

def create_layout():
    return html.Div([
        html.Div([
            html.H2("Reporte empresarial AdventureWorks2019", className='text-primary text-center mt-4 mb-4'),
        ], className='container'),

        html.Div([
            # Contenedor para el input y botón centrados
            html.Div([
                html.Div([
                    dcc.Input(
                        id='sql-query',
                        type='text',
                        placeholder='Ingrese la consulta aquí',
                        className='form-control',
                        value=''  # Agrega un valor predeterminado aquí
                    ),
                    html.Button('Ejecutar Consulta', id='button-sql', n_clicks=0, className='btn btn-primary mt-3'),
                ], className='card-body', style={'textAlign': 'center', 'marginBottom': '20px'})
            ], className='card', style={'maxWidth': '400px', 'margin': 'auto'}),
        ], className='row', style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '20px'}),

        html.Div(id='tabla-ventas'),  # Aquí agregamos el componente para mostrar la tabla

        html.Div([
            # Contenedor para la gráfica y la sentencia SQL
            html.Div([
                # Dividir en dos columnas usando Bootstrap (col-md-6)
                html.Div([
                    # Usar dcc.Graph para mostrar el gráfico
                    dcc.Graph(id='graph'),
                ], className='card', style={'maxWidth': '50%', 'marginRight': '10px'}),

                html.Div([
                    # Agregar un título para el formato SQL
                    html.H4("Formato SQL", className='text-primary mt-4'),
                    # Mostrar la respuesta del API en lugar de la pregunta
                    dcc.Markdown(id='sql-statement', dangerously_allow_html=True, className='mt-2', style={'white-space': 'pre-wrap'}),
                ], className='card', style={'maxWidth': '50%'}),
            ], className='row', style={'display': 'flex', 'justify-content': 'center'}),
        ], className='row'),

    ], className='container-fluid', style={'backgroundColor': 'white', 'padding': '20px'})

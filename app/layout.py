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
                ], className='card-body', style={'text-align': 'center', 'margin-bottom': '20px'})
            ], className='card', style={'maxWidth': '400px', 'margin': 'auto'}),
        ], className='row', style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'}),

        html.Div([
            # Contenedor para la tabla de resultados
            html.Div([
                dcc.Loading(
                    id="loading-table",
                    type="default",
                    children=[
                        html.Table([
                            html.Thead([
                                html.Tr([
                                    html.Th("Tabla de Consultas", style={'padding': '10px'})
                                ])
                            ]),
                            html.Tbody([
                                html.Tr([
                                    dcc.Markdown(id='tabla-ventas', dangerously_allow_html=True, className='table table-striped table-hover')
                                ])
                            ])
                        ], className='table')
                    ]
                )
            ], className='card', style={'maxWidth': '50%', 'marginRight': '10px', 'margin-bottom': '20px'}),
        ], className='row', style={'display': 'flex', 'justify-content': 'center'}),

        html.Div([
            # Contenedor para la gráfica y la sentencia SQL
            html.Div([
                # Dividir en dos columnas usando Bootstrap (col-md-6)
                html.Div([
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

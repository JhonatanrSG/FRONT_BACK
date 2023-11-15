# index.py
from app import app, callbacks
from app.layout import create_layout

# Asigna el layout a la aplicación
app.layout = create_layout()

# Registra las callbacks
callbacks.register_callbacks()

# Utiliza external_stylesheets directamente
external_stylesheets = [
    '/assets/bootstrap-5.3.2-dist/css/bootstrap.min.css',  # Ajusta la ruta según tu estructura de carpetas
    'https://stackpath.bootstrapcdn.com/bootstrap/5.3.2/css/bootstrap.css/bootstrap.min.css'
]

app.css.external_stylesheets = external_stylesheets

if __name__ == '__main__':
    app.run_server(debug=True)



if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)






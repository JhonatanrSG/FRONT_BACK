from dash import Dash

app = Dash(__name__, suppress_callback_exceptions=True)

from app import layout, callbacks

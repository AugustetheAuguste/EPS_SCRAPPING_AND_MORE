# layout.py
from dash import html
import dash_uploader as du

layout = html.Div(className="container", children=[
    html.H2("Face Detection and Recognition", className="my-4"),
    html.Div(className="mb-4", children=[
        du.Upload(id='upload-zip', text='Drag and Drop or Select a Zip File', filetypes=['zip'])
    ]),
    html.Button('Process', id='process-button', n_clicks=0, className="btn btn-primary mb-3"),  # ID is 'process-button'
    html.Div(id='output', className="mt-3")
])

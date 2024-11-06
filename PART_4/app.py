import dash
import dash_uploader as du
from layout import layout
from callbacks import register_callbacks

import sys
import codecs

# Set encoding to UTF-8 for all standard I/O operations
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"])
du.configure_upload(app, folder="uploads")  # Ensure the uploads folder is correct

app.layout = layout
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)

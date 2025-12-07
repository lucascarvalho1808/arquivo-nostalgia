from flask import Flask, render_template
import os
from routes.auth import auth_bp
from routes.legal import legal_bp
from routes.main import main_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

# Registrar Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(legal_bp)

@app.route('/')
def index():
    return render_template('index.html')

# lembrar de tirar parte do debug ao final do projeto 
if __name__ == '__main__':
    app.run(debug=True)
# fim do debug
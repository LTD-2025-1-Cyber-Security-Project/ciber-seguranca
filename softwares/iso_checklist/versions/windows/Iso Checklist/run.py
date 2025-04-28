import os
import webbrowser
import threading
import time
from app import app

def open_browser():
    # Aguarda 1.5 segundos para garantir que o servidor iniciou
    time.sleep(1.5)
    # Abre o navegador padrão
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Inicia um thread para abrir o navegador
    threading.Thread(target=open_browser).start()
    
    # Inicia o servidor Flask
    app.run(debug=False)
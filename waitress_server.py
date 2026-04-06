from waitress import serve
from run import app

if __name__ == '__main__':
    print("Iniciando RetroNexus con Waitress en puerto 8080...")
    serve(app, host='0.0.0.0', port=8080)

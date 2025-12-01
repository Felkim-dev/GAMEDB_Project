from app import create_app
import time
from sqlalchemy import text

app=create_app()

def wait_for_db():
    """Esperar a que la base de datos esté lista"""
    from app.extensions import db
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            with app.app_context():
                db.session.execute(text('SELECT 1'))
            print("✅ Conexión a la base de datos establecida")
            return True
        except Exception as e:
            retry_count += 1
            print(f"⏳ Esperando a la base de datos... ({retry_count}/{max_retries})")
            time.sleep(2)
    
    print("❌ No se pudo conectar a la base de datos")
    return False

if __name__ == "__main__":
    # Esperar a que la base de datos esté lista
    if wait_for_db():
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Error: No se pudo iniciar la aplicación")

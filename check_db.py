import sqlite3
import os

def revisar_datos():
    ruta_db = "data/facial_emotions.db"
    
    # 1. Verificar si el archivo existe físicamente
    if not os.path.exists(ruta_db):
        print(f"❌ ERROR: No se encuentra el archivo en: {os.path.abspath(ruta_db)}")
        return

    try:
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()
        
        print(f"✅ Conectado a: {ruta_db}")
        
        # 2. Consultar usuarios
        cursor.execute("SELECT id, nombre, apellido, email FROM personas")
        usuarios = cursor.fetchall()
        
        print("\n--- USUARIOS REGISTRADOS ---")
        if not usuarios:
            print("La base de datos está abierta pero no tiene usuarios registrados aún.")
        else:
            for u in usuarios:
                print(f"ID: {u[0]} | Nombre: {u[1]} {u[2]} | Email: {u[3]}")
        
        conn.close()
    except Exception as e:
        print(f"❌ Error al leer la base de datos: {e}")

if __name__ == "__main__":
    revisar_datos()
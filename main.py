from src.database.db_handler import DatabaseHandler

def probar_sistema():
    # 1. Instanciar el manejador de la base de datos
    db = DatabaseHandler()
    print("✅ Base de datos inicializada.")

    # 2. Intentar registrar un usuario (Tu primer registro)
    print("\n--- Probando Registro de Persona ---")
    nuevo_id = db.registrar_persona(
        nombre="TuNombre", 
        apellido="TuApellido", 
        email="tu_correo@ejemplo.com"
    )

    if nuevo_id:
        print(f"✨ Persona registrada con éxito. ID asignado: {nuevo_id}")
    else:
        print("⚠️ No se pudo registrar (posible duplicado).")

    # 3. Simular el guardado de una emoción
    if nuevo_id:
        print("\n--- Guardando Detección de Prueba ---")
        db.guardar_deteccion(
            persona_id=nuevo_id, 
            emocion="Felicidad", 
            confianza=98.5
        )
        print("💾 Emoción guardada en el historial.")

if __name__ == "__main__":
    probar_sistema()
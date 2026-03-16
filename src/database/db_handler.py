import sqlite3
import os
from datetime import datetime

class DatabaseHandler:
    def __init__(self, db_path="data/facial_emotions.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.inicializar_tablas()

    def conectar(self):
        return sqlite3.connect(self.db_path)

    def inicializar_tablas(self):
        query_personas = """
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            embedding_path TEXT
        )
        """
        query_historial = """
        CREATE TABLE IF NOT EXISTS historial_emociones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER,
            emocion TEXT,
            confianza REAL,
            fecha_hora TEXT,
            FOREIGN KEY (persona_id) REFERENCES personas (id)
        )
        """
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query_personas)
            cursor.execute(query_historial)
            conn.commit()

    def registrar_persona(self, nombre, apellido, email, embedding):
        embedding_str = str(embedding)
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO personas (nombre, apellido, email, embedding_path) VALUES (?, ?, ?, ?)",
                    (nombre, apellido, email, embedding_str)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def guardar_deteccion(self, persona_id, emocion, confianza):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO historial_emociones (persona_id, emocion, confianza, fecha_hora) VALUES (?, ?, ?, ?)",
                (persona_id, emocion, confianza, fecha)
            )
            conn.commit()
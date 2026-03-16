import customtkinter as ctk
import cv2
from PIL import Image
from src.core.detector import DetectorRostros
from src.database.db_handler import DatabaseHandler

class VentanaRegistro(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registro de Usuario - URU")
        self.geometry("450x550")
        
        # Esto hace que la ventana sea "modal" (bloquea la de atrás)
        self.grab_set() 

        self.db = DatabaseHandler()
        self.detector = DetectorRostros()

        # UI
        ctk.CTkLabel(self, text="NUEVO REGISTRO", font=("Arial", 20, "bold")).pack(pady=20)

        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre", width=280)
        self.entry_nombre.pack(pady=10)

        self.entry_apellido = ctk.CTkEntry(self, placeholder_text="Apellido", width=280)
        self.entry_apellido.pack(pady=10)

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Email", width=280)
        self.entry_email.pack(pady=10)

        self.btn_accion = ctk.CTkButton(self, text="Capturar Rostro y Guardar", 
                                        command=self.ejecutar_registro, fg_color="green")
        self.btn_accion.pack(pady=30)

        self.status = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status.pack(pady=10)

    def ejecutar_registro(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        email = self.entry_email.get()

        if not (nombre and apellido and email):
            self.status.configure(text="❌ Por favor, llena todos los campos", text_color="red")
            return

        # Captura rápida de la cámara para sacar el embedding
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            self.status.configure(text="⌛ Procesando rostro...", text_color="white")
            self.update()
            
            embedding = self.detector.generar_embedding(frame)
            
            if embedding:
                res = self.db.registrar_persona(nombre, apellido, email, embedding)
                if res:
                    self.status.configure(text="✅ Registrado con éxito", text_color="green")
                    self.after(1500, self.destroy)
                else:
                    self.status.configure(text="❌ Error: El email ya existe", text_color="red")
            else:
                self.status.configure(text="❌ No se detectó rostro", text_color="yellow")
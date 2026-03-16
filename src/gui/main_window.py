import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from src.core.emociones import AnalizadorEmociones
from src.database.db_handler import DatabaseHandler

class AppEmociones(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Reconocimiento Facial - URU")
        self.geometry("900x600")
        
        # Configurar el layout (Cuadrícula)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Menú lateral) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="IA Facial", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.btn_registro = ctk.CTkButton(self.sidebar, text="Registrar Usuario")
        self.btn_registro.grid(row=1, column=0, padx=20, pady=10)

        self.btn_analizar = ctk.CTkButton(self.sidebar, text="Iniciar Análisis")
        self.btn_analizar.grid(row=2, column=0, padx=20, pady=10)

        # --- Área de Video ---
        self.video_frame = ctk.CTkFrame(self)
        self.video_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.video_label = ctk.CTkLabel(self.video_frame, text="")
        self.video_label.pack(expand=True, fill="both")

        # Inicializar lógica
        self.cap = None
        self.analizador = AnalizadorEmociones()
        self.db = DatabaseHandler()

    def actualizar_video(self):
        ret, frame = self.cap.read()
        if ret:
            # Aquí llamaremos a tu lógica de emociones más tarde
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)
            self.video_label.configure(image=img_tk)
            self.video_label.image = img_tk
            
        self.after(10, self.actualizar_video)

if __name__ == "__main__":
    app = AppEmociones()
    app.mainloop()
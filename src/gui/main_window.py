import customtkinter as ctk
import cv2
from PIL import Image
from src.core.emociones import AnalizadorEmociones
from src.database.db_handler import DatabaseHandler
from src.gui.registro_window import VentanaRegistro
from src.gui.reportes_window import VentanaReportes # Importación nueva

class AppEmociones(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Reconocimiento Facial y Analítica - URU 2026")
        self.geometry("1100x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # IA y Base de Datos
        self.analizador = AnalizadorEmociones()
        self.db = DatabaseHandler()
        self.cap = None
        self.camara_activa = False
        
        # Variables de control
        self.conteo_frames = 0
        self.nombre_actual = "Desconocido"
        self.usuarios_db = []

        # --- Layout Principal ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar (Izquierda)
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="🤖 IA FACIAL URU", 
                                       font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.pack(pady=(30, 20))

        # Botones de Control
        self.btn_analizar = ctk.CTkButton(self.sidebar, text="Encender Cámara", 
                                         command=self.toggle_analisis, height=45)
        self.btn_analizar.pack(padx=20, pady=10)

        self.btn_registro = ctk.CTkButton(self.sidebar, text="Registrar Usuario", 
                                         command=self.abrir_ventana_registro, 
                                         fg_color="transparent", border_width=2, height=45)
        self.btn_registro.pack(padx=20, pady=10)

        # NUEVO: Botón de Reportes y Estadísticas
        self.btn_reportes = ctk.CTkButton(self.sidebar, text="Estadísticas y Reportes", 
                                          command=self.abrir_ventana_reportes, 
                                          fg_color="gray30", height=45)
        self.btn_reportes.pack(padx=20, pady=10)

        # Panel de Datos en Tiempo Real
        self.info_frame = ctk.CTkFrame(self.sidebar, fg_color="gray10")
        self.info_frame.pack(padx=20, pady=30, fill="x")
        
        self.label_usuario = ctk.CTkLabel(self.info_frame, text="Usuario: ---", 
                                         font=("Arial", 16, "bold"), text_color="#2ecc71")
        self.label_usuario.pack(pady=10)
        
        self.label_emocion = ctk.CTkLabel(self.info_frame, text="Emoción: ---", font=("Arial", 15))
        self.label_emocion.pack(pady=5)
        
        self.label_confianza = ctk.CTkLabel(self.info_frame, text="Confianza: ---", font=("Arial", 15))
        self.label_confianza.pack(pady=5)

        # Contenedor de Video (Derecha)
        self.video_container = ctk.CTkFrame(self, fg_color="black", corner_radius=15)
        self.video_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.video_label = ctk.CTkLabel(self.video_container, text="CÁMARA APAGADA")
        self.video_label.pack(expand=True, fill="both")

    def cargar_usuarios(self):
        """Sincroniza los usuarios de la DB con la memoria RAM"""
        try:
            with self.db.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nombre, embedding_path FROM personas")
                self.usuarios_db = cursor.fetchall()
                print(f"✅ DB Sincronizada: {len(self.usuarios_db)} usuarios listos.")
        except Exception as e:
            print(f"Error cargando usuarios: {e}")

    def toggle_analisis(self):
        if not self.camara_activa:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened(): return

            self.cargar_usuarios() 
            self.camara_activa = True
            self.btn_analizar.configure(text="Apagar Cámara", fg_color="#e74c3c")
            self.actualizar_frame()
        else:
            self.camara_activa = False
            if self.cap: self.cap.release()
            self.btn_analizar.configure(text="Encender Cámara", fg_color=["#3a7ebf", "#1f538d"])
            self.video_label.configure(image="", text="CÁMARA APAGADA")
            self.nombre_actual = "Desconocido"

    def actualizar_frame(self):
        if self.camara_activa:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                
                # 1. Análisis de Emociones
                datos = self.analizador.analizar_rostro(frame)
                
                if datos:
                    # 2. Reconocimiento de Identidad cada 30 frames
                    if self.conteo_frames % 30 == 0:
                        emb_actual = self.analizador.detector.generar_embedding(frame)
                        if emb_actual:
                            self.nombre_actual = self.analizador.detector.buscar_coincidencia(
                                emb_actual, self.usuarios_db
                            )
                            
                            # 3. GUARDADO AUTOMÁTICO EN HISTORIAL
                            # Solo guardamos si es un usuario conocido
                            if self.nombre_actual != "Desconocido":
                                self.db.guardar_deteccion(
                                    self.nombre_actual, 
                                    datos['emocion'], 
                                    round(float(datos['confianza']), 2)
                                )
                    
                    self.conteo_frames += 1

                    # Dibujar Rectángulo Dinámico
                    x, y, w, h = datos['box']['x'], datos['box']['y'], datos['box']['w'], datos['box']['h']
                    color = (46, 204, 113) if self.nombre_actual != "Desconocido" else (231, 76, 60)
                    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, f"{self.nombre_actual}", (x, y-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                    
                    # Actualizar Interfaz (Redondeando decimales)
                    conf_limpia = round(float(datos['confianza']), 2)
                    self.label_usuario.configure(text=f"Usuario: {self.nombre_actual}")
                    self.label_emocion.configure(text=f"Emoción: {datos['emocion']}")
                    self.label_confianza.configure(text=f"Confianza: {conf_limpia}%")

                # Renderizar en la GUI
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(720, 540))
                self.video_label.configure(image=img_ctk, text="")
            
            self.after(15, self.actualizar_frame)

    def abrir_ventana_registro(self):
        ventana = VentanaRegistro(self)
        self.wait_window(ventana)
        self.cargar_usuarios()

    def abrir_ventana_reportes(self):
        """Abre la ventana de estadísticas y analítica"""
        VentanaReportes(self)

if __name__ == "__main__":
    app = AppEmociones()
    app.mainloop()
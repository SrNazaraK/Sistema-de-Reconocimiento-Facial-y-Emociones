import customtkinter as ctk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VentanaReportes(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Panel de Estadísticas y Reportes")
        self.geometry("900x700")
        self.focus()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Título y Botón Exportar
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.label_titulo = ctk.CTkLabel(self.header, text="Análisis Histórico de Emociones", 
                                         font=ctk.CTkFont(size=20, weight="bold"))
        self.label_titulo.pack(side="left")

        self.btn_exportar = ctk.CTkButton(self.header, text="Exportar CSV", 
                                          command=self.exportar_datos, fg_color="#27ae60")
        self.btn_exportar.pack(side="right", padx=10)

        # --- SECCIÓN SUPERIOR: GRÁFICO ---
        self.frame_grafico = ctk.CTkFrame(self)
        self.frame_grafico.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.mostrar_grafico()

        # --- SECCIÓN INFERIOR: TABLA ---
        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        # Configuración de la tabla (Treeview de Tkinter)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", 
                        fieldbackground="#2b2b2b", rowheight=25)
        
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("Fecha", "Nombre", "Emoción", "Confianza"), show="headings")
        self.tabla.heading("Fecha", text="Fecha y Hora")
        self.tabla.heading("Nombre", text="Usuario")
        self.tabla.heading("Emoción", text="Emoción")
        self.tabla.heading("Confianza", text="Confianza %")
        
        self.tabla.pack(expand=True, fill="both", padx=10, pady=10)
        self.llenar_tabla()

    def mostrar_grafico(self):
        """Genera un gráfico de pastel basado en las detecciones reales"""
        datos = self.parent.db.obtener_estadisticas_globales()
        
        if not datos:
            ctk.CTkLabel(self.frame_grafico, text="No hay suficientes datos para graficar").pack(pady=50)
            return

        emociones = [d[0] for d in datos]
        conteos = [d[1] for d in datos]

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor('#2b2b2b') # Color de fondo oscuro
        
        ax.pie(conteos, labels=emociones, autopct='%1.1f%%', startangle=140, 
               textprops={'color':"w"}, colors=['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6'])
        ax.set_title("Distribución de Emociones Detectadas", color="white")

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

    def llenar_tabla(self):
        """Carga los últimos 100 registros en la tabla"""
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        registros = self.parent.db.obtener_historial_completo()
        for reg in registros:
            self.tabla.insert("", "end", values=reg)

    def exportar_datos(self):
        exito = self.parent.db.exportar_a_csv()
        if exito:
            messagebox.showinfo("Éxito", "Reporte exportado como 'reporte_emociones.csv'")
        else:
            messagebox.showerror("Error", "No se pudo exportar el archivo.")
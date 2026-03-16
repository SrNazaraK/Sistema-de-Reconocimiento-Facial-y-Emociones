import cv2
import numpy as np
import os
from deepface import DeepFace
import json

class DetectorRostros:
    def __init__(self):
        # Usamos Facenet512 por su alta precisión
        self.model_name = "Facenet512"
        self.detector_backend = "opencv"

    def generar_embedding(self, frame):
        """
        Extrae y normaliza el vector característico del rostro.
        """
        try:
            embeddings = DeepFace.represent(
                img_path = frame,
                model_name = self.model_name,
                enforce_detection = True,
                detector_backend = self.detector_backend,
                align = True
            )
            
            # Obtenemos el vector original
            raw_embedding = embeddings[0]["embedding"]
            
            # --- NORMALIZACIÓN L2 ---
            # Esto asegura que el vector tenga magnitud 1, evitando distancias locas
            vector = np.array(raw_embedding, dtype='float32')
            norma = np.linalg.norm(vector)
            if norma > 0:
                vector = vector / norma
                
            return vector.tolist() # Lo devolvemos como lista para JSON/DB
        except Exception:
            return None

    def buscar_coincidencia(self, embedding_nuevo, lista_usuarios):
        """
        Compara el rostro actual contra la base de datos.
        """
        if not lista_usuarios:
            return "Desconocido"

        mejor_distancia = 100.0
        nombre_detectado = "Desconocido"
        
        # Aseguramos que el nuevo embedding esté normalizado y sea NumPy
        emb_nuevo_np = np.array(embedding_nuevo, dtype='float32')
        norma_nuevo = np.linalg.norm(emb_nuevo_np)
        if norma_nuevo > 0:
            emb_nuevo_np = emb_nuevo_np / norma_nuevo

        for user_id, nombre, embedding_str in lista_usuarios:
            try:
                # 1. Convertir string de DB a vector NumPy
                embedding_limpio = embedding_str.replace("'", '"')
                emb_guardado = json.loads(embedding_limpio)
                emb_guardado_np = np.array(emb_guardado, dtype='float32')
                
                # 2. Normalizar el guardado por si acaso quedó basura vieja
                norma_guardado = np.linalg.norm(emb_guardado_np)
                if norma_guardado > 0:
                    emb_guardado_np = emb_guardado_np / norma_guardado
                
                # 3. Distancia Euclidiana (Ahora siempre estará entre 0 y 2)
                distancia = float(np.linalg.norm(emb_nuevo_np - emb_guardado_np))
                
                # Debug en consola
                print(f"-> Comparando con {nombre}: Distancia {distancia:.4f}")

                # 4. Umbral (Threshold)
                # Con normalización L2, el punto dulce suele ser 0.85 - 1.05
                if distancia < 1.0: 
                    if distancia < mejor_distancia:
                        mejor_distancia = distancia
                        nombre_detectado = nombre
            except Exception as e:
                print(f"Error procesando {nombre}: {e}")
                continue
                    
        return nombre_detectado

    def guardar_imagen_rostro(self, frame, nombre):
        """Guarda captura física del rostro"""
        path_dir = "data/rostros_registrados"
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
            
        filename = f"{path_dir}/{nombre.lower().replace(' ', '_')}.jpg"
        cv2.imwrite(filename, frame)
        return filename
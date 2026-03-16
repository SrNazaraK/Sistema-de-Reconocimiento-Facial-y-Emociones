from deepface import DeepFace
import numpy as np

class DetectorRostros:
    def __init__(self):
        # Facenet es muy preciso para reconocimiento de identidad
        self.modelo_reconocimiento = "Facenet"
        # Usaremos opencv como detector rápido para el registro
        self.detector_backend = "opencv"

    def generar_embedding(self, frame):
        """
        Extrae el vector numérico (embedding) de un rostro.
        Esto es lo que guardaremos en la DB para reconocerte luego.
        """
        try:
            # represent() convierte la cara en una lista de 128 o 512 números
            resultados = DeepFace.represent(
                img_path = frame, 
                model_name = self.modelo_reconocimiento,
                detector_backend = self.detector_backend,
                enforce_detection = True
            )
            
            # Retornamos el primer rostro detectado
            return resultados[0]["embedding"]
        except Exception as e:
            print(f"Error al generar embedding: {e}")
            return None

    def comparar_rostros(self, embedding_nuevo, embedding_guardado):
        """
        Compara dos firmas faciales para saber si es la misma persona.
        """
        # En la práctica, DeepFace.verify() hace esto, 
        # pero aquí podemos usar distancia euclidiana simple más adelante.
        pass
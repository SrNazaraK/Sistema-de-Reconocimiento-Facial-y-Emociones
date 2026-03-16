from deepface import DeepFace
import cv2
from src.core.detector import DetectorRostros # <-- Importamos el detector de identidad

class AnalizadorEmociones:
    def __init__(self):
        # 1. Iniciamos el detector de identidad (Reconocimiento Facial)
        self.detector = DetectorRostros() 
        
        # 2. Diccionario de traducción para la URU
        self.emociones_espanol = {
            'angry': 'Enojo',
            'disgust': 'Disgusto',
            'fear': 'Miedo',
            'happy': 'Felicidad',
            'sad': 'Tristeza',
            'surprise': 'Sorpresa',
            'neutral': 'Neutral'
        }

    def analizar_rostro(self, frame):
        """
        Analiza un frame de video y devuelve la emoción dominante y su confianza.
        """
        try:
            # Analizamos emociones
            # Usamos enforce_detection=True para que solo analice si hay una cara clara
            resultados = DeepFace.analyze(
                img_path = frame, 
                actions = ['emotion'], 
                enforce_detection = True,
                detector_backend = 'opencv'
            )
            
            res = resultados[0]
            emocion_en = res['dominant_emotion']
            confianza = res['emotion'][emocion_en]
            
            return {
                'emocion': self.emociones_espanol.get(emocion_en, emocion_en),
                'confianza': round(confianza, 2),
                'box': res['region'] 
            }
        except Exception as e:
            # Si no detecta rostro, no imprimimos error para no llenar la consola
            return None

# --- Bloque de prueba rápida actualizado ---
if __name__ == "__main__":
    # Nota: Usamos CAP_DSHOW por el error de Windows que tuviste
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    analizador = AnalizadorEmociones()
    
    print("Iniciando prueba combinada (Emociones + Identidad)...")
    print("Presiona 'q' para salir...")
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1) # Efecto espejo
        data = analizador.analizar_rostro(frame)
        
        if data:
            # Probamos también el detector de identidad aquí mismo
            emb = analizador.detector.generar_embedding(frame)
            # (En esta prueba rápida no tenemos la lista de la DB, 
            # pero verificamos que el objeto detector exista)
            
            x, y, w, h = data['box']['x'], data['box']['y'], data['box']['w'], data['box']['h']
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Emocion: {data['emocion']}", 
                        (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Prueba de Integracion', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
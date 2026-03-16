from deepface import DeepFace
import cv2

class AnalizadorEmociones:
    def __init__(self):
        # Las 7 emociones básicas requeridas
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
            # DeepFace analiza el frame buscando emociones
            # enforce_detection=False evita que el programa se caiga si no ve un rostro
            resultados = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            
            # Tomamos el primer rostro detectado
            res = resultados[0]
            emocion_en = res['dominant_emotion']
            confianza = res['emotion'][emocion_en]
            
            return {
                'emocion': self.emociones_espanol.get(emocion_en, emocion_en),
                'confianza': round(confianza, 2),
                'box': res['region'] # Coordenadas del rostro (x, y, w, h)
            }
        except Exception as e:
            print(f"Error en análisis: {e}")
            return None

# Bloque de prueba rápida
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    analizador = AnalizadorEmociones()
    
    print("Presiona 'q' para salir...")
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        data = analizador.analizar_rostro(frame)
        
        if data:
            # Dibujar el overlay (Requisito de la pantalla de detección)
            x, y, w, h = data['box']['x'], data['box']['y'], data['box']['w'], data['box']['h']
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{data['emocion']} ({data['confianza']}%)", 
                        (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Prueba de Emociones', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
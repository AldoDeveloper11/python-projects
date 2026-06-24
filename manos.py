import cv2
import time
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# modelo -->
base = python.BaseOptions(model_asset_path = 'hand_landmarker.task')
opcion = vision.HandLandmarkerOptions(base_options = base, running_mode = vision.RunningMode.VIDEO, num_hands=2)
hand_landmarker = vision.HandLandmarker.create_from_options(opcion)

# conexiones del esqueleto -->
conexiones = [
    (0, 1), (1, 2), (2, 3), (3, 4),       # pulgar
    (0, 5), (5, 6), (6, 7), (7, 8),       # índice
    (0, 9), (9, 10), (10, 11), (11, 12), # medio
    (0, 13), (13, 14), (14, 15), (15, 16), # anular
    (0, 17), (17, 18), (18, 19), (19, 20) # meñique
]

# camara -->
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    cam = cv2.VideoCapture(1)
if not cam.isOpened():
    raise SystemExit("No se pudo abrir la cámara. Revisa el índice o los permisos.")

# Canvas -->
canvas = None  
xp, yp = 0, 0

# Bucle -->
while True:
    exito, frame = cam.read()
    frame = cv2.flip(frame, 1)  # Voltear horizontalmente
    if not exito or frame is None:
        print("No se pudo leer frame")
        break

    # BGR -> RGB -->
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Formato de video -->
    image = mp.Image(image_format = mp.ImageFormat.SRGB, data = rgb)

    # tiempo de procesamiento -->
    tiempo = int(time.time() * 1000)

    # Captura -->
    hand_results = hand_landmarker.detect_for_video(image, tiempo)

    # Asegurar canvas -->
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Dibujar manos -->
    if hand_results and hand_results.hand_landmarks:
        h, w, _ = frame.shape

        for hand_landmark in hand_results.hand_landmarks:

            # Dibujar conexiones -->
            for start_idx, end_idx in conexiones:

                start = hand_landmark[start_idx]
                end = hand_landmark[end_idx]

                x1, y1 = int(start.x * w), int(start.y * h)
                x2, y2 = int(end.x * w), int(end.y * h)
                cv2.line(frame, (x1, y1), (x2, y2), (250, 0, 0), 3)

            # Detección de dedos -->
            index_up = hand_landmark[8].y < hand_landmark[6].y
            middle_up = hand_landmark[12].y < hand_landmark[10].y
            ring_up = hand_landmark[16].y < hand_landmark[14].y
            pinky_up = hand_landmark[20].y < hand_landmark[18].y
            solo_indice = index_up and not (middle_up or ring_up or pinky_up)
            borrar_gesto = index_up and middle_up and not (ring_up or pinky_up)

            # Coordenadas del dedo índice -->
            indice = hand_landmark[8]
            x, y = int(indice.x * w), int(indice.y * h)

            if solo_indice:
                # Pintar -->
                if xp == 0 and yp == 0:
                    xp, yp = x, y
                cv2.line(canvas, (xp, yp), (x, y), (0, 255, 0), 5)
                xp, yp = x, y

            elif borrar_gesto:
                medio = hand_landmark[12]
                x2, y2 = int(medio.x * w), int(medio.y * h)
                distancia = ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5

                if distancia < 40:
                    cv2.circle(canvas, (x, y), 40, (0, 0, 0), -1)
                xp, yp = 0, 0

            else:
                xp, yp = 0, 0

            # Dibujar puntos -->
            for landmark in hand_landmark:
                x, y = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), 2)

    else:
        xp, yp = 0, 0

    # Combinar canvas con frame -->
    frame = cv2.add(frame, canvas)

    # Mostrar frame -->
    cv2.imshow("Manos", frame)

    # Salir con 'q' -->
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

# Liberar recursos -->
cam.release()
cv2.destroyAllWindows()
import os
import time
import cv2
import numpy as np
import cvzone
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh 
mp_drawing = mp.solutions.drawing_ultils


class PoseDetectionMediapipe:
    def __init__(self,min_detection_confidence = 0.5, min_tracking_confidence = 0.5):
        self.face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence = min_detection_confidence, min_tracking_confidence = min_tracking_confidence)
        self.drawing_spec = mp_drawing.DrawingSpec(thickness = 1, circle_radius = 1)
    def _process(self,img):
        img.flags.writeable = False
        result = self.face_mesh.process(img)
        img.flags.writeable = True
        return result
    def _detect_pose(self, img):
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        result = self._process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img_h, img_w, img_c = img.shape
        face_2d, face_3d = [], []

        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmarks):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)
                    x, y = int(lm.x * img_w), int(lm.y * img_h)

                    face_2d.append((x, y))
                    face_3d.append((x, y, lm.z))

            face_2d = np.array(face_2d, dtype = np.float32)
            face_3d = np.array(face_3d, dtype = np.float32)

            focal_length = 1 * img_w
            cam_matrix = np.array([
                (focal_length, 0, img_h / 2),
                (0, focal_length, img_w / 2),
                (0, 0, 1)
            ])
            dist_matrix = np.zeros((4, 1), dtype = np.float32)
            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            rmat, jac = cv2.Rodrigues(rot_vec)

            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            x = angles[0] * 360
            y = angles[1] * 360
            z = angles[2] * 360

            pose_direction = []
            if y < -10:
                text = 'Looking Left'
            elif y > 10:
                text = 'Looking Right'
            elif x < -10:
                text = 'Looking Down'
            elif x > 10:
                text = 'Looking Up'
            else:
                text = 'Forward'

            pose_direction.append(text)
        coordinates = (x, y, z)

        mp_drawing.draw_landmarks(
        image = img,
        landmark_list = face_landmarks,
        connections = mp_face_mesh.FACEMESH_CONTOURS ,
        landmark_drawing_spec = self.drawing_spec,
        connection_drawing_spec = self.drawing_spec
        )

        return pose_direction, nose_3d, nose_2d, rot_vec, trans_vec, cam_matrix, dist_matrix, coordinates
    def drawing(self, img, pose_direction, nose_3d, nose_2d, rot_vec, trans_vec, cam_matrix, dist_matrix, coordinates):
        x, y, z = coordinates
        text = pose_direction[-1]
        # Hiển thị hướng trên mũi
        nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)
        p1 = (int(nose_2d[0]), int(nose_2d[1]))
        p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

        cv2.line(img, p1, p2, (255, 0, 0), 3)

        cv2.putText(img, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        cv2.putText(img, 'x' + str(np.round(x, 2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        cv2.putText(img, 'y' + str(np.round(y, 2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        cv2.putText(img, 'z' + str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        

                


        


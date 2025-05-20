import os
import cv2
import numpy as np
import warnings
from datetime import datetime
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model

warnings.filterwarnings("ignore", category=FutureWarning)

# Try GPU, fallback to CPU
try:
    face_analyzer = FaceAnalysis(name='buffalo_l', providers=['CUDAExecutionProvider'])
    face_analyzer.prepare(ctx_id=0)
except Exception:
    print("⚠️ CUDA not available for FaceAnalysis. Falling back to CPU.")
    face_analyzer = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
    face_analyzer.prepare(ctx_id=0)

try:
    swapper = get_model('model/insightface/inswapper_128.onnx', providers=['CUDAExecutionProvider'])
except Exception:
    print("⚠️ CUDA not available for Swapper. Falling back to CPU.")
    swapper = get_model('inswapper_128.onnx', providers=['CPUExecutionProvider'])

def face_swap(source_img, target_img, anonymize=False, save_faces=False):
    if source_img is None:
        return target_img

    source_img_rgb = cv2.cvtColor(source_img, cv2.COLOR_BGR2RGB)
    target_img_rgb = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)

    # Resize source to target if needed
    if source_img_rgb.shape != target_img_rgb.shape:
        source_img_rgb = cv2.resize(source_img_rgb, (target_img_rgb.shape[1], target_img_rgb.shape[0]))

    src_faces = face_analyzer.get(source_img_rgb)
    tgt_faces = face_analyzer.get(target_img_rgb)

    if len(tgt_faces) == 0 or len(src_faces) == 0:
        return cv2.cvtColor(target_img_rgb, cv2.COLOR_RGB2BGR)

    src_face = src_faces[0]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"saved_faces/{timestamp}"
    if save_faces:
        os.makedirs(output_dir, exist_ok=True)

    for i, tgt_face in enumerate(tgt_faces):
        x1, y1, x2, y2 = tgt_face.bbox.astype(int)

        if anonymize:
            target_img_rgb[y1:y2, x1:x2] = cv2.GaussianBlur(target_img_rgb[y1:y2, x1:x2], (99, 99), 30)
        else:
            try:
                target_img_rgb = swapper.get(target_img_rgb, tgt_face, src_face, paste_back=True)
            except Exception as e:
                print(f"Swapper error on face {i}: {e}")

        if save_faces:
            face_crop = target_img_rgb[y1:y2, x1:x2]
            face_bgr = cv2.cvtColor(face_crop, cv2.COLOR_RGB2BGR)
            cv2.imwrite(f"{output_dir}/swapped_face_{i}.jpg", face_bgr)

            side_by_side = np.hstack([
                cv2.resize(cv2.cvtColor(source_img_rgb, cv2.COLOR_RGB2BGR), (200, 200)),
                cv2.resize(face_bgr, (200, 200))
            ])
            cv2.imwrite(f"{output_dir}/source_target_face_{i}.jpg", side_by_side)

    return cv2.cvtColor(target_img_rgb, cv2.COLOR_RGB2BGR)

import cv2
from rembg import remove
from PIL import Image
import numpy as np
import keras



def process_img(img, size=200, padding=20):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    no_bg = remove(pil_img,)
    no_bg_np = np.array(no_bg)
    alpha = no_bg_np[:, :, 3]
    coords = cv2.findNonZero(alpha)
    if coords is None:
        return None

    x, y, w, h = cv2.boundingRect(coords)

    x1 = max(x - padding, 0)
    y1 = max(y - padding, 0)
    x2 = min(x + w + padding, no_bg_np.shape[1])
    y2 = min(y + h + padding, no_bg_np.shape[0])

    cropped_rgba = no_bg_np[y1:y2, x1:x2]

    alpha_crop = cropped_rgba[:, :, 3] / 255.0
    black_bg = (cropped_rgba[:, :, :3] * alpha_crop[..., None]).astype(np.uint8)

    resized = cv2.resize(black_bg, (size, size), interpolation=cv2.INTER_AREA)
    return resized

def load_model(model_path):
    return keras.models.load_model(model_path, compile=False)

def predict(img, model_path):
    model = load_model(model_path)
    no_background_img = process_img(img)
    result = model.predict(np.expand_dims(no_background_img, axis=0), verbose=0)[0]
    return result
def prediction_with_classes(img, model_path):
    prediction = predict(img, model_path).tolist()
    classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space']
    return dict(zip(classes, prediction))

if __name__ == "__main__":
    pass

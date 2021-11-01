from fastapi import Body, FastAPI, HTTPException

from .core.services.detector import ObjectDetector
from .core.services.encoding import Encoding
from .core.services.image_handler import ImageHandler

app = FastAPI()
detector = ObjectDetector()

@app.post("/predict")
async def predict(b64: str = Body(..., embed=True)):
    img_bytes = Encoding.b64_to_bytes(b64)
    if img_bytes == "":
        raise HTTPException(status_code=400, detail="Payload is not base64-encoded.")

    img = ImageHandler(img_bytes)
    if not img.is_valid():
        raise HTTPException(status_code=400, detail="Payload is not a valid image.")

    resized_img = img.resize()

    result, inference_time = detector.run(Encoding.img_to_bytes(resized_img))
    print(result)

    img_with_boxes = img.draw_boxes(result["detection_boxes"],
                    result["detection_class_entities"],
                    result["detection_scores"])
    final_b64 = Encoding.img_to_b64(img_with_boxes)

    return { "b64" : final_b64, "inference_time" : inference_time }

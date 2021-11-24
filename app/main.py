from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from .core.services.detector import ObjectDetector
from .core.services.encoding import Encoding
from .core.services.image_handler import ImageHandler

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = ObjectDetector()

@app.post("/predict", )
async def predict(
            b64: str = Body(...),
            resize_image: Optional[bool] = Body(True),
            min_score: Optional[float] = Body(0.2)):
    if min_score < 0 or min_score > 0.9:
        raise HTTPException(status_code=400,
                            detail="Minimum score should be between 0 and 0.9 inclusive.")

    img_bytes = Encoding.b64_to_bytes(b64)
    if img_bytes == "":
        raise HTTPException(status_code=400, detail="Payload is not base64-encoded.")

    img_handler = ImageHandler(img_bytes)
    if not img_handler.is_valid():
        raise HTTPException(status_code=400, detail="Payload is not a valid image.")

    if resize_image:
        img = img_handler.resize()
    else:
        img = img_handler.img

    result, inference_time = detector.run(Encoding.img_to_bytes(img))

    img_with_boxes = img_handler.draw_boxes(result["detection_boxes"],
                    result["detection_class_entities"],
                    result["detection_scores"],
                    min_score=min_score)
    final_b64 = Encoding.img_to_b64(img_with_boxes)

    return { "b64" : final_b64, "inference_time" : inference_time }

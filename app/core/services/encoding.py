import base64
import binascii
from io import BytesIO

class Encoding:
    def b64_to_bytes(b64):
        try:
            decoded = base64.b64decode(b64)
            return BytesIO(decoded)
        except binascii.Error:
            return ""

    def img_to_bytes(img):
        bytes_io = BytesIO()
        img.save(bytes_io, format="JPEG")
        return bytes_io.getvalue()

    def img_to_b64(img):
        img_bytes = Encoding.img_to_bytes(img)
        encoded = base64.b64encode(img_bytes)
        return encoded.decode()

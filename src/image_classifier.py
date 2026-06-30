from transformers import AutoImageProcessor
from transformers import AutoModelForImageClassification

from PIL import Image
import torch

MODEL_NAME = "LaurianeMD/vit-skin-disease"

print("Loading skin disease model...")

processor = AutoImageProcessor.from_pretrained(MODEL_NAME)

model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)

print("Model Ready!")

def predict_skin_disease(image):

    image = Image.open(image).convert("RGB")

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():

        outputs = model(**inputs)

    predicted_class = outputs.logits.argmax(-1).item()

    disease = model.config.id2label[predicted_class]

    confidence = torch.softmax(outputs.logits, dim=1)[0][predicted_class].item()

    return disease, confidence
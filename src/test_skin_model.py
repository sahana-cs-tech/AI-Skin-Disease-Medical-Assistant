from transformers import pipeline

print("Loading skin disease model...")

classifier = pipeline(
    "image-classification",
    model="LaurianeMD/vit-skin-disease"
)

print("✅ Model loaded successfully!")
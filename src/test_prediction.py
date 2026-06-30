from image_classifier import predict_skin_disease

image_path = input("Enter image path: ")

disease, confidence = predict_skin_disease(image_path)

print()

print("Prediction:", disease)

print("Confidence:", round(confidence * 100, 2), "%")
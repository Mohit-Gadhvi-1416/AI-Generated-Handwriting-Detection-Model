# evaluate_model.py

import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Define paths
dataset_path = 'C:/Users/mohit/Downloads/handwriting-detection/backend/dataset'  # Update with your path
model_path = 'C:/Users/mohit/Downloads/handwriting-detection/backend/ml_model/model.h5'

# Define directories for AI and human images
ai_dir = os.path.join(dataset_path, 'AI')
human_dir = os.path.join(dataset_path, 'human')

# Define target size (must match the input size your model expects)
target_size = (28, 28)  # Update this size based on your model's input size

# Load the model
model = load_model(model_path)

# Data generators
datagen = ImageDataGenerator(rescale=1./255)

# Create data generators for AI and human
def create_data_generator(directory):
    return datagen.flow_from_directory(
        directory,
        target_size=target_size,
        batch_size=1,
        class_mode=None,  # Only predict the class, no labels
        shuffle=False,  # Don't shuffle, so we get predictions in the same order as input
        color_mode='rgb'  # Ensure color mode matches the model's expectation
    )

# Create data generators
ai_generator = create_data_generator(ai_dir)
human_generator = create_data_generator(human_dir)

# Predict on AI and human images
def predict_images(generator):
    predictions = []
    for _ in range(generator.samples):
        image = generator.next()
        pred = model.predict(image)
        predictions.append(pred[0][0])
    return predictions

ai_predictions = predict_images(ai_generator)
human_predictions = predict_images(human_generator)

# Create labels for predictions
def create_labels(num_samples, label):
    return [label] * num_samples

# Create true labels
true_labels_ai = create_labels(ai_generator.samples, 'AI')
true_labels_human = create_labels(human_generator.samples, 'human')

# Combine predictions and true labels
all_predictions = ai_predictions + human_predictions
all_true_labels = true_labels_ai + true_labels_human

# Threshold for classification
threshold = 0.5  # Update this based on your model's output

# Convert predictions to class labels
predicted_labels = ['AI' if pred > threshold else 'human' for pred in all_predictions]

# Evaluate the model
conf_matrix = confusion_matrix(all_true_labels, predicted_labels, labels=['AI', 'human'])
class_report = classification_report(all_true_labels, predicted_labels, labels=['AI', 'human'])

print('Confusion Matrix:')
print(conf_matrix)
print('\nClassification Report:')
print(class_report)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['AI', 'human'], yticklabels=['AI', 'human'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.datasets import make_classification
import numpy as np

# Generate synthetic data
# Adjusting features to match the CNN input expectations
X_train, y_train = make_classification(n_samples=1000, n_features=28*28, random_state=42)
X_train = X_train.reshape(-1, 28, 28, 1)  # Adjusted to be suitable for a 2D CNN

# Define the model
model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Save the model to 'model.h5'
model.save('model.h5')

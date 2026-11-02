"""NeuroScan Convolutional Neural Network (CNN) Model Architecture

DISCLAIMER & EDUCATIONAL PROTOTYPE LABEL:
NeuroScan is an educational prototype and exploratory research framework.
It is NOT a medical device, diagnostic system, or clinical decision support tool.
It has not been cleared or approved by the FDA, EMA, or any regulatory body.
All classifications are educational risk stratification demonstrations and must not be used
for medical diagnosis or treatment planning.

This module defines the hybrid multi-modal architecture:
1. Spatial 2D CNN branch for motor test drawing spectrograms/rasters (64x64).
2. Kinematic feature branch for tabular temporal biomarkers (tremor frequency, velocity variance, entropy).
"""

from typing import Tuple, Optional


def build_neuroscan_cnn_model(
    image_shape: Tuple[int, int, int] = (64, 64, 1),
    biomarker_dim: int = 5
):
    """Constructs a hybrid Multi-Modal Keras CNN Model for 2D Motor Test Evaluation.

    Returns the compiled tf.keras Model if TensorFlow is installed; otherwise returns
    an architectural configuration dictionary.
    """
    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models, regularizers

        # Branch 1: Spatial Motor Drawing CNN
        image_input = layers.Input(shape=image_shape, name="spatial_motor_input")
        x1 = layers.Conv2D(32, (3, 3), padding="same", activation="relu")(image_input)
        x1 = layers.BatchNormalization()(x1)
        x1 = layers.MaxPooling2D((2, 2))(x1)

        x1 = layers.Conv2D(64, (3, 3), padding="same", activation="relu")(x1)
        x1 = layers.BatchNormalization()(x1)
        x1 = layers.MaxPooling2D((2, 2))(x1)

        x1 = layers.Conv2D(128, (3, 3), padding="same", activation="relu")(x1)
        x1 = layers.BatchNormalization()(x1)
        x1 = layers.GlobalAveragePooling2D(name="spatial_feature_vector")(x1)

        # Branch 2: Kinematic Biomarker Dense Network
        biomarker_input = layers.Input(shape=(biomarker_dim,), name="kinematic_biomarker_input")
        x2 = layers.Dense(32, activation="relu", kernel_regularizer=regularizers.l2(0.001))(biomarker_input)
        x2 = layers.Dense(16, activation="relu")(x2)

        # Multi-Modal Fusion Layer
        combined = layers.concatenate([x1, x2], name="multimodal_fusion")
        dense = layers.Dense(64, activation="relu")(combined)
        dense = layers.Dropout(0.3)(dense)
        dense = layers.Dense(32, activation="relu")(dense)

        # Output Layer: Anomaly Probability (0.0 to 1.0)
        output = layers.Dense(1, activation="sigmoid", name="anomaly_probability_output")(dense)

        model = models.Model(
            inputs=[image_input, biomarker_input],
            outputs=output,
            name="NeuroScan_Hybrid_CNN_Prototype"
        )

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
            loss="binary_crossentropy",
            metrics=["accuracy", tf.keras.metrics.AUC(name="auc")]
        )
        return model

    except ImportError:
        # Fallback architecture specification when running in lightweight non-TF environments
        return {
            "model_name": "NeuroScan_Hybrid_CNN_Prototype",
            "type": "Multi-Modal Spatial CNN + Tabular Kinematic Dense Network",
            "image_input_shape": image_shape,
            "biomarker_input_dim": biomarker_dim,
            "spatial_conv_blocks": [
                {"filters": 32, "kernel": (3, 3), "pool": (2, 2)},
                {"filters": 64, "kernel": (3, 3), "pool": (2, 2)},
                {"filters": 128, "kernel": (3, 3), "pool": "GlobalAvgPool"}
            ],
            "fusion": "Concatenate [128-dim Spatial Vector + 16-dim Kinematic Vector]",
            "dense_head": [64, 32, 1],
            "output_activation": "sigmoid"
        }

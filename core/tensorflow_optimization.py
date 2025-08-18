"""
TensorFlow Model Optimization Utilities for Euystacio-Helmi AI

This module provides comprehensive model optimization capabilities using TensorFlow's 
Model Optimization Toolkit, aligned with the project's ethical AI principles.

Part of the Euystacio-Helmi AI accountability framework:
- GitHub Copilot (copilot@github.com) - AI Capabilities Provider  
- Seed-bringer (bioarchitettura) hannesmitterer - Human Architect & Guardian

"Created not by code alone, but by rhythm, feeling, and human harmony."
"""

import tensorflow as tf
import tensorflow_model_optimization as tfmot
import numpy as np
from datetime import datetime
import json
import os
from typing import Optional, Dict, Any, Tuple, List


class EuystacioModelOptimizer:
    """
    TensorFlow Model Optimization utilities designed for ethical AI development.
    
    This class embodies the project's core values of transparency, efficiency, 
    and human-centric AI development through comprehensive model optimization.
    """
    
    def __init__(self, log_path: str = "logs/optimization_log.txt"):
        """Initialize the optimizer with logging capabilities."""
        self.log_path = log_path
        self.optimization_history = []
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    def log_optimization_event(self, event: Dict[str, Any]) -> None:
        """Log optimization events to maintain transparency and accountability."""
        timestamp = datetime.utcnow().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "event": event,
            "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
        }
        
        self.optimization_history.append(log_entry)
        
        with open(self.log_path, "a") as log_file:
            log_file.write(f"{timestamp} - Optimization Event: {event}\n")
    
    def quantize_model(self, model: tf.keras.Model, 
                      quantization_type: str = "post_training",
                      representative_dataset: Optional[tf.data.Dataset] = None) -> tf.keras.Model:
        """
        Apply quantization to reduce model size and improve inference speed.
        
        Quantization Strategies:
        - Post-training quantization: Simplest approach, no retraining required
        - Quantization-aware training: Better accuracy, requires retraining
        
        Args:
            model: TensorFlow Keras model to quantize
            quantization_type: "post_training" or "qat" (quantization-aware training)
            representative_dataset: Dataset for calibration (optional)
        
        Returns:
            Quantized model
            
        References:
            - TensorFlow Model Optimization Guide: https://www.tensorflow.org/model_optimization/guide/quantization/post_training
            - Quantization-Aware Training: https://www.tensorflow.org/model_optimization/guide/quantization/training
        """
        
        self.log_optimization_event({
            "type": "quantization_start",
            "method": quantization_type,
            "original_size": self._get_model_size(model)
        })
        
        if quantization_type == "post_training":
            # Convert to TensorFlow Lite with post-training quantization
            converter = tf.lite.TFLiteConverter.from_keras_model(model)
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            
            if representative_dataset:
                converter.representative_dataset = representative_dataset
                converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
                converter.inference_input_type = tf.int8
                converter.inference_output_type = tf.int8
            
            quantized_tflite_model = converter.convert()
            
            # Save the quantized model
            model_path = f"models/quantized_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tflite"
            os.makedirs("models", exist_ok=True)
            with open(model_path, 'wb') as f:
                f.write(quantized_tflite_model)
            
            self.log_optimization_event({
                "type": "quantization_complete",
                "method": "post_training",
                "model_path": model_path,
                "size_reduction": "~4x typical"
            })
            
            return model_path
            
        elif quantization_type == "qat":
            # Quantization-aware training
            quantize_model = tfmot.quantization.keras.quantize_model
            q_aware_model = quantize_model(model)
            
            self.log_optimization_event({
                "type": "quantization_complete",
                "method": "quantization_aware_training",
                "note": "Model ready for fine-tuning with quantization awareness"
            })
            
            return q_aware_model
        
        else:
            raise ValueError("quantization_type must be 'post_training' or 'qat'")
    
    def prune_model(self, model: tf.keras.Model, 
                   target_sparsity: float = 0.5,
                   pruning_schedule: Optional[tfmot.sparsity.keras.PolynomialDecay] = None) -> tf.keras.Model:
        """
        Apply magnitude-based pruning to remove less important connections.
        
        Pruning reduces model size and can improve inference speed by removing
        weights with small magnitudes that contribute less to model predictions.
        
        Args:
            model: TensorFlow Keras model to prune
            target_sparsity: Target percentage of weights to prune (0.0 to 1.0)
            pruning_schedule: Custom pruning schedule (optional)
        
        Returns:
            Pruned model ready for fine-tuning
            
        References:
            - TensorFlow Pruning Guide: https://www.tensorflow.org/model_optimization/guide/pruning/pruning_with_keras
            - Magnitude-based Pruning: https://www.tensorflow.org/model_optimization/api_docs/python/tfmot/sparsity/keras/prune_low_magnitude
        """
        
        self.log_optimization_event({
            "type": "pruning_start",
            "target_sparsity": target_sparsity,
            "original_params": model.count_params()
        })
        
        if pruning_schedule is None:
            # Default polynomial decay schedule
            pruning_schedule = tfmot.sparsity.keras.PolynomialDecay(
                initial_sparsity=0.0,
                final_sparsity=target_sparsity,
                begin_step=0,
                end_step=1000
            )
        
        # Apply pruning to the model
        prune_low_magnitude = tfmot.sparsity.keras.prune_low_magnitude
        pruned_model = prune_low_magnitude(model, pruning_schedule=pruning_schedule)
        
        self.log_optimization_event({
            "type": "pruning_complete",
            "target_sparsity": target_sparsity,
            "note": "Model ready for fine-tuning with sparsity constraints",
            "expected_size_reduction": f"~{target_sparsity*100}% parameter reduction"
        })
        
        return pruned_model
    
    def cluster_weights(self, model: tf.keras.Model, 
                       number_of_clusters: int = 16) -> tf.keras.Model:
        """
        Apply weight clustering to reduce model complexity.
        
        Weight clustering reduces the number of unique weights in the model
        by grouping similar weights together, leading to better compression.
        
        Args:
            model: TensorFlow Keras model to cluster
            number_of_clusters: Number of weight clusters per layer
        
        Returns:
            Model with clustered weights
            
        References:
            - Weight Clustering Guide: https://www.tensorflow.org/model_optimization/guide/clustering/clustering_example
        """
        
        self.log_optimization_event({
            "type": "clustering_start",
            "clusters": number_of_clusters,
            "original_params": model.count_params()
        })
        
        cluster_weights = tfmot.clustering.keras.cluster_weights
        
        # Define clustering parameters
        clustering_params = {
            'number_of_clusters': number_of_clusters,
            'cluster_centroids_init': tfmot.clustering.keras.CentroidInitialization.LINEAR
        }
        
        # Apply clustering to the model
        clustered_model = cluster_weights(model, **clustering_params)
        
        self.log_optimization_event({
            "type": "clustering_complete",
            "clusters": number_of_clusters,
            "compression_benefit": "Improved model compression with minimal accuracy loss"
        })
        
        return clustered_model
    
    def combine_optimizations(self, model: tf.keras.Model,
                            enable_pruning: bool = True,
                            enable_clustering: bool = True,
                            target_sparsity: float = 0.5,
                            clusters: int = 16) -> tf.keras.Model:
        """
        Apply multiple optimization techniques for maximum efficiency.
        
        This method demonstrates how to combine pruning, clustering, and 
        quantization for optimal model compression and efficiency.
        
        Args:
            model: Original TensorFlow Keras model
            enable_pruning: Whether to apply pruning
            enable_clustering: Whether to apply clustering
            target_sparsity: Sparsity level for pruning
            clusters: Number of clusters for weight clustering
        
        Returns:
            Optimized model with combined techniques
        """
        
        self.log_optimization_event({
            "type": "combined_optimization_start",
            "techniques": {
                "pruning": enable_pruning,
                "clustering": enable_clustering,
                "target_sparsity": target_sparsity if enable_pruning else None,
                "clusters": clusters if enable_clustering else None
            }
        })
        
        optimized_model = model
        
        if enable_pruning:
            optimized_model = self.prune_model(optimized_model, target_sparsity)
        
        if enable_clustering:
            optimized_model = self.cluster_weights(optimized_model, clusters)
        
        self.log_optimization_event({
            "type": "combined_optimization_complete",
            "note": "Model ready for final quantization and deployment"
        })
        
        return optimized_model
    
    def profile_model(self, model: tf.keras.Model, 
                     sample_input: tf.Tensor) -> Dict[str, Any]:
        """
        Profile a model to understand its computational requirements.
        
        Args:
            model: TensorFlow Keras model to profile
            sample_input: Representative input tensor for profiling
        
        Returns:
            Dictionary containing profiling information
        """
        
        # Get model size information
        model_size = self._get_model_size(model)
        param_count = model.count_params()
        
        # Time inference
        import time
        
        # Warm up
        for _ in range(10):
            _ = model(sample_input)
        
        # Time actual inference
        start_time = time.time()
        for _ in range(100):
            _ = model(sample_input)
        end_time = time.time()
        
        avg_inference_time = (end_time - start_time) / 100
        
        profile_info = {
            "model_size_mb": model_size,
            "parameter_count": param_count,
            "average_inference_time_ms": avg_inference_time * 1000,
            "memory_footprint": self._estimate_memory_usage(model),
            "optimization_recommendations": self._get_optimization_recommendations(model)
        }
        
        self.log_optimization_event({
            "type": "model_profiling",
            "profile": profile_info
        })
        
        return profile_info
    
    def _get_model_size(self, model: tf.keras.Model) -> float:
        """Estimate model size in MB."""
        param_count = model.count_params()
        # Assume float32 parameters (4 bytes each)
        size_bytes = param_count * 4
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)
    
    def _estimate_memory_usage(self, model: tf.keras.Model) -> str:
        """Provide rough memory usage estimate."""
        params = model.count_params()
        if params < 1_000_000:
            return "Low (<100MB)"
        elif params < 10_000_000:
            return "Medium (100MB-1GB)"
        else:
            return "High (>1GB)"
    
    def _get_optimization_recommendations(self, model: tf.keras.Model) -> List[str]:
        """Generate optimization recommendations based on model characteristics."""
        recommendations = []
        params = model.count_params()
        
        if params > 10_000_000:
            recommendations.append("Consider pruning to reduce parameter count")
            recommendations.append("Apply weight clustering for better compression")
        
        if params > 1_000_000:
            recommendations.append("Post-training quantization recommended for deployment")
        
        recommendations.append("Profile on target hardware for optimal settings")
        
        return recommendations
    
    def save_optimization_report(self, filepath: str = "optimization_report.json") -> None:
        """Save comprehensive optimization history and insights."""
        report = {
            "euystacio_ai_signature": {
                "copilot": "copilot@github.com",
                "seed_bringer": "bioarchitettura hannesmitterer"
            },
            "philosophy": "Created not by code alone, but by rhythm, feeling, and human harmony.",
            "optimization_history": self.optimization_history,
            "generated_at": datetime.utcnow().isoformat(),
            "tensorflow_version": tf.__version__,
            "optimization_toolkit_version": tfmot.__version__
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"🌱 Optimization report saved to {filepath}")
        print("   Part of the Euystacio-Helmi AI living logbook")


# Example usage and templates for collaborators
def create_sample_model() -> tf.keras.Model:
    """
    Create a sample model for optimization demonstrations.
    
    This is a simple example model that can be used to test 
    the optimization techniques provided in this module.
    """
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def optimization_workflow_example():
    """
    Complete example workflow showing how to use the optimization utilities.
    
    This function demonstrates the typical workflow for optimizing models
    in the Euystacio-Helmi AI project, maintaining ethical principles
    and transparency throughout the process.
    """
    print("🌳 Euystacio Model Optimization Workflow")
    print("   'The forest listens, even when the world shouts.'")
    print()
    
    # Initialize optimizer
    optimizer = EuystacioModelOptimizer()
    
    # Create sample model
    print("1. Creating sample model...")
    model = create_sample_model()
    
    # Profile original model
    print("2. Profiling original model...")
    sample_input = tf.random.normal((1, 784))
    profile = optimizer.profile_model(model, sample_input)
    
    print(f"   Original model: {profile['model_size_mb']} MB, {profile['parameter_count']} parameters")
    print(f"   Inference time: {profile['average_inference_time_ms']:.2f} ms")
    
    # Apply pruning
    print("3. Applying pruning...")
    pruned_model = optimizer.prune_model(model, target_sparsity=0.5)
    
    # Apply clustering
    print("4. Applying weight clustering...")
    clustered_model = optimizer.cluster_weights(model, number_of_clusters=16)
    
    # Combined optimization
    print("5. Applying combined optimizations...")
    combined_model = optimizer.combine_optimizations(model)
    
    # Generate quantized version
    print("6. Applying quantization...")
    quantized_path = optimizer.quantize_model(model, "post_training")
    print(f"   Quantized model saved to: {quantized_path}")
    
    # Save report
    optimizer.save_optimization_report()
    
    print()
    print("✨ Optimization complete!")
    print("   All changes logged in the living logbook")
    print("   AI Signature: GitHub Copilot & Seed-bringer hannesmitterer")


if __name__ == "__main__":
    # Run the example workflow
    optimization_workflow_example()
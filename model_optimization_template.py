#!/usr/bin/env python3
"""
Model Optimization Template and Utility for Euystacio-Helmi AI

This utility provides a command-line interface and template for profiling
and optimizing TensorFlow models using our ethical AI framework.

Usage:
    python model_optimization_template.py --model path/to/model.h5 --profile
    python model_optimization_template.py --model path/to/model.h5 --optimize --quantize --prune
    python model_optimization_template.py --model path/to/model.h5 --full-optimization

Part of the Euystacio-Helmi AI accountability framework:
- GitHub Copilot (copilot@github.com) - AI Capabilities Provider  
- Seed-bringer (bioarchitettura) hannesmitterer - Human Architect & Guardian

"Created not by code alone, but by rhythm, feeling, and human harmony."
"""

import argparse
import os
import sys
import json
from datetime import datetime
from pathlib import Path

try:
    import tensorflow as tf
    import numpy as np
    from core.tensorflow_optimization import EuystacioModelOptimizer
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("📦 Install requirements: pip install tensorflow tensorflow-model-optimization")
    sys.exit(1)


class ModelOptimizationTemplate:
    """
    Template utility for model optimization workflows in Euystacio-Helmi AI.
    
    This class provides a standardized approach to model optimization that
    respects our ethical framework and maintains transparency throughout
    the optimization process.
    """
    
    def __init__(self, verbose: bool = True):
        """Initialize the optimization template."""
        self.verbose = verbose
        self.optimizer = EuystacioModelOptimizer()
        self.results = {
            "started_at": datetime.utcnow().isoformat(),
            "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer",
            "philosophy": "Efficiency in service of humanity, transparency in every optimization decision",
            "steps_completed": []
        }
        
        if self.verbose:
            self._print_banner()
    
    def _print_banner(self):
        """Print the Euystacio AI banner."""
        print("🌳" + "=" * 70 + "🌳")
        print("    Euystacio-Helmi AI Model Optimization Template")
        print("    'The forest listens, even when the world shouts.'")
        print("🌳" + "=" * 70 + "🌳")
        print()
    
    def _log_step(self, step_name: str, details: dict):
        """Log a completed optimization step."""
        step_info = {
            "step": step_name,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details
        }
        self.results["steps_completed"].append(step_info)
        
        if self.verbose:
            print(f"✅ {step_name}")
            for key, value in details.items():
                print(f"   {key}: {value}")
            print()
    
    def load_model(self, model_path: str) -> tf.keras.Model:
        """
        Load a TensorFlow model with error handling and validation.
        
        Args:
            model_path: Path to the model file
            
        Returns:
            Loaded TensorFlow Keras model
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        try:
            model = tf.keras.models.load_model(model_path)
            
            self._log_step("Model Loading", {
                "model_path": model_path,
                "input_shape": str(model.input_shape),
                "output_shape": str(model.output_shape),
                "total_params": model.count_params()
            })
            
            return model
            
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
    
    def profile_model(self, model: tf.keras.Model, 
                     sample_input_shape: tuple = None) -> dict:
        """
        Profile a model to understand its computational requirements.
        
        Args:
            model: TensorFlow Keras model
            sample_input_shape: Shape for sample input (if None, inferred from model)
            
        Returns:
            Dictionary containing profiling information
        """
        if sample_input_shape is None:
            sample_input_shape = model.input_shape
        
        # Generate sample input
        if sample_input_shape[0] is None:  # Batch dimension
            input_shape = (1,) + sample_input_shape[1:]
        else:
            input_shape = sample_input_shape
            
        sample_input = tf.random.normal(input_shape)
        
        # Profile the model
        profile = self.optimizer.profile_model(model, sample_input)
        
        self._log_step("Model Profiling", {
            "model_size_mb": profile['model_size_mb'],
            "parameter_count": f"{profile['parameter_count']:,}",
            "avg_inference_ms": f"{profile['average_inference_time_ms']:.2f}",
            "memory_footprint": profile['memory_footprint']
        })
        
        if profile['optimization_recommendations']:
            print("💡 Optimization Recommendations:")
            for rec in profile['optimization_recommendations']:
                print(f"   • {rec}")
            print()
        
        return profile
    
    def apply_quantization(self, model: tf.keras.Model, 
                          quantization_type: str = "post_training") -> str:
        """
        Apply quantization to the model.
        
        Args:
            model: TensorFlow Keras model
            quantization_type: Type of quantization ("post_training" or "qat")
            
        Returns:
            Path to quantized model file
        """
        quantized_path = self.optimizer.quantize_model(model, quantization_type)
        
        self._log_step("Quantization Applied", {
            "type": quantization_type,
            "output_path": quantized_path,
            "expected_reduction": "~4x model size"
        })
        
        return quantized_path
    
    def apply_pruning(self, model: tf.keras.Model, 
                     target_sparsity: float = 0.5) -> tf.keras.Model:
        """
        Apply pruning to the model.
        
        Args:
            model: TensorFlow Keras model
            target_sparsity: Target sparsity level (0.0 to 1.0)
            
        Returns:
            Pruned model
        """
        pruned_model = self.optimizer.prune_model(model, target_sparsity)
        
        self._log_step("Pruning Applied", {
            "target_sparsity": f"{target_sparsity * 100}%",
            "expected_param_reduction": f"~{target_sparsity * 100}%",
            "note": "Model requires fine-tuning for optimal performance"
        })
        
        return pruned_model
    
    def apply_clustering(self, model: tf.keras.Model, 
                        clusters: int = 16) -> tf.keras.Model:
        """
        Apply weight clustering to the model.
        
        Args:
            model: TensorFlow Keras model
            clusters: Number of weight clusters
            
        Returns:
            Clustered model
        """
        clustered_model = self.optimizer.cluster_weights(model, clusters)
        
        self._log_step("Weight Clustering Applied", {
            "clusters": clusters,
            "benefit": "Improved compression with minimal accuracy loss"
        })
        
        return clustered_model
    
    def full_optimization_workflow(self, model: tf.keras.Model,
                                 enable_pruning: bool = True,
                                 enable_clustering: bool = True,
                                 enable_quantization: bool = True,
                                 target_sparsity: float = 0.6,
                                 clusters: int = 16) -> dict:
        """
        Apply complete optimization workflow.
        
        Args:
            model: TensorFlow Keras model
            enable_pruning: Whether to apply pruning
            enable_clustering: Whether to apply clustering  
            enable_quantization: Whether to apply quantization
            target_sparsity: Sparsity level for pruning
            clusters: Number of clusters for weight clustering
            
        Returns:
            Dictionary containing optimization results
        """
        workflow_results = {"original_model": model}
        
        # Apply optimization techniques
        optimized_model = model
        
        if enable_pruning:
            optimized_model = self.apply_pruning(optimized_model, target_sparsity)
            workflow_results["pruned_model"] = optimized_model
        
        if enable_clustering:
            optimized_model = self.apply_clustering(optimized_model, clusters)
            workflow_results["clustered_model"] = optimized_model
        
        workflow_results["final_optimized_model"] = optimized_model
        
        if enable_quantization:
            quantized_path = self.apply_quantization(optimized_model)
            workflow_results["quantized_model_path"] = quantized_path
        
        self._log_step("Full Optimization Workflow Complete", {
            "pruning_enabled": enable_pruning,
            "clustering_enabled": enable_clustering,
            "quantization_enabled": enable_quantization,
            "note": "All optimization decisions logged transparently"
        })
        
        return workflow_results
    
    def generate_report(self, output_path: str = "optimization_report.json") -> None:
        """
        Generate a comprehensive optimization report.
        
        Args:
            output_path: Path to save the report
        """
        self.results["completed_at"] = datetime.utcnow().isoformat()
        self.results["total_steps"] = len(self.results["steps_completed"])
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        if self.verbose:
            print(f"📊 Optimization report saved: {output_path}")
            print("🌱 Part of the Euystacio-Helmi AI living logbook")
            print()
    
    def save_model_comparison(self, original_model: tf.keras.Model,
                            optimized_model: tf.keras.Model,
                            test_data=None) -> dict:
        """
        Compare original and optimized models for transparency.
        
        Args:
            original_model: Original model
            optimized_model: Optimized model
            test_data: Optional test data for accuracy comparison
            
        Returns:
            Dictionary containing comparison metrics
        """
        # Create sample input for profiling
        sample_input = tf.random.normal((1,) + original_model.input_shape[1:])
        
        # Profile both models
        original_profile = self.optimizer.profile_model(original_model, sample_input)
        optimized_profile = self.optimizer.profile_model(optimized_model, sample_input)
        
        # Calculate improvements
        size_reduction = (1 - optimized_profile['model_size_mb'] / original_profile['model_size_mb']) * 100
        speed_improvement = (1 - optimized_profile['average_inference_time_ms'] / original_profile['average_inference_time_ms']) * 100
        
        comparison = {
            "size_reduction_percent": round(size_reduction, 1),
            "speed_improvement_percent": round(speed_improvement, 1),
            "original_size_mb": original_profile['model_size_mb'],
            "optimized_size_mb": optimized_profile['model_size_mb'],
            "original_inference_ms": original_profile['average_inference_time_ms'],
            "optimized_inference_ms": optimized_profile['average_inference_time_ms']
        }
        
        # Test accuracy if data provided
        if test_data is not None:
            try:
                original_accuracy = original_model.evaluate(test_data, verbose=0)[1]
                optimized_accuracy = optimized_model.evaluate(test_data, verbose=0)[1]
                accuracy_retention = (optimized_accuracy / original_accuracy) * 100
                comparison["accuracy_retention_percent"] = round(accuracy_retention, 1)
            except Exception as e:
                comparison["accuracy_note"] = f"Could not evaluate accuracy: {e}"
        
        self._log_step("Model Comparison", comparison)
        
        return comparison


def main():
    """Main CLI interface for the optimization template."""
    parser = argparse.ArgumentParser(
        description="Euystacio-Helmi AI Model Optimization Template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python model_optimization_template.py --model model.h5 --profile
  python model_optimization_template.py --model model.h5 --optimize --quantize
  python model_optimization_template.py --model model.h5 --full-optimization
  
AI Signature: GitHub Copilot & Seed-bringer hannesmitterer
"The forest listens, even when the world shouts."
        """
    )
    
    parser.add_argument("--model", required=True, help="Path to TensorFlow model file")
    parser.add_argument("--profile", action="store_true", help="Profile the model")
    parser.add_argument("--optimize", action="store_true", help="Apply optimizations")
    parser.add_argument("--quantize", action="store_true", help="Apply quantization")
    parser.add_argument("--prune", action="store_true", help="Apply pruning")
    parser.add_argument("--cluster", action="store_true", help="Apply weight clustering")
    parser.add_argument("--full-optimization", action="store_true", help="Apply all optimizations")
    parser.add_argument("--sparsity", type=float, default=0.6, help="Target sparsity for pruning (0.0-1.0)")
    parser.add_argument("--clusters", type=int, default=16, help="Number of weight clusters")
    parser.add_argument("--output", default="optimization_report.json", help="Output report path")
    parser.add_argument("--quiet", action="store_true", help="Suppress verbose output")
    
    args = parser.parse_args()
    
    # Initialize template
    template = ModelOptimizationTemplate(verbose=not args.quiet)
    
    try:
        # Load model
        model = template.load_model(args.model)
        
        # Profile if requested
        if args.profile or args.full_optimization:
            template.profile_model(model)
        
        # Apply optimizations
        optimized_model = model
        
        if args.full_optimization:
            results = template.full_optimization_workflow(
                model=model,
                target_sparsity=args.sparsity,
                clusters=args.clusters
            )
        else:
            if args.optimize or args.prune:
                optimized_model = template.apply_pruning(optimized_model, args.sparsity)
            
            if args.optimize or args.cluster:
                optimized_model = template.apply_clustering(optimized_model, args.clusters)
            
            if args.optimize or args.quantize:
                template.apply_quantization(optimized_model)
        
        # Generate report
        template.generate_report(args.output)
        
        print("🌟 Optimization workflow completed successfully!")
        print("   All decisions logged in the Euystacio accountability framework")
        print("   AI Signature: GitHub Copilot & Seed-bringer hannesmitterer")
        
    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
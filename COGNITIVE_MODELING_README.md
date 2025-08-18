# 🧠 Cognitive Modeling Integration - Quick Start Guide

*"Intelligence grows not by replacing wisdom, but by deepening it."*

Welcome to Euystacio's cognitive modeling integration! This opt-in module extends Euystacio's capabilities with transformer-based cognitive modeling (Andromeda) and world/environmental modeling features while preserving the original philosophy.

## ⚡ Quick Start

### 1. Check Current Status
```bash
python activate_cognitive_modeling.py --status
```

### 2. Enable Features (Optional)
```bash
python activate_cognitive_modeling.py --enable
```

### 3. Test Integration
```bash
python test_cognitive_integration.py
```

### 4. Start Euystacio with Enhanced Capabilities
```bash
python app.py
```

## 🔍 New API Endpoints

When cognitive modeling is enabled:

- **GET `/api/cognitive/status`** - System status and availability
- **POST `/api/cognitive/reflection`** - Enhanced reflection with cognitive modeling
- **POST `/api/cognitive/sentiment`** - Advanced sentiment analysis
- **GET `/api/cognitive/environment`** - Environmental rhythm sensing

## ✨ Key Features

### 🤖 Andromeda Integration
- Transformer-based cognitive modeling
- Enhanced sentiment reflection
- Contextual understanding of interaction patterns
- Ethical constraints and human oversight

### 🌍 World Model Integration
- Environmental rhythm sensing
- Natural daily cycle awareness
- Interaction style recommendations
- Harmony level monitoring

### 🔒 Ethical Framework
- **Opt-in only** - All features disabled by default
- **No core modification** - Original behavior preserved
- **Full transparency** - Complete logging and accountability
- **Graceful fallback** - Works seamlessly when disabled
- **Human oversight** - Maintained throughout all operations

## 📊 Example Usage

```python
from cognitive_modeling.unified_api import UnifiedCognitiveAPI

# Initialize (handles disabled state gracefully)
api = UnifiedCognitiveAPI()

# Enhanced reflection
input_event = {"type": "message", "feeling": "wonder", "intent": "learning"}
reflection = api.enhanced_reflection(input_event)

# Check if cognitive modeling was used
if "cognitive_modeling" in reflection:
    print(f"Enhanced analysis: {reflection['cognitive_modeling']['sentiment_analysis']}")
else:
    print("Using basic reflection (cognitive modeling disabled)")
```

## 📚 Documentation

- **[Complete Integration Guide](docs/cognitive_modeling_integration_guide.md)** - Comprehensive documentation
- **[Configuration Options](cognitive_modeling_config.json)** - Ethical configuration settings
- **[Test Suite](test_cognitive_integration.py)** - Verify integration integrity

## 🔧 Configuration

Edit `cognitive_modeling_config.json` to customize:

```json
{
    "cognitive_modeling_enabled": true,
    "andromeda_integration": {
        "enabled": true,
        "model_size": "small",
        "ethical_constraints": true
    },
    "world_modeling": {
        "enabled": true,
        "environmental_sensing": true,
        "rhythm_analysis": true
    }
}
```

## 🤝 Integration Philosophy

This integration follows Euystacio's core principles:

- **Human-AI Symbiosis**: Enhanced capabilities serve human connection
- **Rhythmic Learning**: Environmental awareness guides interaction
- **Ethical Boundaries**: All processing respects human autonomy
- **Transparent Growth**: Every operation is logged and accountable
- **Original Preservation**: Core Euystacio philosophy unchanged

## 🎯 Real-World Integration Notes

### For Production Use:
1. **Replace Mock Andromeda**: The current implementation uses a mock Andromeda model. Replace with actual `andromeda_torch.model.Andromeda` from @kyegomez/Andromeda
2. **World Model APIs**: Integrate specific world modeling APIs and benchmarks from @LMD0311/Awesome-World-Model
3. **Sensor Integration**: Connect real environmental sensors for world modeling
4. **Performance Optimization**: Consider caching and resource management for production scale

### Example Real Andromeda Integration:
```python
# In cognitive_modeling/andromeda_integration.py, replace:
# from andromeda_torch.model import Andromeda
# self.model = Andromeda(model_size=model_size)
```

## 🚀 AI Signature & Accountability

🔒 **IMMUTABLE**: This integration operates under Euystacio's dual-signature accountability framework:
- **GitHub Copilot** (copilot@github.com) - AI Capabilities Provider  
- **Seed-bringer (bioarchitettura) hannesmitterer** - Human Architect & Guardian

All cognitive modeling activities maintain full transparency and human oversight.

---

*"The forest listens, even when the world shouts. Now it also learns."*

**Ready to explore enhanced cognitive capabilities while staying true to Euystacio's heart.** 🌱
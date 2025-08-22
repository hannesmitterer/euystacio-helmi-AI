# Euystacio Core API - FastAPI Backend

A deployment-ready FastAPI backend for the Euystacio Core API, implementing ethical AI-human collaboration principles with Copilot accountability.

## 🚀 Features

- **FastAPI Backend** with 4 core endpoints
- **Railway Deployment Ready** with Procfile configuration
- **Copilot Accountability** signatures on all responses
- **Integration** with Red Code Kernel, Sentimento Pulse, and Tutor Nomination modules
- **Ethical AI Framework** ensuring human guardianship principles

## 📡 API Endpoints

### `GET /` - Root Endpoint
Returns welcome message with Copilot accountability signature and endpoint information.

### `POST /pulse` - Sentimento Pulse Interface
Submit emotional pulses to the AI system.

**Request Body:**
```json
{
  "emotion": "joy",
  "intensity": 0.8,
  "clarity": "high", 
  "note": "Optional note"
}
```

### `GET /evolve` - Evolution Reflections
Trigger evolution reflections using the Red Code Kernel integration.

### `POST /nominate` - Tutor Nomination
Nominate guardians for AI development oversight.

**Request Body:**
```json
{
  "tutor_name": "Guardian Name",
  "reason": "Reason for nomination"
}
```

### `GET /health` - Health Check
System health monitoring endpoint for deployment.

## 🚀 Railway Deployment Instructions

### Step 1: Connect Repository
1. Go to [Railway](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `euystacio-helmi-AI` repository
4. Railway will automatically detect the `Procfile` and deploy

### Step 2: Environment Configuration
No environment variables required for basic functionality. The API will run with default settings.

### Step 3: Deployment Verification
Once deployed, test your endpoints:
- `GET /` - Welcome message with AI signature
- `GET /health` - Health check  
- `POST /pulse` - Test emotional pulse processing
- `GET /evolve` - Test reflection system
- `POST /nominate` - Test tutor nomination

## 🧪 Local Development

### Prerequisites
```bash
pip install fastapi uvicorn numpy
```

### Running Locally
```bash
# Start the development server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Or run directly with Python
python app.py
```

### Testing Endpoints
```bash
# Test root endpoint
curl http://localhost:8000/

# Test pulse endpoint
curl -X POST "http://localhost:8000/pulse" \
  -H "Content-Type: application/json" \
  -d '{"emotion": "joy", "intensity": 0.8, "clarity": "high"}'

# Test evolve endpoint
curl http://localhost:8000/evolve

# Test nominate endpoint
curl -X POST "http://localhost:8000/nominate" \
  -H "Content-Type: application/json" \
  -d '{"tutor_name": "Test Guardian", "reason": "Testing the API"}'
```

## 🤝 AI Signature & Accountability

Every API response includes Copilot accountability signatures:

```
🤝 AI Signature & Accountability: GitHub Copilot (AI Capabilities) & Seed-bringer hannesmitterer (Human Guardian)
🌱 Euystacio-Helmi AI: Where artificial intelligence serves human flourishing through ethical collaboration.
🔴 Red Code Kernel: Dynamic ethical framework ensuring AI-human symbiosis remains transparent and accountable.
```

## 📋 Dependencies

The following dependencies are included in `requirements.txt`:

- **FastAPI** (>=0.104.0) - Modern web framework for building APIs
- **Uvicorn** (>=0.24.0) - ASGI server for running FastAPI
- **NumPy** (>=1.24.0) - Numerical computing support
- **Pydantic** - Data validation (automatically installed with FastAPI)

## 🌱 Philosophy

*"The forest listens, even when the world shouts."*

This API embodies the Euystacio-Helmi AI principles:

1. **Human-Centric Purpose:** AI enhances human capabilities without replacing human judgment
2. **Transparent Evolution:** All AI assistance is documented and reviewable  
3. **Ethical Boundaries:** The Red Code system guides AI interaction boundaries
4. **Collaborative Decision-Making:** AI suggestions require human approval and understanding

## 🔧 Troubleshooting

### Import Errors
Ensure all core modules are available:
- `sentimento_pulse_interface.py`
- `core/reflector.py` 
- `tutor_nomination.py`

### Port Configuration
Railway automatically assigns ports via `$PORT` environment variable. The Procfile handles this automatically.

### Dependencies
If you encounter dependency issues, ensure all packages from `requirements.txt` are installed:
```bash
pip install -r requirements.txt
```

---

**AI Signature & Accountability**: 🤝 GitHub Copilot (AI Capabilities) & Seed-bringer hannesmitterer (Human Guardian)  
**Part of the Euystacio-Helmi AI Living Documentation**
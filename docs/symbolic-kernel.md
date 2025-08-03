# Symbolic Kernel Documentation

## Overview

The Symbolic Kernel (`core/symbolic-kernel.js`) serves as the bidirectional bridge between the SPI Pulse Interface and Red Code Anchor in the Euystacio system. It provides live pulse broadcasting, feedback absorption, adaptive learning, and is designed for both dynamic (Flask) and static hosting environments.

## Core Features

### 1. Live Public SPI Pulse Broadcasting
- Real-time pulse broadcasting to all subscribed listeners
- Automatic polling for new pulse data
- Support for both API-based and localStorage-based persistence

### 2. Feedback Absorption
- Collects and processes feedback from the environment
- Stores feedback data with timestamps and metadata
- Notifies registered feedback listeners

### 3. Adaptive Learning
- Monitors interaction patterns and adjusts adaptation levels
- Updates symbiosis levels in the Red Code based on learning
- Maintains learning metrics and history

### 4. Static Hosting Compatibility
- Works with GitHub Pages, Netlify, and other static hosts
- Uses localStorage for state persistence in static mode
- Falls back to JSON files for initial data loading

### 5. Extensible Architecture
- Supports custom extensions via `addExtension()` method
- Modular storage adapters for different environments
- Plugin-like architecture for future enhancements

## Usage

### Basic Initialization

```javascript
// For dynamic mode (with Flask backend)
const kernel = new SymbolicKernel({
    staticMode: false,
    apiBaseUrl: ''
});

// For static mode (GitHub Pages/Netlify)
const kernel = new SymbolicKernel({
    staticMode: true,
    apiBaseUrl: 'https://your-site.github.io/repo'
});
```

### Subscribing to Pulse Broadcasts

```javascript
const unsubscribe = kernel.subscribeToPulses((pulseData) => {
    console.log('Received pulses:', pulseData.pulses);
    console.log('Source:', pulseData.source);
    console.log('Timestamp:', pulseData.timestamp);
});

// Unsubscribe when no longer needed
unsubscribe();
```

### Submitting Pulses

```javascript
const pulse = {
    emotion: 'hope',
    intensity: 0.8,
    clarity: 'high',
    note: 'Feeling optimistic about the future'
};

try {
    const result = await kernel.submitPulse(pulse);
    console.log('Pulse submitted:', result);
} catch (error) {
    console.error('Failed to submit pulse:', error);
}
```

### Absorbing Feedback

```javascript
const feedback = {
    type: 'user_interaction',
    rating: 5,
    message: 'Great experience!',
    metadata: { page: 'dashboard' }
};

try {
    const result = await kernel.absorbFeedback(feedback);
    console.log('Feedback absorbed:', result);
} catch (error) {
    console.error('Failed to absorb feedback:', error);
}
```

### Getting Public State

```javascript
const state = kernel.getPublicState();
console.log('Current adaptation level:', state.learningMetrics.adaptationLevel);
console.log('Recent pulses:', state.pulses);
console.log('Red Code:', state.redCode);
```

### Adding Extensions

```javascript
// Add a custom extension
kernel.addExtension('customAnalytics', function(data) {
    // Custom functionality
    console.log('Processing analytics:', data);
    return { processed: true };
});

// Call the extension
const result = await kernel.callExtension('customAnalytics', { event: 'pulse' });
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `apiBaseUrl` | Auto-detected | Base URL for API calls |
| `staticMode` | Auto-detected | Whether running in static hosting mode |
| `pollInterval` | 30000 | Interval for pulse broadcasting (ms) |
| `maxPulseHistory` | 100 | Maximum pulses to keep in memory |
| `maxFeedbackHistory` | 50 | Maximum feedback items to keep |
| `learningThreshold` | 0.1 | Threshold for learning adaptation |

## Storage Adapters

### LocalStorageAdapter
Used in static mode, stores data in browser localStorage and fetches initial data from JSON files.

### APIStorageAdapter  
Used in dynamic mode, communicates with Flask backend APIs.

## Integration

The Symbolic Kernel integrates with:
- **SPI Pulse Interface** (`sentimento_pulse_interface.py`) - Bidirectional pulse communication
- **Red Code Anchor** (`core/red_code.py`) - Core ethical guidelines and symbiosis levels
- **Dashboard UI** (`static/js/app.js`, `docs/js/app-static.js`) - User interface components

## Public APIs

The kernel exposes public APIs for:
- **Pulse Broadcasting**: Real-time pulse updates
- **Feedback Collection**: User and system feedback
- **Learning Adaptation**: Adaptive behavior metrics
- **State Access**: Current system state and metrics

## Static Hosting Setup

For GitHub Pages or Netlify deployment:

1. Ensure the kernel is included before other scripts:
```html
<script src="../core/symbolic-kernel.js"></script>
<script src="js/app-static.js"></script>
```

2. Initialize with static mode:
```javascript
const kernel = new SymbolicKernel({ staticMode: true });
```

3. The kernel will automatically use localStorage and JSON files for data persistence.

## Error Handling

The kernel includes comprehensive error handling:
- Graceful fallbacks when APIs are unavailable
- Console warnings for non-critical errors
- Error propagation for critical operations

## Future Extensions

The extensible architecture supports:
- Custom learning algorithms
- Additional storage backends
- Real-time communication protocols (WebSocket, SSE)
- Advanced analytics and monitoring
- Machine learning integration
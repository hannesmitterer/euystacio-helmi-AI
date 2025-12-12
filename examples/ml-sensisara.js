/**
 * Example: ML Integration with Sensisara Principle
 * Demonstrates ecosystem-inspired decision-making patterns
 */

const { SensisaraML } = require('../sdk/index.js');

console.log('🌿 Sensisara ML - Natural Decision Making\n');

// Example 1: Homeostatic Balancing
console.log('🔄 Example 1: Homeostatic Balancing');
console.log('   (Natural bounds and smoothing for model outputs)\n');

const rawOutputs = [0.98, 0.03, 0.91, 0.07, 0.85];
console.log('   Raw model outputs:', rawOutputs);

const balanced = SensisaraML.applyHomeostasis(rawOutputs, {
  minThreshold: 0.1,    // Minimum natural bound
  maxThreshold: 0.9,    // Maximum natural bound
  smoothingFactor: 0.4  // Damping factor (like biological resistance)
});

console.log('   Balanced outputs:', balanced.map(v => v.toFixed(3)));
console.log('   Benefits:');
console.log('     ✅ Prevents extreme outputs');
console.log('     ✅ Adds stability through damping');
console.log('     ✅ Mimics biological homeostasis\n');

// Example 2: Quorum-Based Decision Making
console.log('🤝 Example 2: Quorum-Based Decision (Ensemble)');
console.log('   (Multiple models must agree - like bacterial quorum sensing)\n');

// Simulate outputs from 3 different models
const model1_outputs = [0.82, 0.15, 0.73, 0.28];
const model2_outputs = [0.79, 0.18, 0.71, 0.31];
const model3_outputs = [0.84, 0.14, 0.75, 0.25];

console.log('   Model 1:', model1_outputs);
console.log('   Model 2:', model2_outputs);
console.log('   Model 3:', model3_outputs);

const decision = SensisaraML.quorumDecision(
  [model1_outputs, model2_outputs, model3_outputs],
  0.7 // 70% confidence threshold for quorum
);

console.log('\n   Consensus Outputs:', decision.outputs.map(v => v.toFixed(3)));
console.log('   Confidence:', decision.confidence.map(v => v.toFixed(3)));
console.log('   Meets Quorum:', decision.meetsQuorum ? '✅' : '❌');
console.log('   Average Confidence:', decision.averageConfidence.toFixed(3));
console.log('\n   Benefits:');
console.log('     ✅ Reduces individual model bias');
console.log('     ✅ Increases decision robustness');
console.log('     ✅ Provides confidence metrics');
console.log('     ✅ Mimics natural consensus patterns\n');

// Example 3: Combined Pattern
console.log('🌊 Example 3: Combined Homeostasis + Quorum');
console.log('   (Full biosystemic decision pipeline)\n');

// Multiple models with raw outputs
const rawModel1 = [0.95, 0.02, 0.88];
const rawModel2 = [0.97, 0.01, 0.92];
const rawModel3 = [0.93, 0.04, 0.86];

console.log('   Raw outputs from 3 models:');
console.log('     Model 1:', rawModel1);
console.log('     Model 2:', rawModel2);
console.log('     Model 3:', rawModel3);

// Step 1: Apply homeostasis to each model
const balancedModel1 = SensisaraML.applyHomeostasis(rawModel1);
const balancedModel2 = SensisaraML.applyHomeostasis(rawModel2);
const balancedModel3 = SensisaraML.applyHomeostasis(rawModel3);

console.log('\n   After homeostatic balancing:');
console.log('     Model 1:', balancedModel1.map(v => v.toFixed(3)));
console.log('     Model 2:', balancedModel2.map(v => v.toFixed(3)));
console.log('     Model 3:', balancedModel3.map(v => v.toFixed(3)));

// Step 2: Apply quorum decision
const finalDecision = SensisaraML.quorumDecision(
  [balancedModel1, balancedModel2, balancedModel3],
  0.6
);

console.log('\n   Final consensus decision:', finalDecision.outputs.map(v => v.toFixed(3)));
console.log('   Confidence:', finalDecision.confidence.map(v => v.toFixed(3)));
console.log('   Meets Quorum:', finalDecision.meetsQuorum ? '✅' : '❌');

console.log('\n   This mimics natural decision-making:');
console.log('     1️⃣  Individual regulation (homeostasis)');
console.log('     2️⃣  Collective agreement (quorum sensing)');
console.log('     3️⃣  Confidence-weighted output');
console.log('     4️⃣  Resilient to individual failures\n');

// Example 4: Real-world Application
console.log('🎯 Example 4: Real-World Application - Fraud Detection\n');

// Simulate fraud detection from 4 models
const fraudModel1 = [0.89, 0.12, 0.65, 0.91]; // [fraud_score_tx1, tx2, tx3, tx4]
const fraudModel2 = [0.85, 0.15, 0.61, 0.88];
const fraudModel3 = [0.92, 0.10, 0.68, 0.94];
const fraudModel4 = [0.87, 0.14, 0.63, 0.90];

console.log('   Transaction fraud scores (4 models, 4 transactions):');
console.log('   Model A:', fraudModel1);
console.log('   Model B:', fraudModel2);
console.log('   Model C:', fraudModel3);
console.log('   Model D:', fraudModel4);

const fraudDecision = SensisaraML.quorumDecision(
  [fraudModel1, fraudModel2, fraudModel3, fraudModel4],
  0.8 // High confidence threshold for fraud detection
);

console.log('\n   Consensus fraud scores:', fraudDecision.outputs.map(v => v.toFixed(3)));
console.log('   Confidence:', fraudDecision.confidence.map(v => v.toFixed(3)));
console.log('   Meets high-confidence quorum:', fraudDecision.meetsQuorum ? '✅' : '❌');

console.log('\n   Decision interpretation:');
fraudDecision.outputs.forEach((score, idx) => {
  const confidence = fraudDecision.confidence[idx];
  const status = score > 0.7 && confidence > 0.8 ? '🚨 FRAUD' : 
                 score > 0.5 ? '⚠️  REVIEW' : '✅ SAFE';
  console.log(`     Transaction ${idx + 1}: ${status} (score: ${score.toFixed(2)}, confidence: ${confidence.toFixed(2)})`);
});

console.log('\n   Benefits for fraud detection:');
console.log('     ✅ Reduces false positives through consensus');
console.log('     ✅ Provides confidence levels for decisions');
console.log('     ✅ Resilient to model failures or attacks');
console.log('     ✅ Natural scaling with additional models\n');

console.log('🎉 Sensisara ML examples completed!\n');
console.log('💡 Key Principle: Nature has optimized decision-making for 3.8 billion years.');
console.log('   By applying biological patterns, we create more robust AI systems.\n');

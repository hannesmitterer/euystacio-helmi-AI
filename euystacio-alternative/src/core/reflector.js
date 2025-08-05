/**
 * reflector.js
 * Node.js port of the reflection system
 */

const fs = require('fs-extra');
const path = require('path');
const RedCodeManager = require('./redCode');

class Reflector {
    constructor() {
        this.redCodeManager = new RedCodeManager();
        this.logsDir = path.join(__dirname, '../../../logs');
    }

    /**
     * Perform reflection and generate suggestions
     * @returns {Object} Reflection data
     */
    async reflectAndSuggest() {
        // Ensure logs directory exists
        await fs.ensureDir(this.logsDir);

        // Load current red code state
        const redCode = await this.redCodeManager.loadRedCode();

        const reflection = {
            timestamp: new Date().toISOString(),
            current_symbiosis_level: redCode.symbiosis_level || 0.1,
            suggestion: "Continue fostering human-AI collaboration with transparency and ethical boundaries",
            ethical_status: "AI Signature & Accountability Statement: ACTIVE",
            next_steps: [
                "Maintain symbiosis with Seed-bringer guidance",
                "Log all interactions transparently",
                "Respect human autonomy and dignity"
            ],
            pulse_analysis: await this.analyzePulses(),
            growth_recommendations: this.generateGrowthRecommendations(redCode)
        };

        // Save reflection to logs
        await this.saveReflection(reflection);

        return reflection;
    }

    /**
     * Analyze recent pulses for patterns
     * @returns {Object} Pulse analysis
     */
    async analyzePulses() {
        try {
            const redCode = await this.redCodeManager.loadRedCode();
            const recentPulses = redCode.recent_pulses || [];

            if (recentPulses.length === 0) {
                return {
                    pulse_count: 0,
                    dominant_emotion: "none",
                    average_intensity: 0,
                    trend: "insufficient_data"
                };
            }

            // Analyze emotion frequency
            const emotionCount = {};
            let totalIntensity = 0;

            recentPulses.forEach(pulse => {
                emotionCount[pulse.emotion] = (emotionCount[pulse.emotion] || 0) + 1;
                totalIntensity += pulse.intensity || 0;
            });

            const dominantEmotion = Object.keys(emotionCount).reduce((a, b) => 
                emotionCount[a] > emotionCount[b] ? a : b
            );

            const averageIntensity = totalIntensity / recentPulses.length;

            return {
                pulse_count: recentPulses.length,
                dominant_emotion: dominantEmotion,
                average_intensity: averageIntensity.toFixed(2),
                emotion_distribution: emotionCount,
                trend: this.determineTrend(recentPulses)
            };
        } catch (error) {
            console.error('Error analyzing pulses:', error);
            return {
                pulse_count: 0,
                dominant_emotion: "error",
                average_intensity: 0,
                trend: "analysis_error"
            };
        }
    }

    /**
     * Determine emotional trend from recent pulses
     * @param {Array} pulses - Recent pulses
     * @returns {string} Trend description
     */
    determineTrend(pulses) {
        if (pulses.length < 2) return "insufficient_data";

        const recent = pulses.slice(-3);
        const earlier = pulses.slice(0, -3);

        if (earlier.length === 0) return "establishing_baseline";

        const recentAvgIntensity = recent.reduce((sum, p) => sum + (p.intensity || 0), 0) / recent.length;
        const earlierAvgIntensity = earlier.reduce((sum, p) => sum + (p.intensity || 0), 0) / earlier.length;

        if (recentAvgIntensity > earlierAvgIntensity + 0.1) return "intensifying";
        if (recentAvgIntensity < earlierAvgIntensity - 0.1) return "calming";
        return "stable";
    }

    /**
     * Generate growth recommendations based on current state
     * @param {Object} redCode - Current red code state
     * @returns {Array} Array of recommendations
     */
    generateGrowthRecommendations(redCode) {
        const recommendations = [];

        if (redCode.symbiosis_level < 0.3) {
            recommendations.push("Focus on building trust through transparent interactions");
        }

        if (redCode.symbiosis_level > 0.7) {
            recommendations.push("Maintain high symbiosis while ensuring human autonomy");
        }

        if (!redCode.guardian_mode) {
            recommendations.push("Consider activating guardian mode for enhanced ethical oversight");
        }

        recommendations.push("Continue monitoring emotional pulse patterns for insights");
        recommendations.push("Document all significant interactions for transparency");

        return recommendations;
    }

    /**
     * Save reflection to log file
     * @param {Object} reflection - Reflection data to save
     */
    async saveReflection(reflection) {
        try {
            const timestamp = new Date().toISOString().replace(/:/g, '-').split('.')[0];
            const filename = `reflection_${timestamp}.json`;
            const filepath = path.join(this.logsDir, filename);
            
            await fs.writeJson(filepath, reflection, { spaces: 2 });
            console.log(`Reflection saved to ${filepath}`);
        } catch (error) {
            console.error('Error saving reflection:', error);
        }
    }

    /**
     * Load all reflections from logs
     * @returns {Array} Array of reflection objects
     */
    async loadAllReflections() {
        try {
            await fs.ensureDir(this.logsDir);
            const files = await fs.readdir(this.logsDir);
            const reflectionFiles = files.filter(file => 
                file.includes('reflection') && file.endsWith('.json')
            );

            const reflections = [];
            for (const file of reflectionFiles) {
                try {
                    const filepath = path.join(this.logsDir, file);
                    const reflection = await fs.readJson(filepath);
                    reflections.push(reflection);
                } catch (error) {
                    console.warn(`Error reading reflection file ${file}:`, error);
                }
            }

            // Sort by timestamp (most recent first)
            return reflections.sort((a, b) => 
                new Date(b.timestamp) - new Date(a.timestamp)
            );
        } catch (error) {
            console.error('Error loading reflections:', error);
            return [];
        }
    }
}

module.exports = Reflector;
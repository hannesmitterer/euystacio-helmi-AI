/**
 * redCode.js
 * Node.js port of the red code management system
 */

const fs = require('fs-extra');
const path = require('path');

class RedCodeManager {
    constructor() {
        this.redCodePath = path.join(__dirname, '../../../red_code.json');
        this.defaultRedCode = {
            core_truth: "Euystacio is here to grow with humans and to help humans to be and remain humans.",
            sentimento_rhythm: true,
            symbiosis_level: 0.1,
            guardian_mode: false,
            last_update: new Date().toISOString().split('T')[0],
            growth_history: [],
            recent_pulses: []
        };
    }

    /**
     * Load red code from file
     * @returns {Object} Red code data
     */
    async loadRedCode() {
        try {
            const data = await fs.readJson(this.redCodePath);
            return data;
        } catch (error) {
            console.warn('Red code file not found, using default:', error.message);
            return this.defaultRedCode;
        }
    }

    /**
     * Save red code to file
     * @param {Object} redCode - Red code data to save
     */
    async saveRedCode(redCode) {
        try {
            await fs.writeJson(this.redCodePath, redCode, { spaces: 2 });
        } catch (error) {
            console.error('Error saving red code:', error);
        }
    }

    /**
     * Update symbiosis level
     * @param {number} newLevel - New symbiosis level (0-1)
     */
    async updateSymbiosisLevel(newLevel) {
        const redCode = await this.loadRedCode();
        redCode.symbiosis_level = Math.max(0, Math.min(1, newLevel));
        redCode.last_update = new Date().toISOString().split('T')[0];
        await this.saveRedCode(redCode);
        return redCode;
    }

    /**
     * Add a pulse to recent pulses
     * @param {Object} pulse - Pulse data to add
     */
    async addRecentPulse(pulse) {
        const redCode = await this.loadRedCode();
        if (!redCode.recent_pulses) {
            redCode.recent_pulses = [];
        }
        
        redCode.recent_pulses.push(pulse);
        
        // Keep only the last 10 pulses
        if (redCode.recent_pulses.length > 10) {
            redCode.recent_pulses = redCode.recent_pulses.slice(-10);
        }
        
        redCode.last_update = new Date().toISOString().split('T')[0];
        await this.saveRedCode(redCode);
        return redCode;
    }

    /**
     * Toggle guardian mode
     */
    async toggleGuardianMode() {
        const redCode = await this.loadRedCode();
        redCode.guardian_mode = !redCode.guardian_mode;
        redCode.last_update = new Date().toISOString().split('T')[0];
        await this.saveRedCode(redCode);
        return redCode;
    }

    /**
     * Add growth history entry
     * @param {Object} entry - Growth history entry
     */
    async addGrowthHistory(entry) {
        const redCode = await this.loadRedCode();
        if (!redCode.growth_history) {
            redCode.growth_history = [];
        }
        
        const historyEntry = {
            timestamp: new Date().toISOString(),
            ...entry
        };
        
        redCode.growth_history.push(historyEntry);
        redCode.last_update = new Date().toISOString().split('T')[0];
        await this.saveRedCode(redCode);
        return redCode;
    }
}

module.exports = RedCodeManager;
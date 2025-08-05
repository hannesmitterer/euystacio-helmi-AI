/**
 * routes.js
 * Main API routes for the Euystacio Express server
 */

const express = require('express');
const fs = require('fs-extra');
const path = require('path');

const SentimentoPulseInterface = require('../core/sentimentoPulseInterface');
const RedCodeManager = require('../core/redCode');
const Reflector = require('../core/reflector');
const TutorNomination = require('../core/tutorNomination');

const router = express.Router();

// Initialize core modules
const spi = new SentimentoPulseInterface();
const redCodeManager = new RedCodeManager();
const reflector = new Reflector();
const tutors = new TutorNomination();

// Logs directory
const logsDir = path.join(__dirname, '../../../logs');

/**
 * Helper function to get all pulses from logs and red_code.json
 */
async function getAllPulses() {
    const pulses = [];
    
    try {
        // From red_code.json
        const redCode = await redCodeManager.loadRedCode();
        if (redCode.recent_pulses) {
            pulses.push(...redCode.recent_pulses);
        }
    } catch (error) {
        console.warn('Error loading recent pulses from red code:', error);
    }

    try {
        // From logs directory
        await fs.ensureDir(logsDir);
        const files = await fs.readdir(logsDir);
        const logFiles = files.filter(file => 
            file.startsWith('log_') && file.endsWith('.json')
        );

        for (const file of logFiles) {
            try {
                const filepath = path.join(logsDir, file);
                const log = await fs.readJson(filepath);
                
                // Extract pulses from log entries
                for (const [key, value] of Object.entries(log)) {
                    if (typeof value === 'object' && value.emotion) {
                        pulses.push(value);
                    }
                }
            } catch (error) {
                console.warn(`Error reading log file ${file}:`, error);
            }
        }
    } catch (error) {
        console.warn('Error reading logs directory:', error);
    }

    // Sort by timestamp (most recent first)
    return pulses.sort((a, b) => 
        new Date(b.timestamp || 0) - new Date(a.timestamp || 0)
    );
}

/**
 * GET /api/red_code
 * Get the current Red Code state
 */
router.get('/red_code', async (req, res) => {
    try {
        const redCode = await redCodeManager.loadRedCode();
        res.json(redCode);
    } catch (error) {
        console.error('Error getting red code:', error);
        res.status(500).json({ error: 'Failed to load red code' });
    }
});

/**
 * GET /api/pulses
 * Fetch the latest pulses
 */
router.get('/pulses', async (req, res) => {
    try {
        const pulses = await getAllPulses();
        res.json(pulses);
    } catch (error) {
        console.error('Error getting pulses:', error);
        res.status(500).json({ error: 'Failed to load pulses' });
    }
});

/**
 * POST /api/pulse
 * Submit a new emotional pulse
 */
router.post('/pulse', async (req, res) => {
    try {
        const { emotion, intensity, clarity, note } = req.body;

        // Validate required fields
        if (!emotion) {
            return res.status(400).json({ error: 'Emotion is required' });
        }

        // Process the pulse
        const event = spi.receivePulse(
            emotion,
            parseFloat(intensity) || 0.5,
            clarity || 'medium',
            note || ''
        );

        // Add to red code recent pulses
        await redCodeManager.addRecentPulse(event);

        // Emit WebSocket event if io is available
        if (req.io) {
            req.io.emit('new_pulse', event);
        }

        res.json(event);
    } catch (error) {
        console.error('Error processing pulse:', error);
        res.status(500).json({ error: 'Failed to process pulse' });
    }
});

/**
 * GET /api/reflections
 * Get reflection logs
 */
router.get('/reflections', async (req, res) => {
    try {
        const reflections = await reflector.loadAllReflections();
        res.json(reflections);
    } catch (error) {
        console.error('Error getting reflections:', error);
        res.status(500).json({ error: 'Failed to load reflections' });
    }
});

/**
 * POST /api/reflect
 * Trigger a new reflection
 */
router.post('/reflect', async (req, res) => {
    try {
        const reflection = await reflector.reflectAndSuggest();
        
        // Emit WebSocket event if io is available
        if (req.io) {
            req.io.emit('new_reflection', reflection);
        }

        res.json(reflection);
    } catch (error) {
        console.error('Error triggering reflection:', error);
        res.status(500).json({ error: 'Failed to trigger reflection' });
    }
});

/**
 * GET /api/tutors
 * Get tutor nominations
 */
router.get('/tutors', async (req, res) => {
    try {
        const tutorList = tutors.listTutors();
        res.json(tutorList);
    } catch (error) {
        console.error('Error getting tutors:', error);
        res.status(500).json({ error: 'Failed to load tutors' });
    }
});

/**
 * POST /api/tutors
 * Nominate a new tutor
 */
router.post('/tutors', async (req, res) => {
    try {
        const { name, reason } = req.body;

        if (!name) {
            return res.status(400).json({ error: 'Tutor name is required' });
        }

        const tutor = await tutors.nominate(name, reason || 'Nominated for wisdom and guidance');
        res.json(tutor);
    } catch (error) {
        console.error('Error nominating tutor:', error);
        res.status(500).json({ error: 'Failed to nominate tutor' });
    }
});

/**
 * GET /api/status
 * System status endpoint
 */
router.get('/status', async (req, res) => {
    try {
        const redCode = await redCodeManager.loadRedCode();
        const pulses = await getAllPulses();
        const reflections = await reflector.loadAllReflections();
        const tutorList = tutors.listTutors();

        res.json({
            status: 'healthy',
            timestamp: new Date().toISOString(),
            stats: {
                total_pulses: pulses.length,
                recent_pulses: redCode.recent_pulses?.length || 0,
                total_reflections: reflections.length,
                active_tutors: tutorList.length,
                symbiosis_level: redCode.symbiosis_level,
                guardian_mode: redCode.guardian_mode
            }
        });
    } catch (error) {
        console.error('Error getting status:', error);
        res.status(500).json({ 
            status: 'error',
            error: 'Failed to get system status' 
        });
    }
});

module.exports = router;
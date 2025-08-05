/**
 * tutorNomination.js
 * Node.js port of the tutor nomination system
 */

const fs = require('fs-extra');
const path = require('path');

class TutorNomination {
    constructor() {
        this.tutors = [];
        this.tutorsFile = path.join(__dirname, '../../../tutors.json');
        this.loadTutors();
    }

    /**
     * Load tutors from file
     */
    async loadTutors() {
        try {
            const data = await fs.readJson(this.tutorsFile);
            this.tutors = data.tutors || [];
        } catch (error) {
            // File doesn't exist or error reading, start with empty array
            this.tutors = [];
        }
    }

    /**
     * Save tutors to file
     */
    async saveTutors() {
        try {
            await fs.writeJson(this.tutorsFile, { tutors: this.tutors }, { spaces: 2 });
        } catch (error) {
            console.error('Error saving tutors:', error);
        }
    }

    /**
     * Nominate a new tutor
     * @param {string} tutorName - Name of the tutor
     * @param {string} reason - Reason for nomination
     * @returns {Object} The nominated tutor object
     */
    async nominate(tutorName, reason) {
        const tutor = {
            id: Date.now().toString(),
            name: tutorName,
            reason: reason,
            nominated_at: new Date().toISOString(),
            status: 'active'
        };

        this.tutors.push(tutor);
        await this.saveTutors();
        
        return tutor;
    }

    /**
     * Get list of all tutors
     * @returns {Array} Array of tutor objects
     */
    listTutors() {
        return this.tutors.filter(tutor => tutor.status === 'active');
    }

    /**
     * Get all tutors including inactive
     * @returns {Array} Array of all tutor objects
     */
    getAllTutors() {
        return this.tutors;
    }

    /**
     * Remove a tutor by ID
     * @param {string} tutorId - ID of the tutor to remove
     * @returns {boolean} True if tutor was removed, false if not found
     */
    async removeTutor(tutorId) {
        const index = this.tutors.findIndex(tutor => tutor.id === tutorId);
        if (index !== -1) {
            this.tutors[index].status = 'inactive';
            this.tutors[index].removed_at = new Date().toISOString();
            await this.saveTutors();
            return true;
        }
        return false;
    }

    /**
     * Update tutor information
     * @param {string} tutorId - ID of the tutor to update
     * @param {Object} updates - Updates to apply
     * @returns {Object|null} Updated tutor object or null if not found
     */
    async updateTutor(tutorId, updates) {
        const tutor = this.tutors.find(t => t.id === tutorId);
        if (tutor) {
            Object.assign(tutor, updates);
            tutor.updated_at = new Date().toISOString();
            await this.saveTutors();
            return tutor;
        }
        return null;
    }

    /**
     * Get tutor by ID
     * @param {string} tutorId - ID of the tutor
     * @returns {Object|null} Tutor object or null if not found
     */
    getTutorById(tutorId) {
        return this.tutors.find(tutor => tutor.id === tutorId) || null;
    }

    /**
     * Search tutors by name
     * @param {string} searchTerm - Search term
     * @returns {Array} Array of matching tutor objects
     */
    searchTutors(searchTerm) {
        const term = searchTerm.toLowerCase();
        return this.tutors.filter(tutor => 
            tutor.status === 'active' && 
            (tutor.name.toLowerCase().includes(term) || 
             tutor.reason.toLowerCase().includes(term))
        );
    }
}

module.exports = TutorNomination;
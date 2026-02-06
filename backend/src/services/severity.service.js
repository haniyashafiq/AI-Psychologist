/**
 * Severity assessment service for MDD
 */
const logger = require('../utils/logger');
const MDD_CRITERIA = require('../models/mdd-criteria');

class SeverityService {
  /**
   * Calculate severity of depression based on symptoms and functional impairment
   * @param {Array} symptoms - Detected symptoms
   * @param {Object} metadata - NLP metadata including functional impairment
   * @returns {Object} Severity assessment
   */
  calculateSeverity(symptoms, metadata) {
    const detectedCount = symptoms.filter((s) => s.detected).length;
    const functionalImpairment = metadata.functional_impairment || {};

    // Base severity from symptom count
    let severityLevel = this._getSeverityFromCount(detectedCount);
    let score = detectedCount;

    // Adjust severity based on functional impairment
    const impairmentSeverity = functionalImpairment.severity || 'none';

    if (impairmentSeverity === 'severe') {
      // Upgrade severity if severe impairment detected
      if (severityLevel === 'mild' && detectedCount >= 5) {
        severityLevel = 'moderate';
        logger.info('Upgraded severity from mild to moderate due to severe functional impairment');
      } else if (severityLevel === 'moderate' && detectedCount >= 7) {
        severityLevel = 'severe';
        logger.info(
          'Upgraded severity from moderate to severe due to severe functional impairment'
        );
      }
    }

    const severityData = MDD_CRITERIA.severityLevels[severityLevel];

    return {
      level: severityLevel,
      score,
      scoreRange: `${severityData.symptomRange[0]}-${severityData.symptomRange[1]}`,
      description: severityData.description,
      functionalImpairment: functionalImpairment.detected || false,
      impairmentSeverity: impairmentSeverity,
      impairmentDetails: functionalImpairment.keywords || [],
    };
  }

  /**
   * Get severity level from symptom count
   * @param {number} count - Number of detected symptoms
   * @returns {string} Severity level
   */
  _getSeverityFromCount(count) {
    if (count >= 9) return 'severe';
    if (count >= 7) return 'moderate';
    if (count >= 5) return 'mild';
    return 'subthreshold';
  }
}

module.exports = SeverityService;

/**
 * Diagnosis service implementing DSM-5 MDD diagnostic logic
 * Enhanced with RAG-powered AI clinical assessment
 */
const logger = require('../utils/logger');
const MDD_CRITERIA = require('../models/mdd-criteria');
const NLPService = require('./nlp.service');
const RAGService = require('./rag.service');
const SeverityService = require('./severity.service');

class DiagnosisService {
  constructor() {
    this.nlpService = new NLPService();
    this.ragService = new RAGService();
    this.severityService = new SeverityService();
    this.criteria = MDD_CRITERIA;
  }

  /**
   * Perform complete diagnosis from natural language text
   * @param {string} text - Patient symptom description
   * @returns {Promise<Object>} Complete diagnosis result
   */
  async diagnose(text) {
    try {
      logger.info('Starting diagnosis process');

      // Step 1: Run NLP symptom extraction and RAG assessment in parallel
      // RAG is the primary assessment — NLP provides supporting rule-based analysis
      const nlpResults = await this.nlpService.extractSymptoms(text);

      // Step 2: Map NLP results to DSM-5 criteria (needed as input for RAG)
      const mappedSymptoms = this._mapSymptomsToCriteria(nlpResults.symptoms);

      // Step 3: Apply rule-based diagnostic logic (supporting analysis)
      const diagnosis = this._applyMDDRules(mappedSymptoms, nlpResults.metadata);
      const severity = this.severityService.calculateSeverity(mappedSymptoms, nlpResults.metadata);
      const recommendations = this._generateRecommendations(diagnosis, severity, mappedSymptoms);
      const disclaimer = this._getDisclaimer();

      // Step 4: Get RAG-powered AI assessment (PRIMARY)
      // This is the core assessment — errors are propagated to the caller
      logger.info('Requesting RAG-powered AI clinical assessment (primary)');
      const aiAssessment = await this.ragService.queryAssessment(text, mappedSymptoms, {
        durationDays: nlpResults.metadata.duration_days,
        durationSpecified: nlpResults.metadata.duration_days > 0,
        functionalImpairment: nlpResults.metadata.functional_impairment || null,
      });

      logger.info(
        `Diagnosis complete: ${diagnosis.meetsThreshold ? 'MDD criteria met' : 'MDD criteria not met'}`
      );

      return {
        aiAssessment,
        diagnosis,
        severity,
        symptoms: mappedSymptoms,
        recommendations,
        disclaimer,
        metadata: {
          processingTime: nlpResults.metadata.processing_time_ms,
          durationDays: nlpResults.metadata.duration_days,
          durationSpecified: nlpResults.metadata.duration_days > 0,
        },
      };
    } catch (error) {
      logger.error('Diagnosis failed:', error);
      throw error;
    }
  }

  /**
   * Map NLP-extracted symptoms to DSM-5 criteria
   * @param {Array} nlpSymptoms - Symptoms from NLP service
   * @returns {Array} Mapped symptoms with DSM-5 codes
   */
  _mapSymptomsToCriteria(nlpSymptoms) {
    const mappedSymptoms = [];

    // Create a map of detected symptom IDs
    const detectedMap = new Map();
    nlpSymptoms.forEach((symptom) => {
      detectedMap.set(symptom.symptom_id, symptom);
    });

    // Map to DSM-5 criteria
    for (const [code, criteriaSymptom] of Object.entries(this.criteria.symptoms)) {
      const nlpSymptom = detectedMap.get(criteriaSymptom.id);

      if (nlpSymptom) {
        mappedSymptoms.push({
          dsm5Code: code,
          symptomId: criteriaSymptom.id,
          name: criteriaSymptom.name,
          detected: true,
          confidence: nlpSymptom.confidence,
          evidence: nlpSymptom.matched_phrases,
          sentenceContext: nlpSymptom.sentence_context,
          matchType: nlpSymptom.match_type,
        });
      } else {
        // Symptom not detected
        mappedSymptoms.push({
          dsm5Code: code,
          symptomId: criteriaSymptom.id,
          name: criteriaSymptom.name,
          detected: false,
          confidence: 0,
          evidence: [],
          sentenceContext: null,
          matchType: null,
        });
      }
    }

    return mappedSymptoms;
  }

  /**
   * Apply DSM-5 MDD diagnostic rules
   * @param {Array} symptoms - Mapped symptoms
   * @param {Object} metadata - NLP metadata
   * @returns {Object} Diagnosis result
   */
  _applyMDDRules(symptoms, metadata) {
    const detectedSymptoms = symptoms.filter((s) => s.detected);
    const detectedCount = detectedSymptoms.length;
    const detectedCodes = detectedSymptoms.map((s) => s.dsm5Code);

    // Check if core symptoms (A1 or A2) are present
    const hasDepressedMood = detectedCodes.includes('A1');
    const hasAnhedonia = detectedCodes.includes('A2');
    const hasCoreSymptom = hasDepressedMood || hasAnhedonia;

    // Check symptom count threshold
    const meetsCountThreshold = detectedCount >= this.criteria.requiredSymptoms;

    // Check duration
    const durationDays = metadata.duration_days || 0;
    const meetsDuration = durationDays >= this.criteria.requiredDurationDays;
    const durationSpecified = durationDays > 0;

    // Overall diagnosis
    const meetsThreshold =
      meetsCountThreshold && hasCoreSymptom && (meetsDuration || !durationSpecified);

    // Determine confidence level
    let confidence = 'low';
    if (meetsThreshold && meetsDuration) {
      confidence = 'high';
    } else if (meetsCountThreshold && hasCoreSymptom) {
      confidence = 'moderate';
    }

    // Check for crisis (suicidal ideation)
    const crisisDetected = detectedCodes.includes('A9');

    return {
      condition: this.criteria.name,
      code: this.criteria.code,
      meetsThreshold,
      confidence,
      criteriaMetCount: detectedCount,
      requiredCount: this.criteria.requiredSymptoms,
      hasCoreSymptom,
      coreSymptoms: {
        depressedMood: hasDepressedMood,
        anhedonia: hasAnhedonia,
      },
      duration: {
        days: durationDays,
        specified: durationSpecified,
        meetsRequirement: meetsDuration,
        required: this.criteria.requiredDurationDays,
      },
      crisisDetected,
    };
  }

  /**
   * Generate recommendations based on diagnosis
   * @param {Object} diagnosis - Diagnosis result
   * @param {Object} severity - Severity assessment
   * @param {Array} symptoms - Detected symptoms
   * @returns {Array} Recommendations
   */
  _generateRecommendations(diagnosis, severity, symptoms) {
    const recommendations = [];

    // Crisis recommendation (highest priority)
    if (diagnosis.crisisDetected) {
      recommendations.push({
        priority: 'critical',
        type: 'crisis_intervention',
        message:
          'URGENT: Suicidal ideation detected. Immediate professional intervention recommended.',
        resources: [
          'National Suicide Prevention Lifeline: 988',
          'Crisis Text Line: Text HOME to 741741',
          'Emergency Services: 911',
        ],
      });
    }

    // Diagnosis-based recommendations
    if (diagnosis.meetsThreshold) {
      recommendations.push({
        priority: 'high',
        type: 'professional_evaluation',
        message:
          'Criteria for Major Depressive Disorder are met. Strongly recommend professional psychiatric evaluation.',
        nextSteps: [
          'Schedule appointment with a mental health professional',
          'Consider bringing this assessment to your appointment',
          'Discuss treatment options (therapy, medication, or both)',
        ],
      });

      // Severity-specific recommendations
      if (severity.level === 'severe' || severity.functionalImpairment) {
        recommendations.push({
          priority: 'high',
          type: 'urgent_care',
          message:
            'Severe symptoms or significant functional impairment detected. Consider urgent evaluation.',
        });
      }
    } else if (diagnosis.criteriaMetCount >= 3) {
      recommendations.push({
        priority: 'moderate',
        type: 'monitoring',
        message:
          'Some depressive symptoms detected but full criteria not met. Monitor symptoms and consider professional consultation.',
        nextSteps: [
          'Track symptoms over the next 2 weeks',
          'Maintain self-care routines (sleep, nutrition, exercise)',
          'Seek support from friends, family, or counselor',
          'Consider professional evaluation if symptoms worsen',
        ],
      });
    }

    // General mental health recommendations
    recommendations.push({
      priority: 'general',
      type: 'self_care',
      message: 'General mental health recommendations',
      suggestions: [
        'Maintain regular sleep schedule',
        'Engage in physical activity',
        'Stay connected with supportive people',
        'Practice stress management techniques',
        'Avoid alcohol and substance use',
      ],
    });

    return recommendations;
  }

  /**
   * Get disclaimer text
   * @returns {string} Disclaimer
   */
  _getDisclaimer() {
    return (
      'IMPORTANT DISCLAIMER: This assessment is NOT a substitute for professional medical diagnosis. ' +
      'It is a screening tool based on DSM-5 criteria and should only be used by qualified mental health ' +
      'professionals as part of a comprehensive clinical evaluation. Only a licensed psychiatrist or ' +
      'psychologist can provide an official diagnosis. If you or someone you know is in crisis, ' +
      'please contact emergency services or a crisis hotline immediately.'
    );
  }
}

module.exports = DiagnosisService;

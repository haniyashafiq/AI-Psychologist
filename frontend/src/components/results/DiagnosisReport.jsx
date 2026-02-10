/**
 * Main diagnosis report component
 */
import clsx from 'clsx';
import { Button } from '../common/Button';
import { AIAssessment } from './AIAssessment';
import { RecommendationsCard } from './RecommendationsCard';
import { SeverityIndicator } from './SeverityIndicator';

export const DiagnosisReport = ({ results, onReset }) => {
  if (!results) return null;

  const { diagnosis, severity, symptoms, recommendations, disclaimer, aiAssessment } = results;

  return (
    <div className="space-y-6">
      {/* Crisis Alert */}
      {diagnosis.crisisDetected && (
        <div className="bg-red-100 border-4 border-red-600 rounded-lg p-6 animate-pulse">
          <div className="flex items-start space-x-3">
            <span className="text-4xl">🚨</span>
            <div>
              <h2 className="text-2xl font-bold text-red-900 mb-2">
                CRISIS ALERT: IMMEDIATE ACTION REQUIRED
              </h2>
              <p className="text-red-800 font-semibold mb-3">
                Suicidal ideation has been detected. This requires immediate professional
                intervention.
              </p>
              <div className="space-y-2 text-red-900">
                <p className="font-semibold">Crisis Resources:</p>
                <ul className="space-y-1">
                  <li>
                    • <strong>National Suicide Prevention Lifeline:</strong> 988
                  </li>
                  <li>
                    • <strong>Crisis Text Line:</strong> Text HOME to 741741
                  </li>
                  <li>
                    • <strong>Emergency Services:</strong> 911
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quick Summary Banner */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <h2 className="text-xl font-bold text-gray-900">Assessment Results</h2>
            <span className="text-sm text-gray-500">
              {diagnosis.condition} ({diagnosis.code})
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <span
              className={clsx(
                'px-3 py-1 rounded-full text-xs font-semibold',
                diagnosis.meetsThreshold
                  ? 'bg-orange-100 text-orange-800 border border-orange-300'
                  : 'bg-gray-100 text-gray-800 border border-gray-300'
              )}
            >
              {diagnosis.meetsThreshold
                ? `✓ ${diagnosis.criteriaMetCount}/${diagnosis.requiredCount} Criteria Met`
                : `✗ ${diagnosis.criteriaMetCount}/${diagnosis.requiredCount} Criteria Met`}
            </span>
          </div>
        </div>
      </div>

      {/* AI Clinical Assessment (RAG-powered) — PRIMARY */}
      {aiAssessment && <AIAssessment aiAssessment={aiAssessment} />}

      {/* Recommendations */}
      <RecommendationsCard recommendations={recommendations} />

      {/* Supporting Rule-Based Analysis (collapsible) */}
      <details className="bg-white rounded-lg shadow-md overflow-hidden">
        <summary className="px-6 py-4 cursor-pointer hover:bg-gray-50 transition-colors">
          <div className="inline-flex items-center space-x-2">
            <span className="text-lg">🔬</span>
            <span className="text-lg font-semibold text-gray-900">
              Supporting Rule-Based Analysis
            </span>
            <span className="px-2 py-0.5 text-xs font-medium bg-gray-200 text-gray-600 rounded-full">
              NLP Pattern Matching
            </span>
          </div>
          <p className="text-sm text-gray-500 mt-1 ml-8">
            Automated symptom detection, severity scoring, and DSM-5 criteria matching
          </p>
        </summary>

        <div className="px-6 pb-6 space-y-4">
          {/* Diagnosis Summary */}
          <div className="flex items-center justify-between pt-2">
            <h4 className="text-md font-semibold text-gray-800">Diagnostic Criteria Check</h4>
            <span
              className={clsx(
                'px-3 py-1 rounded-full text-xs font-semibold',
                diagnosis.meetsThreshold
                  ? 'bg-orange-100 text-orange-800 border border-orange-300'
                  : 'bg-gray-100 text-gray-800 border border-gray-300'
              )}
            >
              {diagnosis.meetsThreshold ? '✓ Criteria Met' : '✗ Criteria Not Met'}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-xs text-gray-600 mb-1">Symptoms Detected</p>
              <p className="text-2xl font-bold text-gray-900">
                {diagnosis.criteriaMetCount} / {diagnosis.requiredCount}
              </p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-xs text-gray-600 mb-1">Rule Confidence</p>
              <p className="text-2xl font-bold text-gray-900 capitalize">{diagnosis.confidence}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-xs text-gray-600 mb-1">Duration</p>
              <p className="text-2xl font-bold text-gray-900">
                {diagnosis.duration.specified ? `${diagnosis.duration.days} days` : 'Not specified'}
              </p>
            </div>
          </div>

          {/* Severity */}
          <SeverityIndicator severity={severity} />

          {/* Symptom Detail */}
          <h4 className="text-md font-semibold text-gray-800">Symptom Detection Detail</h4>
          <div className="space-y-2">
            {symptoms.map((symptom, index) => (
              <div
                key={index}
                className={clsx(
                  'rounded-lg p-3 border',
                  symptom.detected ? 'bg-green-50 border-green-300' : 'bg-gray-50 border-gray-200'
                )}
              >
                <div className="flex items-center space-x-2">
                  <span className="text-sm">{symptom.detected ? '✅' : '⭕'}</span>
                  <div className="flex-1">
                    <p className="font-medium text-sm text-gray-900">
                      {symptom.dsm5Code}: {symptom.name}
                    </p>
                    {symptom.detected && (
                      <div className="mt-1 space-y-0.5">
                        <p className="text-xs text-gray-700">
                          <strong>Evidence:</strong> {symptom.evidence.join(', ')}
                        </p>
                        {symptom.sentenceContext && (
                          <p className="text-xs text-gray-600 italic">
                            "{symptom.sentenceContext}"
                          </p>
                        )}
                        <p className="text-xs text-gray-500">
                          Confidence: {(symptom.confidence * 100).toFixed(0)}% • {symptom.matchType}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </details>

      {/* Disclaimer */}
      <div className="bg-yellow-50 border-2 border-yellow-400 rounded-lg p-6">
        <h3 className="font-bold text-yellow-900 mb-2 flex items-center">
          <span className="text-2xl mr-2">⚠️</span>
          Important Disclaimer
        </h3>
        <p className="text-sm text-yellow-900 leading-relaxed">{disclaimer}</p>
      </div>

      {/* Actions */}
      <div className="flex justify-center space-x-4">
        <Button onClick={onReset} variant="secondary" size="lg">
          New Assessment
        </Button>
        <Button onClick={() => window.print()} variant="primary" size="lg">
          Print Report
        </Button>
      </div>
    </div>
  );
};

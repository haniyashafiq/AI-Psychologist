/**
 * Main diagnosis report component
 */
import clsx from 'clsx';
import { Button } from '../common/Button';
import { RecommendationsCard } from './RecommendationsCard';
import { SeverityIndicator } from './SeverityIndicator';

export const DiagnosisReport = ({ results, onReset }) => {
  if (!results) return null;

  const { diagnosis, severity, symptoms, recommendations, disclaimer } = results;

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

      {/* Diagnosis Result */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Diagnostic Assessment</h2>
          <span
            className={clsx(
              'px-4 py-2 rounded-full text-sm font-semibold',
              diagnosis.meetsThreshold
                ? 'bg-orange-100 text-orange-800 border border-orange-300'
                : 'bg-gray-100 text-gray-800 border border-gray-300'
            )}
          >
            {diagnosis.meetsThreshold ? '✓ Criteria Met' : '✗ Criteria Not Met'}
          </span>
        </div>

        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">{diagnosis.condition}</h3>
            <p className="text-gray-600 text-sm">DSM-5 Code: {diagnosis.code}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-600 mb-1">Symptoms Detected</p>
              <p className="text-3xl font-bold text-gray-900">
                {diagnosis.criteriaMetCount} / {diagnosis.requiredCount}
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-600 mb-1">Confidence</p>
              <p className="text-3xl font-bold text-gray-900 capitalize">{diagnosis.confidence}</p>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-600 mb-1">Duration</p>
              <p className="text-3xl font-bold text-gray-900">
                {diagnosis.duration.specified ? `${diagnosis.duration.days} days` : 'Not specified'}
              </p>
            </div>
          </div>

          {/* Core Symptoms Check */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="font-semibold text-blue-900 mb-2">Core Symptoms (At least 1 required):</p>
            <div className="space-y-1 text-sm">
              <p
                className={
                  diagnosis.coreSymptoms.depressedMood ? 'text-green-700' : 'text-gray-600'
                }
              >
                {diagnosis.coreSymptoms.depressedMood ? '✓' : '○'} Depressed Mood
              </p>
              <p className={diagnosis.coreSymptoms.anhedonia ? 'text-green-700' : 'text-gray-600'}>
                {diagnosis.coreSymptoms.anhedonia ? '✓' : '○'} Anhedonia (Loss of Interest/Pleasure)
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Severity */}
      <SeverityIndicator severity={severity} />

      {/* Symptoms Detail */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Symptom Analysis</h3>

        <div className="space-y-3">
          {symptoms.map((symptom, index) => (
            <div
              key={index}
              className={clsx(
                'rounded-lg p-4 border-2',
                symptom.detected ? 'bg-green-50 border-green-300' : 'bg-gray-50 border-gray-200'
              )}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-xl">{symptom.detected ? '✅' : '⭕'}</span>
                    <div>
                      <p className="font-semibold text-gray-900">
                        {symptom.dsm5Code}: {symptom.name}
                      </p>
                      {symptom.detected && (
                        <div className="mt-2 space-y-1">
                          <p className="text-sm text-gray-700">
                            <strong>Evidence:</strong> {symptom.evidence.join(', ')}
                          </p>
                          {symptom.sentenceContext && (
                            <p className="text-sm text-gray-600 italic">
                              "{symptom.sentenceContext}"
                            </p>
                          )}
                          <p className="text-xs text-gray-500">
                            Confidence: {(symptom.confidence * 100).toFixed(0)}% • Match Type:{' '}
                            {symptom.matchType}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <RecommendationsCard recommendations={recommendations} />

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

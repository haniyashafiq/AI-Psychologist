/**
 * AI Clinical Assessment component
 * Renders RAG-powered clinical assessment with DSM-5-TR references
 */
import clsx from 'clsx';
import { useState } from 'react';

export const AIAssessment = ({ aiAssessment }) => {
  const [expandedSections, setExpandedSections] = useState({
    narrative: true,
    references: false,
    differential: false,
    assessments: false,
    riskFactors: false,
    sources: false,
  });

  if (!aiAssessment) return null;

  const { assessment, sources, usage, metrics } = aiAssessment;

  const toggleSection = (section) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const SectionHeader = ({ title, section, icon, badge }) => (
    <button
      onClick={() => toggleSection(section)}
      className="w-full flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg transition-colors"
    >
      <div className="flex items-center space-x-2">
        <span className="text-lg">{icon}</span>
        <h4 className="text-lg font-semibold text-gray-900">{title}</h4>
        {badge && (
          <span className="px-2 py-0.5 text-xs font-medium bg-indigo-100 text-indigo-700 rounded-full">
            {badge}
          </span>
        )}
      </div>
      <span className="text-gray-400 text-sm">{expandedSections[section] ? '▲' : '▼'}</span>
    </button>
  );

  const strengthColor = (strength) => {
    switch (strength) {
      case 'strong':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'moderate':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'weak':
        return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'absent':
        return 'bg-gray-100 text-gray-600 border-gray-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden border-2 border-indigo-200">
      {/* Header with AI badge */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">🧠</span>
            <div>
              <h3 className="text-xl font-bold text-white">AI Clinical Assessment</h3>
              <p className="text-indigo-200 text-sm">RAG-powered analysis grounded in DSM-5-TR</p>
            </div>
          </div>
          <span className="px-3 py-1 bg-white/20 text-white text-xs font-semibold rounded-full backdrop-blur-sm">
            AI-Generated
          </span>
        </div>
      </div>

      <div className="p-6 space-y-4">
        {/* Clinical Narrative */}
        <div>
          <SectionHeader title="Clinical Narrative" section="narrative" icon="📋" />
          {expandedSections.narrative && assessment?.clinical_narrative && (
            <div className="mt-2 px-3 py-4 bg-gray-50 rounded-lg">
              <p className="text-gray-800 leading-relaxed whitespace-pre-line">
                {assessment.clinical_narrative}
              </p>
            </div>
          )}
        </div>

        {/* DSM-5-TR References */}
        {assessment?.dsm_references?.length > 0 && (
          <div>
            <SectionHeader
              title="DSM-5-TR Criteria References"
              section="references"
              icon="📖"
              badge={`${assessment.dsm_references.length} criteria`}
            />
            {expandedSections.references && (
              <div className="mt-2 space-y-2 px-3">
                {assessment.dsm_references.map((ref, i) => (
                  <div key={i} className="border rounded-lg p-3 bg-white">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="font-semibold text-indigo-700">{ref.criteria_code}</span>
                          <span
                            className={clsx(
                              'px-2 py-0.5 text-xs font-medium rounded-full border',
                              strengthColor(ref.evidence_strength)
                            )}
                          >
                            {ref.evidence_strength}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 mb-1">{ref.criteria_text}</p>
                        <p className="text-sm text-gray-600 italic">{ref.relevance}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Differential Considerations */}
        {assessment?.differential_considerations?.length > 0 && (
          <div>
            <SectionHeader
              title="Differential Diagnosis Considerations"
              section="differential"
              icon="🔀"
              badge={`${assessment.differential_considerations.length} conditions`}
            />
            {expandedSections.differential && (
              <div className="mt-2 space-y-2 px-3">
                {assessment.differential_considerations.map((diff, i) => (
                  <div key={i} className="border rounded-lg p-3 bg-orange-50 border-orange-200">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="font-semibold text-orange-800">{diff.condition}</span>
                      {diff.dsm5_code && (
                        <span className="text-xs text-orange-600">({diff.dsm5_code})</span>
                      )}
                    </div>
                    <p className="text-sm text-gray-700 mb-1">{diff.rationale}</p>
                    {diff.distinguishing_features && (
                      <p className="text-xs text-gray-600">
                        <strong>Distinguishing:</strong> {diff.distinguishing_features}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Severity Rationale */}
        {assessment?.severity_rationale && (
          <div className="px-3 py-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-lg">📊</span>
              <h4 className="font-semibold text-blue-900">Severity Rationale</h4>
            </div>
            <p className="text-sm text-blue-800">{assessment.severity_rationale}</p>
          </div>
        )}

        {/* Recommended Assessments */}
        {assessment?.recommended_assessments?.length > 0 && (
          <div>
            <SectionHeader
              title="Recommended Assessment Instruments"
              section="assessments"
              icon="📝"
              badge={`${assessment.recommended_assessments.length} tools`}
            />
            {expandedSections.assessments && (
              <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-2 px-3">
                {assessment.recommended_assessments.map((tool, i) => (
                  <div key={i} className="border rounded-lg p-3 bg-green-50 border-green-200">
                    <p className="font-semibold text-green-800 text-sm">{tool.instrument}</p>
                    <p className="text-xs text-gray-600 mt-1">{tool.purpose}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Risk & Protective Factors */}
        {(assessment?.risk_factors?.length > 0 || assessment?.protective_factors?.length > 0) && (
          <div>
            <SectionHeader title="Risk & Protective Factors" section="riskFactors" icon="⚖️" />
            {expandedSections.riskFactors && (
              <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-3 px-3">
                {assessment.risk_factors?.length > 0 && (
                  <div className="border rounded-lg p-3 bg-red-50 border-red-200">
                    <p className="font-semibold text-red-800 text-sm mb-2">Risk Factors</p>
                    <ul className="space-y-1">
                      {assessment.risk_factors.map((factor, i) => (
                        <li key={i} className="text-xs text-red-700 flex items-start">
                          <span className="mr-1">•</span>
                          <span>{factor}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {assessment.protective_factors?.length > 0 && (
                  <div className="border rounded-lg p-3 bg-emerald-50 border-emerald-200">
                    <p className="font-semibold text-emerald-800 text-sm mb-2">
                      Protective Factors
                    </p>
                    <ul className="space-y-1">
                      {assessment.protective_factors.map((factor, i) => (
                        <li key={i} className="text-xs text-emerald-700 flex items-start">
                          <span className="mr-1">•</span>
                          <span>{factor}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Confidence Notes */}
        {assessment?.confidence_notes && (
          <div className="px-3 py-3 bg-amber-50 border border-amber-200 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-lg">💡</span>
              <h4 className="font-semibold text-amber-900">Confidence Notes</h4>
            </div>
            <p className="text-sm text-amber-800">{assessment.confidence_notes}</p>
          </div>
        )}

        {/* Source References (collapsible) */}
        {sources?.length > 0 && (
          <div>
            <SectionHeader
              title="Retrieved DSM-5-TR Sources"
              section="sources"
              icon="🔗"
              badge={`${sources.length} sources`}
            />
            {expandedSections.sources && (
              <div className="mt-2 space-y-2 px-3">
                {sources.map((source, i) => (
                  <div key={i} className="border rounded-lg p-2 bg-gray-50 text-xs">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium text-gray-800">
                        {source.section || 'DSM-5-TR Section'}
                      </span>
                      <span className="text-gray-500">
                        Relevance: {(source.relevance_score * 100).toFixed(0)}%
                      </span>
                    </div>
                    {source.disorder && (
                      <span className="text-gray-600">
                        {source.disorder} {source.code && `(${source.code})`}
                      </span>
                    )}
                    {source.pages && <span className="text-gray-500 ml-2">pp. {source.pages}</span>}
                    <p className="text-gray-500 mt-1 italic">{source.excerpt}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Pipeline Metrics (subtle footer) */}
        {metrics && (
          <div className="flex items-center justify-between text-xs text-gray-400 pt-3 border-t border-gray-100 px-3">
            <span>
              Model: {usage?.model || 'GPT-4o'} • Tokens: {usage?.total_tokens || '—'}
            </span>
            <span>
              Embed: {metrics.embedding_ms}ms • Retrieval: {metrics.retrieval_ms}ms • LLM:{' '}
              {metrics.llm_ms}ms • Total: {metrics.total_ms}ms
            </span>
          </div>
        )}

        {/* AI Disclaimer */}
        <div className="px-3 py-2 bg-gray-100 rounded-lg mt-2">
          <p className="text-xs text-gray-500 leading-relaxed">
            <strong>AI Notice:</strong> This assessment was generated by an AI system using
            Retrieval-Augmented Generation (RAG) with DSM-5-TR reference material. It is a clinical
            decision-support tool and should NOT be used as a standalone diagnosis. All findings
            require verification by a licensed mental health professional.
          </p>
        </div>
      </div>
    </div>
  );
};

/**
 * Severity level indicator component
 */
import clsx from 'clsx';

export const SeverityIndicator = ({ severity }) => {
  if (!severity) return null;

  const { level, score, scoreRange, functionalImpairment, impairmentSeverity } = severity;

  const severityConfig = {
    mild: {
      color: 'yellow',
      bgColor: 'bg-yellow-100',
      textColor: 'text-yellow-800',
      borderColor: 'border-yellow-300',
      label: 'Mild',
      icon: '⚠️',
    },
    moderate: {
      color: 'orange',
      bgColor: 'bg-orange-100',
      textColor: 'text-orange-800',
      borderColor: 'border-orange-300',
      label: 'Moderate',
      icon: '⚠️⚠️',
    },
    severe: {
      color: 'red',
      bgColor: 'bg-red-100',
      textColor: 'text-red-800',
      borderColor: 'border-red-300',
      label: 'Severe',
      icon: '🚨',
    },
    subthreshold: {
      color: 'gray',
      bgColor: 'bg-gray-100',
      textColor: 'text-gray-800',
      borderColor: 'border-gray-300',
      label: 'Subthreshold',
      icon: 'ℹ️',
    },
  };

  const config = severityConfig[level] || severityConfig.subthreshold;

  return (
    <div className={clsx('rounded-lg border-2 p-6', config.borderColor, config.bgColor)}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <span className="text-3xl">{config.icon}</span>
          <div>
            <h3
              className="text-2xl font-bold"
              style={{ color: config.textColor.replace('text-', '') }}
            >
              {config.label} Severity
            </h3>
            <p className={clsx('text-sm', config.textColor)}>
              Symptom Score: {score} (Range: {scoreRange})
            </p>
          </div>
        </div>
      </div>

      {functionalImpairment && (
        <div className={clsx('mt-4 p-3 rounded-md border', config.borderColor)}>
          <div className="flex items-start space-x-2">
            <span className="text-lg">🔴</span>
            <div>
              <p className={clsx('font-semibold', config.textColor)}>
                Functional Impairment Detected
              </p>
              <p className={clsx('text-sm mt-1', config.textColor)}>
                {impairmentSeverity === 'severe' && 'Severe impairment in daily functioning'}
                {impairmentSeverity === 'moderate' && 'Moderate impairment in daily functioning'}
                {impairmentSeverity === 'mild' && 'Mild impairment in daily functioning'}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

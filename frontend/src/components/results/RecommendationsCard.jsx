/**
 * Recommendations card component
 */
import clsx from 'clsx';

export const RecommendationsCard = ({ recommendations = [] }) => {
  if (!recommendations || recommendations.length === 0) return null;

  const priorityConfig = {
    critical: {
      bgColor: 'bg-red-50',
      borderColor: 'border-red-400',
      textColor: 'text-red-900',
      badgeColor: 'bg-red-600 text-white',
      icon: '🚨',
    },
    high: {
      bgColor: 'bg-orange-50',
      borderColor: 'border-orange-400',
      textColor: 'text-orange-900',
      badgeColor: 'bg-orange-600 text-white',
      icon: '⚠️',
    },
    moderate: {
      bgColor: 'bg-yellow-50',
      borderColor: 'border-yellow-400',
      textColor: 'text-yellow-900',
      badgeColor: 'bg-yellow-600 text-white',
      icon: '💡',
    },
    general: {
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-400',
      textColor: 'text-blue-900',
      badgeColor: 'bg-blue-600 text-white',
      icon: 'ℹ️',
    },
  };

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold text-gray-900">Recommendations</h3>

      {recommendations.map((rec, index) => {
        const config = priorityConfig[rec.priority] || priorityConfig.general;

        return (
          <div
            key={index}
            className={clsx('rounded-lg border-2 p-4', config.borderColor, config.bgColor)}
          >
            <div className="flex items-start space-x-3">
              <span className="text-2xl">{config.icon}</span>
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <span
                    className={clsx(
                      'px-2 py-1 rounded text-xs font-semibold uppercase',
                      config.badgeColor
                    )}
                  >
                    {rec.priority}
                  </span>
                  <span className={clsx('text-xs font-medium', config.textColor)}>
                    {rec.type.replace(/_/g, ' ')}
                  </span>
                </div>

                <p className={clsx('font-medium mb-2', config.textColor)}>{rec.message}</p>

                {rec.resources && rec.resources.length > 0 && (
                  <div className="mt-3 space-y-1">
                    <p className={clsx('text-sm font-semibold', config.textColor)}>Resources:</p>
                    <ul className="space-y-1">
                      {rec.resources.map((resource, idx) => (
                        <li key={idx} className={clsx('text-sm', config.textColor)}>
                          • {resource}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {rec.nextSteps && rec.nextSteps.length > 0 && (
                  <div className="mt-3 space-y-1">
                    <p className={clsx('text-sm font-semibold', config.textColor)}>Next Steps:</p>
                    <ul className="space-y-1">
                      {rec.nextSteps.map((step, idx) => (
                        <li key={idx} className={clsx('text-sm', config.textColor)}>
                          {idx + 1}. {step}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {rec.suggestions && rec.suggestions.length > 0 && (
                  <div className="mt-3 space-y-1">
                    <ul className="space-y-1">
                      {rec.suggestions.map((suggestion, idx) => (
                        <li key={idx} className={clsx('text-sm', config.textColor)}>
                          • {suggestion}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

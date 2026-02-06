/**
 * DSM-5 Major Depressive Disorder diagnostic criteria
 */

const MDD_CRITERIA = {
  name: 'Major Depressive Disorder',
  code: 'F32.x / F33.x',
  requiredSymptoms: 5,
  requiredDurationDays: 14,
  mustIncludeOneOf: ['A1', 'A2'],

  symptoms: {
    A1: {
      id: 'depressed_mood',
      code: 'A1',
      name: 'Depressed mood most of the day, nearly every day',
      weight: 1,
    },
    A2: {
      id: 'anhedonia',
      code: 'A2',
      name: 'Markedly diminished interest or pleasure in all, or almost all, activities',
      weight: 1,
    },
    A3: {
      id: 'weight_change',
      code: 'A3',
      name: 'Significant weight loss or gain, or decrease/increase in appetite',
      weight: 1,
    },
    A4: {
      id: 'sleep_disturbance',
      code: 'A4',
      name: 'Insomnia or hypersomnia nearly every day',
      weight: 1,
    },
    A5: {
      id: 'psychomotor',
      code: 'A5',
      name: 'Psychomotor agitation or retardation (observable by others)',
      weight: 1,
    },
    A6: {
      id: 'fatigue',
      code: 'A6',
      name: 'Fatigue or loss of energy nearly every day',
      weight: 1,
    },
    A7: {
      id: 'worthlessness',
      code: 'A7',
      name: 'Feelings of worthlessness or excessive/inappropriate guilt',
      weight: 1,
    },
    A8: {
      id: 'concentration',
      code: 'A8',
      name: 'Diminished ability to think or concentrate, or indecisiveness',
      weight: 1,
    },
    A9: {
      id: 'suicidal_ideation',
      code: 'A9',
      name: 'Recurrent thoughts of death, suicidal ideation, or suicide attempt',
      weight: 1,
      flagForCrisis: true,
    },
  },

  severityLevels: {
    subthreshold: {
      symptomRange: [0, 4],
      description:
        'Fewer than 5 symptoms, does not meet diagnostic threshold for Major Depressive Disorder',
    },
    mild: {
      symptomRange: [5, 6],
      description:
        'Few symptoms in excess of those required, and symptoms result in minor impairment in functioning',
    },
    moderate: {
      symptomRange: [7, 8],
      description: 'Symptom severity or functional impairment is between mild and severe',
    },
    severe: {
      symptomRange: [9, 9],
      description:
        'Number of symptoms substantially exceeds what is required, and symptoms seriously interfere with functioning',
    },
  },

  exclusionCriteria: [
    'Symptoms are not attributable to the physiological effects of a substance or another medical condition',
    'The episode is not better explained by schizoaffective disorder, schizophrenia, or other psychotic disorders',
    'There has never been a manic episode or a hypomanic episode',
  ],
};

module.exports = MDD_CRITERIA;

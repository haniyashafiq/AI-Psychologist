# DSM-5 Major Depressive Disorder Criteria

## Overview

This document details the DSM-5 diagnostic criteria for Major Depressive Disorder (MDD) as implemented in the AI Psychologist system.

## Diagnostic Criteria

### Criterion A: Symptom Presence

Five (or more) of the following symptoms have been present during the same 2-week period and represent a change from previous functioning. **At least one of the symptoms is either (1) depressed mood or (2) loss of interest or pleasure.**

#### A1: Depressed Mood

**Clinical Description**: Depressed mood most of the day, nearly every day, as indicated by either subjective report (e.g., feels sad, empty, hopeless) or observation made by others (e.g., appears tearful).

**System Implementation**:

- **Keywords**: sad, depressed, empty, hopeless, down, low mood, miserable, unhappy, blue, crying, tearful
- **Phrases**: "feel sad", "feeling down", "mood is low", "can't stop crying", "everything feels dark"
- **Negation**: Excluded if preceded by "not", "no", "never", etc.

#### A2: Anhedonia (Loss of Interest or Pleasure)

**Clinical Description**: Markedly diminished interest or pleasure in all, or almost all, activities most of the day, nearly every day.

**System Implementation**:

- **Keywords**: no interest, lost interest, don't enjoy, no pleasure, anhedonia, apathy
- **Phrases**: "nothing interests me", "can't enjoy anything", "lost passion", "don't want to do anything"

#### A3: Weight or Appetite Change

**Clinical Description**: Significant weight loss when not dieting or weight gain (e.g., a change of more than 5% of body weight in a month), or decrease or increase in appetite nearly every day.

**System Implementation**:

- **Keywords**: lost weight, gained weight, no appetite, eating too much, lost appetite
- **Phrases**: "dropped pounds", "can't eat", "always hungry", "force myself to eat"

#### A4: Sleep Disturbance

**Clinical Description**: Insomnia or hypersomnia nearly every day.

**System Implementation**:

- **Keywords**: can't sleep, insomnia, trouble sleeping, sleeping too much, hypersomnia
- **Phrases**: "lying awake", "tossing and turning", "sleep all day", "can't get out of bed"

#### A5: Psychomotor Changes

**Clinical Description**: Psychomotor agitation or retardation nearly every day (observable by others, not merely subjective feelings of restlessness or being slowed down).

**System Implementation**:

- **Keywords**: restless, can't sit still, agitated, slowed down, sluggish, lethargic
- **Phrases**: "feel restless", "everything is slow", "moving in slow motion", "body feels heavy"

#### A6: Fatigue or Loss of Energy

**Clinical Description**: Fatigue or loss of energy nearly every day.

**System Implementation**:

- **Keywords**: tired, exhausted, fatigue, no energy, drained, worn out, weak
- **Phrases**: "always tired", "completely exhausted", "zero energy", "running on empty"

#### A7: Worthlessness or Guilt

**Clinical Description**: Feelings of worthlessness or excessive or inappropriate guilt (which may be delusional) nearly every day (not merely self-reproach or guilt about being sick).

**System Implementation**:

- **Keywords**: worthless, useless, failure, guilty, shame, inadequate, burden
- **Phrases**: "feel worthless", "i'm a failure", "let everyone down", "hate myself"

#### A8: Diminished Concentration

**Clinical Description**: Diminished ability to think or concentrate, or indecisiveness, nearly every day (either by subjective account or as observed by others).

**System Implementation**:

- **Keywords**: can't focus, can't concentrate, brain fog, indecisive, forgetful, confused
- **Phrases**: "mind is blank", "can't think clearly", "constantly distracted", "forget everything"

#### A9: Suicidal Ideation

**Clinical Description**: Recurrent thoughts of death (not just fear of dying), recurrent suicidal ideation without a specific plan, or a suicide attempt or a specific plan for committing suicide.

**System Implementation**:

- **Keywords**: suicide, kill myself, end it all, death, dying, better off dead, want to die
- **Phrases**: "think about death", "wish i was dead", "don't want to live", "thoughts of suicide"
- **Crisis Flag**: Automatically triggers immediate intervention recommendations

### Criterion B: Clinical Significance

The symptoms cause clinically significant distress or impairment in social, occupational, or other important areas of functioning.

**System Implementation**:

- Detected through **functional impairment keywords**
- Keywords: "can't work", "stopped socializing", "can't get out of bed", "relationships suffering"
- Used to adjust severity assessment

### Criterion C: Not Attributable to Substance/Medical Condition

The episode is not attributable to the physiological effects of a substance or another medical condition.

**System Implementation**:

- Not automatically evaluated (requires clinical judgment)
- Included in disclaimer/recommendations

### Criterion D: Not Better Explained by Other Disorders

The occurrence is not better explained by schizoaffective disorder, schizophrenia, schizophreniform disorder, delusional disorder, or other specified and unspecified schizophrenia spectrum and other psychotic disorders.

**System Implementation**:

- Not evaluated in MVP (single disorder only)
- Future: differential diagnosis logic

### Criterion E: No Manic/Hypomanic Episode

There has never been a manic episode or a hypomanic episode.

**System Implementation**:

- Not evaluated in MVP
- Future: screen for bipolar disorder

## Diagnostic Thresholds

### Symptom Count

- **Required**: ≥ 5 symptoms out of 9
- **Core Symptom**: Must include A1 (depressed mood) OR A2 (anhedonia)

### Duration

- **Required**: Symptoms present for ≥ 2 weeks
- **System Detection**: Extracts from phrases like "for 3 weeks", "past month", "lately"

### Severity Levels

#### Mild

- **Symptom Count**: 5-6 symptoms
- **Functional Impairment**: Few, if any, symptoms in excess of those required; minor impairment in functioning

#### Moderate

- **Symptom Count**: 7-8 symptoms
- **Functional Impairment**: Symptom severity or functional impairment between "mild" and "severe"

#### Severe

- **Symptom Count**: 9 symptoms
- **Functional Impairment**: Number of symptoms substantially exceeds what is required; symptoms seriously interfere with functioning

**System Enhancement**: Functional impairment can upgrade severity by one level if severe impairment detected.

## Exclusions

The system does NOT diagnose if:

- Fewer than 5 symptoms detected
- Neither A1 nor A2 is present
- Duration < 2 weeks (if specified)

## Confidence Levels

The system assigns confidence based on:

- **High**: All criteria met, duration confirmed
- **Moderate**: Symptom thresholds met, duration not specified
- **Low**: Borderline symptom count or missing core symptom

## Limitations

This system:

- ✅ Evaluates DSM-5 Criterion A (symptoms)
- ✅ Evaluates Criterion B (functional impairment - partial)
- ❌ Cannot evaluate Criterion C (substance/medical exclusion)
- ❌ Cannot evaluate Criterion D (differential diagnosis)
- ❌ Cannot evaluate Criterion E (bipolar screening)

**Clinical judgment is required for complete diagnosis.**

## References

American Psychiatric Association. (2013). Diagnostic and Statistical Manual of Mental Disorders (5th ed.). Arlington, VA: American Psychiatric Publishing.

---

**Note**: This implementation is for educational and professional screening purposes only. It does not replace clinical evaluation by a qualified mental health professional.

# Test Cases for MDD Diagnosis System

## Test Case 1: Typical Moderate MDD

### Input

```
I've been feeling really down for the past three weeks. I can't seem to enjoy anything anymore, not even activities I used to love like reading or spending time with friends. I'm having trouble sleeping at night - I lie awake for hours thinking about how worthless I am. During the day, I feel completely exhausted and have no energy to do anything. I've lost my appetite and dropped about 10 pounds without trying. It's hard to concentrate at work, and I can't make even simple decisions. I just feel like there's no point to anything.
```

### Expected Output

- **Diagnosis**: Meets MDD criteria (7 symptoms)
- **Severity**: Moderate
- **Symptoms Detected**:
  - A1: Depressed mood ✓ ("feeling really down")
  - A2: Anhedonia ✓ ("can't enjoy anything")
  - A3: Weight/Appetite ✓ ("lost appetite", "dropped 10 pounds")
  - A4: Sleep ✓ ("trouble sleeping", "lie awake")
  - A6: Fatigue ✓ ("exhausted", "no energy")
  - A7: Worthlessness ✓ ("how worthless I am")
  - A8: Concentration ✓ ("hard to concentrate", "can't make decisions")
- **Duration**: 3 weeks (meets 2-week threshold)
- **Functional Impairment**: Minimal

---

## Test Case 2: Severe MDD with Crisis

### Input

```
For the past month, I wake up every day feeling empty and hopeless. Nothing brings me joy anymore. I can't sleep at night, and when I do, I oversleep until noon. I have no appetite and have lost 15 pounds. I'm completely exhausted all the time and can barely get out of bed. I feel extremely guilty about being a burden to my family. My thoughts are foggy and I can't focus on anything. I move and think so slowly that my family has noticed. Lately, I've been thinking it would be better if I wasn't here anymore. Everyone would be better off without me. I keep thinking about different ways to end it all.
```

### Expected Output

- **Diagnosis**: Meets MDD criteria (9 symptoms) + CRISIS FLAG
- **Severity**: Severe
- **Symptoms Detected**: All 9 (A1-A9)
- **Duration**: 1 month (meets threshold)
- **Crisis Alert**: Suicidal ideation detected (A9)
- **Recommendations**: URGENT crisis intervention

---

## Test Case 3: Mild MDD

### Input

```
Over the past two weeks, I've noticed I'm feeling sad most days. Things that used to interest me don't seem as appealing anymore. I'm tired more than usual and my sleep has been off - sometimes I can't fall asleep, other times I sleep too much. My appetite is down and I've lost a few pounds. I still go to work and see friends, but it takes more effort than before.
```

### Expected Output

- **Diagnosis**: Meets MDD criteria (5 symptoms)
- **Severity**: Mild
- **Symptoms Detected**:
  - A1: Depressed mood ✓ ("feeling sad")
  - A2: Anhedonia ✓ (partial - "don't seem as appealing")
  - A3: Weight/Appetite ✓ ("appetite is down", "lost a few pounds")
  - A4: Sleep ✓ ("can't fall asleep", "sleep too much")
  - A6: Fatigue ✓ ("tired more than usual")
- **Duration**: 2 weeks (meets threshold exactly)
- **Functional Impairment**: Minimal ("still go to work")

---

## Test Case 4: Subthreshold (Not MDD)

### Input

```
I've been feeling a bit down lately, maybe for a week or so. Work has been stressful and I'm not sleeping great. I still enjoy hanging out with friends and working on my hobbies. I'm eating normally and have plenty of energy during the day. Sometimes I feel a little distracted, but nothing major.
```

### Expected Output

- **Diagnosis**: Does NOT meet MDD criteria (2-3 symptoms only)
- **Severity**: Subthreshold
- **Symptoms Detected**:
  - A1: Depressed mood ✓ (weak - "bit down")
  - A4: Sleep ✓ (weak - "not sleeping great")
  - A8: Concentration ? (very weak - "little distracted")
- **A2 Negated**: "still enjoy" (excludes anhedonia)
- **Duration**: ~1 week (below 2-week threshold)
- **Recommendations**: Monitoring, self-care

---

## Test Case 5: Negation Handling

### Input

```
I'm NOT feeling depressed at all. Actually, I'm doing quite well. I don't have trouble sleeping and my appetite is normal. I have plenty of energy and don't feel worthless. I can concentrate fine at work. I'm not having any thoughts about death or suicide. Things are going well for me right now.
```

### Expected Output

- **Diagnosis**: Does NOT meet MDD criteria (0 symptoms)
- **Symptoms Detected**: None (all negated)
- **Negation Detection**: All symptoms properly excluded due to negation terms

---

## Test Case 6: Mixed Severity with Functional Impairment

### Input

```
For three weeks now, I feel sad and empty every single day. I've completely lost interest in everything I used to care about. I can't sleep more than 3-4 hours a night. I have zero energy and feel exhausted constantly. I feel guilty about being such a failure. I can't concentrate on anything. I've stopped going to work because I just can't function. I can't get out of bed most days and stopped showering regularly. My relationships are falling apart because I don't have the energy to maintain them.
```

### Expected Output

- **Diagnosis**: Meets MDD criteria (6-7 symptoms)
- **Base Severity**: Mild to Moderate (6-7 symptoms)
- **Adjusted Severity**: Moderate to Severe (due to severe functional impairment)
- **Functional Impairment**: Severe
  - "stopped going to work"
  - "can't get out of bed"
  - "stopped showering"
  - "relationships falling apart"
- **Duration**: 3 weeks (meets threshold)

---

## Test Case 7: Duration Edge Cases

### Input A (No Duration Specified)

```
I feel sad and empty. Nothing interests me. I can't sleep. I'm exhausted. I feel worthless and can't concentrate.
```

### Expected Output A

- **Diagnosis**: Possible MDD (5 symptoms) but **moderate confidence**
- **Duration**: Not specified (system should note this)
- **Recommendation**: Duration assessment needed

### Input B (Below Threshold Duration)

```
For the past 10 days, I've been feeling depressed, lost interest in things, can't sleep, feel tired all the time, and feel worthless.
```

### Expected Output B

- **Diagnosis**: 5 symptoms but duration < 2 weeks
- **Recommendation**: Continue monitoring, reassess if persists

---

## Test Case 8: Psychomotor Symptoms (Often Missed)

### Input

```
My family says I've been moving really slowly lately, like everything is in slow motion. I feel restless inside but my body can't keep up. I've been pacing around the house constantly. People at work commented that I'm talking more slowly than usual. Along with this, I feel down most days, have no energy, trouble sleeping, and feel like a failure. This has been going on for about a month.
```

### Expected Output

- **Diagnosis**: Meets MDD criteria (5+ symptoms)
- **Symptoms Detected**:
  - A1: Depressed mood ✓ ("feel down")
  - A4: Sleep ✓ ("trouble sleeping")
  - A5: Psychomotor ✓ ("moving really slowly", "feel restless", "pacing", "talking slowly")
  - A6: Fatigue ✓ ("no energy")
  - A7: Worthlessness ✓ ("feel like a failure")
- **Duration**: 1 month ✓

---

## Test Case 9: Cultural/Colloquial Language

### Input

```
Man, I've been feeling like total crap for weeks now. Nothing's fun anymore, you know? I'm up all night staring at the ceiling, then dragging myself through the day. I've dropped like 12 pounds without even trying. I feel like I'm not worth anything and everything's my fault. My brain's just mush - can't think straight at all. Been like this for a solid month, maybe more.
```

### Expected Output

- **Diagnosis**: Meets MDD criteria (7+ symptoms)
- **Symptom Detection**: System should handle colloquial terms
  - "feeling like total crap" → depressed mood
  - "Nothing's fun" → anhedonia
  - "up all night staring at ceiling" → insomnia
  - "dragging through the day" → fatigue
  - "dropped 12 pounds" → weight change
  - "not worth anything" → worthlessness
  - "brain's just mush" → concentration issues

---

## Test Case 10: Functional Impairment Without Full MDD

### Input

```
I've been feeling down and have trouble sleeping. I've stopped going to work and can't take care of myself anymore. I stay in bed all day. But I still enjoy watching TV and eating my favorite foods. I don't feel worthless or have trouble concentrating.
```

### Expected Output

- **Diagnosis**: Does NOT meet full MDD criteria (3-4 symptoms only)
- **Symptoms**: A1 (mood), A4 (sleep), A6 (implied fatigue)
- **Missing Core Symptom**: A2 excluded ("still enjoy")
- **Functional Impairment**: Severe (but not sufficient for diagnosis without symptoms)
- **Recommendation**: Evaluate for other conditions, mood disorder NOS

---

## Performance Benchmarks

### Expected System Performance

- **Processing Time**: < 1 second per assessment
- **Symptom Detection Accuracy**: > 85% for clear cases
- **Negation Detection Accuracy**: > 90%
- **False Positive Rate**: < 10%
- **False Negative Rate**: < 15%

### Edge Cases to Monitor

- Very short input (< 50 words)
- Extremely long input (> 3000 words)
- Multiple languages/code-switching
- Medical terminology vs. colloquial language
- Ambiguous temporal phrases ("recently", "lately")

---

## Testing Checklist

- [ ] All 9 DSM-5 symptoms correctly detected
- [ ] Negation handling works properly
- [ ] Duration extraction accurate
- [ ] Functional impairment detection working
- [ ] Severity calculation correct
- [ ] Crisis detection (A9) triggers alerts
- [ ] Subthreshold cases handled appropriately
- [ ] API error handling functional
- [ ] Frontend displays all results correctly
- [ ] Print functionality works

---

**Note**: These test cases should be run manually through the UI and can also be automated via API tests using the provided test data.

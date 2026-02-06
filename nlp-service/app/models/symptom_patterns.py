"""DSM-5 Major Depressive Disorder symptom patterns and vocabulary"""

# DSM-5 MDD Diagnostic Criteria
MDD_CRITERIA = {
    "required_symptoms": 5,
    "required_duration_days": 14,
    "must_include_one_of": ["A1", "A2"],
}

# Symptom patterns for Major Depressive Disorder (DSM-5 Criteria A1-A9)
SYMPTOM_PATTERNS = {
    "A1": {
        "id": "depressed_mood",
        "name": "Depressed mood most of the day",
        "keywords": [
            "sad", "depressed", "empty", "hopeless", "down", "low mood",
            "miserable", "unhappy", "blue", "gloomy", "melancholy",
            "dejected", "despondent", "crying", "tearful"
        ],
        "phrases": [
            "feel sad", "feeling depressed", "feel empty", "feel hopeless",
            "mood is low", "feeling down", "feel miserable", "feel unhappy",
            "can't stop crying", "nothing makes me happy", "life feels meaningless",
            "everything feels dark", "feel like giving up", "no point in anything",
            "feeling blue", "feel awful", "emotionally numb"
        ],
        "token_patterns": [
            [{"LEMMA": "feel"}, {"LOWER": {"IN": ["sad", "depressed", "down", "empty", "hopeless", "miserable"]}}],
            [{"LOWER": "mood"}, {"LOWER": "is"}, {"LOWER": {"IN": ["low", "down", "bad"]}}],
            [{"LEMMA": "be"}, {"LOWER": {"IN": ["sad", "depressed", "unhappy", "miserable"]}}],
        ]
    },
    "A2": {
        "id": "anhedonia",
        "name": "Diminished interest or pleasure in activities",
        "keywords": [
            "no interest", "lost interest", "don't enjoy", "no pleasure",
            "anhedonia", "apathy", "unmotivated", "indifferent"
        ],
        "phrases": [
            "don't enjoy", "no interest in", "lost interest", "nothing feels good",
            "can't enjoy anything", "nothing interests me", "don't care about",
            "no motivation", "everything feels dull", "can't find pleasure",
            "activities don't appeal", "hobbies aren't fun", "stopped doing things i love",
            "nothing excites me", "lost passion", "don't want to do anything"
        ],
        "token_patterns": [
            [{"LOWER": {"IN": ["no", "lost"]}}, {"LOWER": "interest"}],
            [{"LOWER": {"IN": ["don't", "can't", "cannot"]}}, {"LOWER": "enjoy"}],
            [{"LOWER": "nothing"}, {"LEMMA": {"IN": ["interest", "excite", "appeal"]}}],
        ]
    },
    "A3": {
        "id": "weight_change",
        "name": "Significant weight loss or gain, or change in appetite",
        "keywords": [
            "lost weight", "gained weight", "weight loss", "weight gain",
            "no appetite", "eating too much", "appetite", "lost appetite",
            "overeating", "can't eat", "eating less"
        ],
        "phrases": [
            "lost weight", "gained weight", "no appetite", "eating too much",
            "can't eat", "lost appetite", "always hungry", "never hungry",
            "eating less", "eating more", "weight changed", "food doesn't appeal",
            "force myself to eat", "binge eating", "can't stop eating",
            "dropped pounds", "put on weight"
        ],
        "token_patterns": [
            [{"LOWER": {"IN": ["lost", "gained"]}}, {"LOWER": "weight"}],
            [{"LOWER": "no"}, {"LOWER": "appetite"}],
            [{"LOWER": {"IN": ["eating", "eat"]}}, {"LOWER": {"IN": ["less", "more", "too much"]}}],
        ]
    },
    "A4": {
        "id": "sleep_disturbance",
        "name": "Insomnia or hypersomnia nearly every day",
        "keywords": [
            "can't sleep", "insomnia", "trouble sleeping", "awake at night",
            "sleeping too much", "hypersomnia", "sleep all day", "can't get up"
        ],
        "phrases": [
            "can't sleep", "trouble sleeping", "can't fall asleep", "wake up at night",
            "lying awake", "tossing and turning", "insomnia", "sleepless nights",
            "sleeping too much", "sleep all day", "can't get out of bed",
            "always tired but can't sleep", "waking up early", "sleeping 12 hours",
            "no rest", "exhausted but awake", "oversleeping"
        ],
        "token_patterns": [
            [{"LOWER": {"IN": ["can't", "cannot", "trouble"]}}, {"LOWER": {"IN": ["sleep", "sleeping"]}}],
            [{"LOWER": "sleeping"}, {"LOWER": {"IN": ["too", "all"]}}, {"LOWER": {"IN": ["much", "day"]}}],
            [{"LEMMA": "wake"}, {"LOWER": {"IN": ["up", "at"]}}, {"LOWER": "night"}],
        ]
    },
    "A5": {
        "id": "psychomotor",
        "name": "Psychomotor agitation or retardation",
        "keywords": [
            "restless", "can't sit still", "agitated", "fidgety",
            "slowed down", "moving slow", "sluggish", "lethargic"
        ],
        "phrases": [
            "feel restless", "can't sit still", "always moving", "fidgeting",
            "everything is slow", "moving in slow motion", "feel sluggish",
            "body feels heavy", "like moving through water", "thoughts are slow",
            "can't stop pacing", "nervous energy", "feel slowed down"
        ],
        "token_patterns": [
            [{"LOWER": {"IN": ["feel", "feeling"]}}, {"LOWER": {"IN": ["restless", "agitated", "sluggish"]}}],
            [{"LOWER": {"IN": ["can't", "cannot"]}}, {"LOWER": "sit"}, {"LOWER": "still"}],
            [{"LOWER": {"IN": ["moving", "everything"]}}, {"LOWER": {"IN": ["slow", "slowly"]}}],
        ]
    },
    "A6": {
        "id": "fatigue",
        "name": "Fatigue or loss of energy nearly every day",
        "keywords": [
            "tired", "exhausted", "fatigue", "no energy", "drained",
            "worn out", "depleted", "lethargic", "weak"
        ],
        "phrases": [
            "always tired", "no energy", "completely exhausted", "feel drained",
            "worn out", "too tired to", "constant fatigue", "can't do anything",
            "body feels heavy", "no stamina", "feel weak", "depleted",
            "running on empty", "zero energy", "exhausted all the time"
        ],
        "token_patterns": [
            [{"LOWER": {"IN": ["always", "constantly", "completely"]}}, {"LOWER": {"IN": ["tired", "exhausted"]}}],
            [{"LOWER": "no"}, {"LOWER": {"IN": ["energy", "stamina"]}}],
            [{"LEMMA": "feel"}, {"LOWER": {"IN": ["tired", "exhausted", "drained", "weak"]}}],
        ]
    },
    "A7": {
        "id": "worthlessness",
        "name": "Feelings of worthlessness or excessive guilt",
        "keywords": [
            "worthless", "useless", "failure", "guilty", "shame",
            "inadequate", "burden", "let everyone down"
        ],
        "phrases": [
            "feel worthless", "feel useless", "i'm a failure", "feel guilty",
            "everything is my fault", "i'm a burden", "let everyone down",
            "not good enough", "feel inadequate", "ashamed of myself",
            "hate myself", "feel like a failure", "no value", "waste of space",
            "don't deserve", "feel terrible about myself"
        ],
        "token_patterns": [
            [{"LEMMA": "feel"}, {"LOWER": {"IN": ["worthless", "useless", "guilty", "inadequate"]}}],
            [{"LOWER": "i'm"}, {"LOWER": {"IN": ["a", "failure", "worthless", "useless"]}}],
            [{"LOWER": {"IN": ["hate", "ashamed"]}}, {"LOWER": "myself"}],
        ]
    },
    "A8": {
        "id": "concentration",
        "name": "Diminished ability to think, concentrate, or make decisions",
        "keywords": [
            "can't focus", "can't concentrate", "can't think", "brain fog",
            "indecisive", "forgetful", "confused", "distracted"
        ],
        "phrases": [
            "can't focus", "can't concentrate", "trouble thinking", "mind is blank",
            "brain fog", "can't make decisions", "everything is confusing",
            "can't remember", "thoughts are jumbled", "mind won't work",
            "can't think clearly", "hard to focus", "constantly distracted",
            "forget everything", "indecisive about everything"
        ],
        "token_patterns": [
            [{"LOWER": {"IN": ["can't", "cannot", "trouble"]}}, {"LOWER": {"IN": ["focus", "concentrate", "think"]}}],
            [{"LOWER": "brain"}, {"LOWER": "fog"}],
            [{"LOWER": {"IN": ["hard", "difficult"]}}, {"LOWER": "to"}, {"LOWER": {"IN": ["focus", "concentrate"]}}],
        ]
    },
    "A9": {
        "id": "suicidal_ideation",
        "name": "Recurrent thoughts of death, suicidal ideation, or suicide attempt",
        "keywords": [
            "suicide", "kill myself", "end it all", "death", "dying",
            "better off dead", "want to die", "suicidal"
        ],
        "phrases": [
            "want to die", "think about death", "kill myself", "end it all",
            "better off dead", "everyone would be better without me",
            "suicidal thoughts", "plan to die", "thoughts of suicide",
            "wish i was dead", "don't want to live", "end my life",
            "think about dying", "thoughts of ending it"
        ],
        "token_patterns": [
            [{"LOWER": {"IN": ["want", "wish"]}}, {"LOWER": "to"}, {"LOWER": "die"}],
            [{"LOWER": {"IN": ["kill", "end"]}}, {"LOWER": "myself"}],
            [{"LOWER": {"IN": ["think", "thinking", "thoughts"]}}, {"LOWER": "about"}, {"LOWER": {"IN": ["death", "dying", "suicide"]}}],
        ],
        "flag_for_crisis": True
    }
}

# Temporal/duration markers
TEMPORAL_MARKERS = {
    "chronic": ["always", "constantly", "every day", "all the time", "nonstop"],
    "frequent": ["often", "usually", "most days", "frequently", "regularly"],
    "recent": ["lately", "recently", "past few weeks", "for 2 weeks", "past month", "last month"],
    "intermittent": ["sometimes", "occasionally", "now and then", "once in a while"]
}

# Intensity/severity markers
INTENSITY_MARKERS = {
    "high": ["very", "extremely", "severely", "completely", "totally", "absolutely", "incredibly"],
    "moderate": ["quite", "fairly", "somewhat", "pretty", "rather", "moderately"],
    "low": ["a little", "slightly", "mildly", "a bit", "kind of", "sort of"]
}

# Functional impairment keywords
FUNCTIONAL_IMPAIRMENT_KEYWORDS = [
    "can't work", "can't go to work", "stopped working", "quit my job",
    "can't get out of bed", "stopped showering", "don't shower", "hygiene",
    "can't take care", "stopped seeing friends", "isolated", "stay in bed all day",
    "can't function", "can't do anything", "stopped doing", "gave up on",
    "relationships suffering", "marriage falling apart", "losing friends",
    "can't handle", "too much to cope", "falling apart", "life falling apart",
    "can't take care of myself", "neglecting myself", "stopped activities"
]

# Negation patterns
NEGATION_TERMS = ["no", "not", "never", "none", "without", "barely", "hardly", "rarely", "don't", "doesn't", "didn't", "won't", "can't", "cannot"]

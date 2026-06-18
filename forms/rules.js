// Auto-generated — meowREMIX Rule Engine v6.0
// Source song  : wateriswide
// Generated at : 2026-06-17T22:48:08.315830
// DO NOT EDIT — regenerate via: POST /api/audio/rebuild-rules

export const metadata = {
  "source": "wateriswide",
  "generatedAt": "2026-06-17T22:48:08.315830",
  "totalMotifs": 0,
  "totalTransitions": 56,
  "totalSuspensions": 0,
  "voiceLeadingEnabled": true,
  "totalTransitionSmoothnessPairs": 72,
  "totalRhythmFlowRules": 10,
  "engineVersion": "6.0",
  "blendMode": false,
  "noteBuckets": [
    "long",
    "medium",
    "short"
  ],
  "sampleNames": [
    "g",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g2"
  ],
  "totalMomentTokens": 453,
  "tokenVocabSize": 41,
  "tokenBigramContexts": 30
};

export const musicRules = {
  "transitionRules": {
    "G4": [
      {
        "note": "G4",
        "weight": 0.223301
      },
      {
        "note": "A4",
        "weight": 0.213592
      },
      {
        "note": "E4",
        "weight": 0.194175
      },
      {
        "note": "F#4",
        "weight": 0.135922
      },
      {
        "note": "B3",
        "weight": 0.116505
      },
      {
        "note": "D4",
        "weight": 0.07767
      },
      {
        "note": "B4",
        "weight": 0.038835
      }
    ],
    "D4": [
      {
        "note": "D4",
        "weight": 0.289474
      },
      {
        "note": "G4",
        "weight": 0.210526
      },
      {
        "note": "E4",
        "weight": 0.184211
      },
      {
        "note": "B4",
        "weight": 0.078947
      },
      {
        "note": "D5",
        "weight": 0.078947
      },
      {
        "note": "B3",
        "weight": 0.078947
      },
      {
        "note": "C4",
        "weight": 0.078947
      }
    ],
    "A4": [
      {
        "note": "G4",
        "weight": 0.459459
      },
      {
        "note": "B4",
        "weight": 0.405405
      },
      {
        "note": "A4",
        "weight": 0.054054
      },
      {
        "note": "G3",
        "weight": 0.081081
      }
    ],
    "E4": [
      {
        "note": "D4",
        "weight": 0.651163
      },
      {
        "note": "E4",
        "weight": 0.116279
      },
      {
        "note": "C4",
        "weight": 0.139535
      },
      {
        "note": "G4",
        "weight": 0.093023
      }
    ],
    "B3": [
      {
        "note": "B3",
        "weight": 0.317073
      },
      {
        "note": "G4",
        "weight": 0.146341
      },
      {
        "note": "B4",
        "weight": 0.146341
      },
      {
        "note": "C4",
        "weight": 0.146341
      },
      {
        "note": "A3",
        "weight": 0.146341
      },
      {
        "note": "G3",
        "weight": 0.097561
      }
    ],
    "B4": [
      {
        "note": "C5",
        "weight": 0.416667
      },
      {
        "note": "A3",
        "weight": 0.25
      },
      {
        "note": "B4",
        "weight": 0.083333
      },
      {
        "note": "A4",
        "weight": 0.166667
      },
      {
        "note": "D4",
        "weight": 0.083333
      }
    ],
    "C5": [
      {
        "note": "B4",
        "weight": 0.666667
      },
      {
        "note": "D5",
        "weight": 0.333333
      }
    ],
    "C4": [
      {
        "note": "C4",
        "weight": 0.190476
      },
      {
        "note": "B3",
        "weight": 0.380952
      },
      {
        "note": "D4",
        "weight": 0.333334
      },
      {
        "note": "G3",
        "weight": 0.095238
      }
    ],
    "F#4": [
      {
        "note": "G4",
        "weight": 0.7
      },
      {
        "note": "E4",
        "weight": 0.3
      }
    ],
    "E3": [
      {
        "note": "G3",
        "weight": 0.82353
      },
      {
        "note": "E3",
        "weight": 0.17647
      }
    ],
    "A3": [
      {
        "note": "B3",
        "weight": 0.428571
      },
      {
        "note": "A4",
        "weight": 0.428571
      },
      {
        "note": "G3",
        "weight": 0.142857
      }
    ],
    "G3": [
      {
        "note": "G3",
        "weight": 0.1875
      },
      {
        "note": "B3",
        "weight": 0.25
      },
      {
        "note": "G4",
        "weight": 0.1875
      },
      {
        "note": "A3",
        "weight": 0.1875
      },
      {
        "note": "F#3",
        "weight": 0.1875
      }
    ],
    "F#3": [
      {
        "note": "E3",
        "weight": 0.6
      },
      {
        "note": "G3",
        "weight": 0.4
      }
    ],
    "D5": [
      {
        "note": "D4",
        "weight": 0.75
      },
      {
        "note": "D5",
        "weight": 0.25
      }
    ],
    "D3": [
      {
        "note": "B3",
        "weight": 1.0
      }
    ]
  },
  "intervalBias": {
    "-14": 0.026087,
    "-12": 0.008696,
    "-8": 0.02029,
    "-5": 0.02029,
    "-4": 0.017391,
    "-3": 0.037681,
    "-2": 0.144927,
    "-1": 0.081159,
    "0": 0.269566,
    "+1": 0.063768,
    "+2": 0.162319,
    "+3": 0.028985,
    "+4": 0.023189,
    "+5": 0.028985,
    "+8": 0.008696,
    "+9": 0.014493,
    "+12": 0.043478
  },
  "motifs": [],
  "motifsByEntry": {},
  "rhythmPatterns": [
    {
      "pattern": [
        "quarter",
        "dotted-half"
      ],
      "weight": 0.283951
    },
    {
      "pattern": [
        "dotted-half",
        "quarter"
      ],
      "weight": 0.395062
    },
    {
      "pattern": [
        "half",
        "half"
      ],
      "weight": 0.098765
    },
    {
      "pattern": [
        "half",
        "quarter",
        "quarter"
      ],
      "weight": 0.024691
    },
    {
      "pattern": [
        "eighth",
        "eighth",
        "dotted-half"
      ],
      "weight": 0.123457
    },
    {
      "pattern": [
        "dotted-quarter",
        "quarter",
        "dotted-quarter"
      ],
      "weight": 0.061728
    },
    {
      "pattern": [
        "quarter",
        "dotted-quarter",
        "dotted-quarter"
      ],
      "weight": 0.061728
    }
  ],
  "singleDurations": {
    "quarter": 0.324503,
    "eighth": 0.410596,
    "dotted-half": 0.163355,
    "dotted-quarter": 0.0883
  },
  "beatDurationRules": {
    "1.0": [
      {
        "duration": "dotted-half",
        "weight": 0.578125
      },
      {
        "duration": "quarter",
        "weight": 0.375
      },
      {
        "duration": "eighth",
        "weight": 0.046875
      }
    ],
    "2.0": [
      {
        "duration": "quarter",
        "weight": 0.616279
      },
      {
        "duration": "eighth",
        "weight": 0.313953
      },
      {
        "duration": "half",
        "weight": 0.069767
      }
    ],
    "3.0": [
      {
        "duration": "quarter",
        "weight": 0.511628
      },
      {
        "duration": "dotted-quarter",
        "weight": 0.465116
      },
      {
        "duration": "eighth",
        "weight": 0.023256
      }
    ],
    "3.5": [
      {
        "duration": "eighth",
        "weight": 1.0
      }
    ],
    "4.0": [
      {
        "duration": "eighth",
        "weight": 0.95
      },
      {
        "duration": "quarter",
        "weight": 0.05
      }
    ],
    "2.5": [
      {
        "duration": "eighth",
        "weight": 1.0
      }
    ],
    "4.5": [
      {
        "duration": "eighth",
        "weight": 1.0
      }
    ],
    "1.5": [
      {
        "duration": "eighth",
        "weight": 1.0
      }
    ]
  },
  "contourRules": [
    {
      "pattern": [
        "UP",
        "UP"
      ],
      "weight": 0.074903
    },
    {
      "pattern": [
        "UP",
        "SAME"
      ],
      "weight": 0.018482
    },
    {
      "pattern": [
        "SAME",
        "SAME"
      ],
      "weight": 0.053502
    },
    {
      "pattern": [
        "SAME",
        "UP"
      ],
      "weight": 0.016537
    },
    {
      "pattern": [
        "UP",
        "DOWN"
      ],
      "weight": 0.032101
    },
    {
      "pattern": [
        "DOWN",
        "UP"
      ],
      "weight": 0.033074
    },
    {
      "pattern": [
        "SAME",
        "DOWN"
      ],
      "weight": 0.019455
    },
    {
      "pattern": [
        "DOWN",
        "DOWN"
      ],
      "weight": 0.071984
    },
    {
      "pattern": [
        "DOWN",
        "SAME"
      ],
      "weight": 0.018482
    },
    {
      "pattern": [
        "UP",
        "UP",
        "SAME"
      ],
      "weight": 0.007782
    },
    {
      "pattern": [
        "UP",
        "SAME",
        "SAME"
      ],
      "weight": 0.011673
    },
    {
      "pattern": [
        "SAME",
        "SAME",
        "UP"
      ],
      "weight": 0.0107
    },
    {
      "pattern": [
        "SAME",
        "UP",
        "UP"
      ],
      "weight": 0.0107
    },
    {
      "pattern": [
        "UP",
        "UP",
        "UP"
      ],
      "weight": 0.048638
    },
    {
      "pattern": [
        "UP",
        "UP",
        "DOWN"
      ],
      "weight": 0.018482
    },
    {
      "pattern": [
        "UP",
        "DOWN",
        "UP"
      ],
      "weight": 0.008755
    },
    {
      "pattern": [
        "DOWN",
        "UP",
        "SAME"
      ],
      "weight": 0.007782
    },
    {
      "pattern": [
        "SAME",
        "SAME",
        "DOWN"
      ],
      "weight": 0.009728
    },
    {
      "pattern": [
        "SAME",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.015564
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.038911
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "SAME"
      ],
      "weight": 0.012646
    },
    {
      "pattern": [
        "DOWN",
        "SAME",
        "DOWN"
      ],
      "weight": 0.004864
    },
    {
      "pattern": [
        "DOWN",
        "SAME",
        "SAME"
      ],
      "weight": 0.009728
    },
    {
      "pattern": [
        "SAME",
        "SAME",
        "SAME"
      ],
      "weight": 0.032101
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "UP"
      ],
      "weight": 0.020428
    },
    {
      "pattern": [
        "DOWN",
        "UP",
        "UP"
      ],
      "weight": 0.014591
    },
    {
      "pattern": [
        "UP",
        "DOWN",
        "SAME"
      ],
      "weight": 0.005837
    },
    {
      "pattern": [
        "DOWN",
        "SAME",
        "UP"
      ],
      "weight": 0.003891
    },
    {
      "pattern": [
        "UP",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.01751
    },
    {
      "pattern": [
        "DOWN",
        "UP",
        "DOWN"
      ],
      "weight": 0.0107
    },
    {
      "pattern": [
        "UP",
        "SAME",
        "DOWN"
      ],
      "weight": 0.004864
    },
    {
      "pattern": [
        "UP",
        "SAME",
        "UP"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "SAME",
        "DOWN",
        "UP"
      ],
      "weight": 0.003891
    },
    {
      "pattern": [
        "SAME",
        "UP",
        "SAME"
      ],
      "weight": 0.002918
    },
    {
      "pattern": [
        "SAME",
        "UP",
        "DOWN"
      ],
      "weight": 0.002918
    },
    {
      "pattern": [
        "UP",
        "UP",
        "SAME",
        "SAME"
      ],
      "weight": 0.005837
    },
    {
      "pattern": [
        "UP",
        "SAME",
        "SAME",
        "UP"
      ],
      "weight": 0.004864
    },
    {
      "pattern": [
        "SAME",
        "SAME",
        "UP",
        "UP"
      ],
      "weight": 0.007782
    },
    {
      "pattern": [
        "SAME",
        "UP",
        "UP",
        "UP"
      ],
      "weight": 0.005837
    },
    {
      "pattern": [
        "UP",
        "UP",
        "UP",
        "DOWN"
      ],
      "weight": 0.013619
    },
    {
      "pattern": [
        "UP",
        "UP",
        "DOWN",
        "UP"
      ],
      "weight": 0.006809
    },
    {
      "pattern": [
        "UP",
        "DOWN",
        "UP",
        "SAME"
      ],
      "weight": 0.004864
    },
    {
      "pattern": [
        "DOWN",
        "UP",
        "SAME",
        "SAME"
      ],
      "weight": 0.005837
    },
    {
      "pattern": [
        "UP",
        "SAME",
        "SAME",
        "DOWN"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "SAME",
        "SAME",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.008755
    },
    {
      "pattern": [
        "SAME",
        "DOWN",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.007782
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.021401
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "DOWN",
        "SAME"
      ],
      "weight": 0.005837
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "SAME",
        "DOWN"
      ],
      "weight": 0.004864
    },
    {
      "pattern": [
        "DOWN",
        "SAME",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.002918
    },
    {
      "pattern": [
        "SAME",
        "DOWN",
        "DOWN",
        "SAME"
      ],
      "weight": 0.002918
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "SAME",
        "SAME"
      ],
      "weight": 0.004864
    },
    {
      "pattern": [
        "DOWN",
        "SAME",
        "SAME",
        "SAME"
      ],
      "weight": 0.006809
    },
    {
      "pattern": [
        "SAME",
        "SAME",
        "SAME",
        "SAME"
      ],
      "weight": 0.020428
    },
    {
      "pattern": [
        "SAME",
        "SAME",
        "SAME",
        "DOWN"
      ],
      "weight": 0.005837
    },
    {
      "pattern": [
        "SAME",
        "DOWN",
        "DOWN",
        "UP"
      ],
      "weight": 0.004864
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "UP",
        "UP"
      ],
      "weight": 0.011673
    },
    {
      "pattern": [
        "DOWN",
        "UP",
        "UP",
        "UP"
      ],
      "weight": 0.009728
    },
    {
      "pattern": [
        "UP",
        "UP",
        "DOWN",
        "SAME"
      ],
      "weight": 0.002918
    },
    {
      "pattern": [
        "DOWN",
        "SAME",
        "UP",
        "UP"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "UP",
        "UP",
        "UP",
        "UP"
      ],
      "weight": 0.033074
    },
    {
      "pattern": [
        "UP",
        "UP",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.008755
    },
    {
      "pattern": [
        "UP",
        "DOWN",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.009728
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "DOWN",
        "UP"
      ],
      "weight": 0.011673
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "UP",
        "DOWN"
      ],
      "weight": 0.006809
    },
    {
      "pattern": [
        "DOWN",
        "UP",
        "DOWN",
        "UP"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "UP",
        "DOWN",
        "UP",
        "UP"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "UP",
        "SAME",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.003891
    },
    {
      "pattern": [
        "DOWN",
        "UP",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.006809
    },
    {
      "pattern": [
        "SAME",
        "UP",
        "UP",
        "DOWN"
      ],
      "weight": 0.002918
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "UP",
        "SAME"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "UP",
        "DOWN",
        "DOWN",
        "UP"
      ],
      "weight": 0.003891
    },
    {
      "pattern": [
        "UP",
        "SAME",
        "SAME",
        "SAME"
      ],
      "weight": 0.004864
    },
    {
      "pattern": [
        "DOWN",
        "SAME",
        "DOWN",
        "UP"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "DOWN",
        "UP",
        "UP",
        "SAME"
      ],
      "weight": 0.002918
    },
    {
      "pattern": [
        "SAME",
        "SAME",
        "SAME",
        "UP"
      ],
      "weight": 0.004864
    },
    {
      "pattern": [
        "UP",
        "DOWN",
        "DOWN",
        "SAME"
      ],
      "weight": 0.003891
    },
    {
      "pattern": [
        "DOWN",
        "SAME",
        "SAME",
        "DOWN"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "SAME",
        "DOWN",
        "UP",
        "DOWN"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "UP",
        "DOWN",
        "UP",
        "DOWN"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "DOWN",
        "UP",
        "DOWN",
        "SAME"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "UP",
        "DOWN",
        "SAME",
        "SAME"
      ],
      "weight": 0.004864
    },
    {
      "pattern": [
        "SAME",
        "UP",
        "UP",
        "SAME"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "DOWN",
        "DOWN",
        "SAME",
        "UP"
      ],
      "weight": 0.002918
    },
    {
      "pattern": [
        "DOWN",
        "SAME",
        "UP",
        "SAME"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "SAME",
        "UP",
        "SAME",
        "DOWN"
      ],
      "weight": 0.002918
    },
    {
      "pattern": [
        "SAME",
        "SAME",
        "UP",
        "DOWN"
      ],
      "weight": 0.002918
    },
    {
      "pattern": [
        "SAME",
        "UP",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "UP",
        "UP",
        "UP",
        "SAME"
      ],
      "weight": 0.001946
    },
    {
      "pattern": [
        "DOWN",
        "UP",
        "UP",
        "DOWN"
      ],
      "weight": 0.001946
    }
  ],
  "contourArcs": [
    {
      "name": "arch",
      "pattern": [
        "UP",
        "UP",
        "DOWN"
      ],
      "weight": 0.0
    },
    {
      "name": "rise_plateau",
      "pattern": [
        "UP",
        "SAME",
        "DOWN"
      ],
      "weight": 0.0
    },
    {
      "name": "wave",
      "pattern": [
        "UP",
        "DOWN",
        "UP"
      ],
      "weight": 0.9677
    },
    {
      "name": "ascending",
      "pattern": [
        "UP",
        "UP",
        "UP"
      ],
      "weight": 0.0
    },
    {
      "name": "descending",
      "pattern": [
        "DOWN",
        "DOWN",
        "DOWN"
      ],
      "weight": 0.0
    },
    {
      "name": "stasis",
      "pattern": [
        "SAME",
        "SAME"
      ],
      "weight": 0.0323
    }
  ],
  "harmonyRules": {
    "B4": [
      {
        "note": "B3",
        "weight": 0.510204
      },
      {
        "note": "D4",
        "weight": 0.489796
      }
    ],
    "D4": [
      {
        "note": "D4",
        "weight": 2.5
      }
    ],
    "G4": [
      {
        "note": "D4",
        "weight": 0.141667
      },
      {
        "note": "G3",
        "weight": 0.277778
      },
      {
        "note": "B3",
        "weight": 0.25
      }
    ],
    "A4": [
      {
        "note": "A3",
        "weight": 1.0
      }
    ],
    "D5": [
      {
        "note": "D4",
        "weight": 2.5
      }
    ]
  },
  "pitchClassHarmonyRules": {
    "B": [
      {
        "note": "D",
        "weight": 0.615385
      },
      {
        "note": "B",
        "weight": 0.384615
      }
    ],
    "D": [
      {
        "note": "D",
        "weight": 1.0
      }
    ],
    "G": [
      {
        "note": "D",
        "weight": 0.404762
      },
      {
        "note": "B",
        "weight": 0.357143
      },
      {
        "note": "G",
        "weight": 0.238095
      }
    ],
    "A": [
      {
        "note": "A",
        "weight": 1.0
      }
    ]
  },
  "suspensionRules": [],
  "phraseTemplates": {
    "length_distribution": {
      "5": 0.0323,
      "6": 0.1613,
      "1": 0.3226,
      "4": 0.4839
    },
    "typical_tension_arcs": [
      {
        "type": "low",
        "mean_tension": 0.2422
      },
      {
        "type": "medium",
        "mean_tension": 0.3554
      }
    ],
    "typical_contour_shapes": [
      {
        "shape": "multiple_peak",
        "probability": 0.9677
      },
      {
        "shape": "flat",
        "probability": 0.0323
      }
    ]
  },
  "barCenterRules": {
    "D4": [
      {
        "note": "G4",
        "weight": 0.454545
      },
      {
        "note": "D4",
        "weight": 0.181818
      },
      {
        "note": "B4",
        "weight": 0.090909
      },
      {
        "note": "C4",
        "weight": 0.090909
      },
      {
        "note": "B3",
        "weight": 0.090909
      },
      {
        "note": "D5",
        "weight": 0.090909
      }
    ],
    "B4": [
      {
        "note": "G4",
        "weight": 0.666667
      },
      {
        "note": "E3",
        "weight": 0.333333
      }
    ],
    "G4": [
      {
        "note": "D4",
        "weight": 0.5
      },
      {
        "note": "G4",
        "weight": 0.3
      },
      {
        "note": "C5",
        "weight": 0.1
      },
      {
        "note": "B3",
        "weight": 0.1
      }
    ],
    "C5": [
      {
        "note": "A4",
        "weight": 1.0
      }
    ],
    "A4": [
      {
        "note": "B4",
        "weight": 0.333333
      },
      {
        "note": "A4",
        "weight": 0.166667
      },
      {
        "note": "D5",
        "weight": 0.166667
      },
      {
        "note": "A3",
        "weight": 0.166667
      },
      {
        "note": "D4",
        "weight": 0.166667
      }
    ],
    "D5": [
      {
        "note": "A4",
        "weight": 0.666667
      },
      {
        "note": "F#4",
        "weight": 0.333333
      }
    ],
    "B3": [
      {
        "note": "E4",
        "weight": 0.5
      },
      {
        "note": "D4",
        "weight": 0.25
      },
      {
        "note": "C4",
        "weight": 0.25
      }
    ],
    "E4": [
      {
        "note": "A4",
        "weight": 0.666667
      },
      {
        "note": "C4",
        "weight": 0.333333
      }
    ],
    "A3": [
      {
        "note": "D5",
        "weight": 1.0
      }
    ],
    "E3": [
      {
        "note": "D4",
        "weight": 1.0
      }
    ],
    "C4": [
      {
        "note": "B3",
        "weight": 0.666667
      },
      {
        "note": "D4",
        "weight": 0.333333
      }
    ],
    "F#4": [
      {
        "note": "E4",
        "weight": 1.0
      }
    ]
  },
  "styleBiases": {
    "ruleBiases": {
      "transition": 0.3,
      "harmony": 0.6,
      "rhythm": 0.2,
      "motif": 0.4,
      "suspension": 0.5,
      "contour": 0.3
    },
    "styleInterpolationDefaults": {
      "Hallelujah": 0.4,
      "Greensleeves": 0.35,
      "ItIsWell": 0.25
    }
  },
  "smoothnessRules": {
    "transitionSmoothness": {
      "D4": {
        "G4": 0.4,
        "B4": 0.15,
        "D4": 1.0,
        "D5": 0.15,
        "B3": 0.7,
        "C4": 0.95,
        "E4": 0.95,
        "F#4": 0.7
      },
      "G4": {
        "G4": 1.0,
        "A4": 0.95,
        "E4": 0.7,
        "F#4": 0.95,
        "B3": 0.15,
        "B4": 0.7,
        "D4": 0.4
      },
      "A4": {
        "D4": 0.4,
        "B4": 0.95,
        "A4": 1.0,
        "G4": 0.95,
        "G3": 0.15
      },
      "E4": {
        "D4": 0.95,
        "E4": 1.0,
        "G4": 0.7,
        "C4": 0.7,
        "F#4": 0.95
      },
      "F#4": {
        "G4": 0.95,
        "E4": 0.95,
        "D4": 0.7,
        "F#4": 1.0
      },
      "B3": {
        "G4": 0.15,
        "B4": 0.15,
        "C4": 0.95,
        "A3": 0.95,
        "B3": 1.0,
        "G3": 0.7,
        "D4": 0.7
      },
      "B4": {
        "C5": 0.95,
        "A3": 0.15,
        "A4": 0.95,
        "D4": 0.15,
        "B4": 1.0
      },
      "C5": {
        "B4": 0.95,
        "D5": 0.95
      },
      "A3": {
        "A4": 0.15,
        "B3": 0.95,
        "G3": 0.95
      },
      "D5": {
        "D4": 0.15,
        "D5": 1.0
      },
      "G3": {
        "G4": 0.15,
        "B3": 0.7,
        "A3": 0.95,
        "F#3": 0.95,
        "G3": 1.0,
        "C3": 0.4
      },
      "C4": {
        "D4": 0.95,
        "G3": 0.4,
        "C4": 1.0,
        "B3": 0.95,
        "E3": 0.15
      },
      "D3": {
        "B3": 0.15,
        "E3": 0.95,
        "A2": 0.4,
        "D3": 1.0,
        "G3": 0.4
      },
      "F#3": {
        "G3": 0.95,
        "E3": 0.95
      },
      "E3": {
        "G3": 0.7,
        "E3": 1.0,
        "D3": 0.95
      },
      "A2": {
        "A2": 1.0,
        "D3": 0.4
      },
      "C3": {
        "E3": 0.7
      }
    },
    "rhythmFlowRules": [
      {
        "from": "quarter",
        "to": "quarter",
        "smoothness": 0.9
      },
      {
        "from": "quarter",
        "to": "eighth",
        "smoothness": 0.9
      },
      {
        "from": "quarter",
        "to": "dotted-half",
        "smoothness": 0.6
      },
      {
        "from": "quarter",
        "to": "dotted-quarter",
        "smoothness": 0.9
      },
      {
        "from": "eighth",
        "to": "eighth",
        "smoothness": 0.9
      },
      {
        "from": "eighth",
        "to": "quarter",
        "smoothness": 0.9
      },
      {
        "from": "eighth",
        "to": "dotted-quarter",
        "smoothness": 0.6
      },
      {
        "from": "eighth",
        "to": "half",
        "smoothness": 0.6
      },
      {
        "from": "eighth",
        "to": "dotted-half",
        "smoothness": 0.3
      },
      {
        "from": "dotted-quarter",
        "to": "eighth",
        "smoothness": 0.6
      }
    ],
    "smoothnessBias": 0.85
  },
  "verticalHarmonyRules": {
    "preferredIntervals": {},
    "consonanceThreshold": 0.5,
    "preferredIntervalClasses": [
      3,
      4,
      5,
      7,
      8,
      9
    ]
  },
  "noteLengthBuckets": {
    "bucketWeights": {
      "medium": 0.4128,
      "short": 0.4106,
      "long": 0.1766
    },
    "bucketByPitch": {
      "D": {
        "medium": "d",
        "short": "d",
        "long": "d"
      },
      "G": {
        "short": "g",
        "medium": "g",
        "long": "g"
      },
      "A": {
        "medium": "a",
        "short": "a",
        "long": "a"
      },
      "B": {
        "long": "b",
        "medium": "b",
        "short": "b"
      },
      "E": {
        "short": "e",
        "medium": "e",
        "long": "e"
      },
      "F#": {
        "short": "f",
        "medium": "f",
        "long": "f"
      },
      "C": {
        "medium": "c",
        "short": "c"
      }
    },
    "audioPaths": {
      "long": "../projects/audio/notes/long",
      "medium": "../projects/audio/notes/medium",
      "short": "../projects/audio/notes/short"
    },
    "sampleNames": [
      "g",
      "a",
      "b",
      "c",
      "d",
      "e",
      "f",
      "g2"
    ],
    "bucketTransitions": {
      "long": [
        {
          "next": "long",
          "weight": 0.5685
        },
        {
          "next": "medium",
          "weight": 0.4274
        },
        {
          "next": "short",
          "weight": 0.0042
        }
      ],
      "medium": [
        {
          "next": "medium",
          "weight": 0.6745
        },
        {
          "next": "short",
          "weight": 0.1979
        },
        {
          "next": "long",
          "weight": 0.1276
        }
      ],
      "short": [
        {
          "next": "short",
          "weight": 0.7866
        },
        {
          "next": "medium",
          "weight": 0.1466
        },
        {
          "next": "long",
          "weight": 0.0668
        }
      ]
    },
    "bucketRhythmBias": {
      "long": {
        "dotted-half": 0.8163,
        "half": 0.102,
        "whole": 0.0816
      },
      "medium": {
        "quarter": 0.7562,
        "dotted-quarter": 0.2189,
        "half": 0.0149
      },
      "short": {
        "eighth": 0.9548,
        "quarter": 0.0201,
        "dotted-eighth": 0.0151,
        "dotted-quarter": 0.0101
      }
    },
    "bucketTensionMap": {
      "avgTensionByBucket": {
        "medium": 0.1289,
        "short": 0.1527,
        "long": 0.0925
      },
      "pitchBias": {
        "long": {
          "B": 1.4,
          "D": 1.4,
          "G": 1.2,
          "A": 1.4,
          "E": 1.4,
          "F#": 0.8
        },
        "medium": {
          "D": 1.1,
          "A": 1.3,
          "G": 0.9,
          "B": 1.1,
          "C": 1.5,
          "E": 1.3,
          "F#": 1.1
        },
        "short": {
          "G": 0.4,
          "A": 0.8,
          "E": 0.8,
          "D": 0.6,
          "F#": 1.4,
          "B": 0.6,
          "C": 1.0
        }
      }
    }
  },
  "preferenceSignals": {
    "bpm_preference": {
      "avg_disliked_bpm": 90.0,
      "avg_liked_bpm": 90.0
    },
    "by_type": {
      "chord": 27,
      "harmony": 209,
      "phrase": 108,
      "rhythm": 43,
      "sequence": 308,
      "staccato_phrase": 113
    },
    "chord_signals": {
      "top_disliked": [
        {
          "disliked_count": 1,
          "harmony_pc": "D",
          "like_rate": 0.0,
          "liked_count": 0,
          "melody_pc": "G",
          "pad_pc": "D-",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "harmony_pc": "E",
          "like_rate": 0.0,
          "liked_count": 0,
          "melody_pc": "A",
          "pad_pc": "G",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "harmony_pc": "D",
          "like_rate": 0.0,
          "liked_count": 0,
          "melody_pc": "G",
          "pad_pc": "E-",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "harmony_pc": "B-",
          "like_rate": 0.0,
          "liked_count": 0,
          "melody_pc": "C#",
          "pad_pc": "D",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "harmony_pc": "D--",
          "like_rate": 0.0,
          "liked_count": 0,
          "melody_pc": "D--",
          "pad_pc": "C",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "harmony_pc": "G--",
          "like_rate": 0.0,
          "liked_count": 0,
          "melody_pc": "G--",
          "pad_pc": "B-",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "harmony_pc": "G",
          "like_rate": 0.0,
          "liked_count": 0,
          "melody_pc": "C",
          "pad_pc": "F",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "harmony_pc": "A",
          "like_rate": 0.0,
          "liked_count": 0,
          "melody_pc": "C",
          "pad_pc": "G",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "harmony_pc": "B-",
          "like_rate": 0.0,
          "liked_count": 0,
          "melody_pc": "B-",
          "pad_pc": "D",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "harmony_pc": "B",
          "like_rate": 0.0,
          "liked_count": 0,
          "melody_pc": "D#",
          "pad_pc": "D",
          "preference_score": -1.0
        }
      ],
      "top_liked": [
        {
          "disliked_count": 0,
          "harmony_pc": "D",
          "like_rate": 1.0,
          "liked_count": 1,
          "melody_pc": "D",
          "pad_pc": "G",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "harmony_pc": "D",
          "like_rate": 1.0,
          "liked_count": 1,
          "melody_pc": "E",
          "pad_pc": "B-",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "harmony_pc": "E--",
          "like_rate": 1.0,
          "liked_count": 1,
          "melody_pc": "E--",
          "pad_pc": "C",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "harmony_pc": "B--",
          "like_rate": 1.0,
          "liked_count": 1,
          "melody_pc": "B--",
          "pad_pc": "D",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "harmony_pc": "F",
          "like_rate": 1.0,
          "liked_count": 1,
          "melody_pc": "A",
          "pad_pc": "B-",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "harmony_pc": "E-",
          "like_rate": 1.0,
          "liked_count": 1,
          "melody_pc": "E-",
          "pad_pc": "E-",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "harmony_pc": "A",
          "like_rate": 1.0,
          "liked_count": 1,
          "melody_pc": "D",
          "pad_pc": "D",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "harmony_pc": "C",
          "like_rate": 1.0,
          "liked_count": 1,
          "melody_pc": "C",
          "pad_pc": "E-",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "harmony_pc": "C--",
          "like_rate": 1.0,
          "liked_count": 1,
          "melody_pc": "C--",
          "pad_pc": "B-",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "harmony_pc": "A-",
          "like_rate": 1.0,
          "liked_count": 1,
          "melody_pc": "A-",
          "pad_pc": "B-",
          "preference_score": 1.0
        }
      ],
      "total_ratings": 27
    },
    "dislike_count": 386,
    "disliked_patterns": {
      "avg_bucket_dist": {
        "long": 0.2902,
        "medium": 0.4264,
        "short": 0.3206
      },
      "avg_pitch_variety": 6.9888,
      "avg_tension": 0.2478,
      "count": 89
    },
    "harmony_signals": {
      "top_disliked": [
        {
          "disliked_count": 2,
          "like_rate": 0.0,
          "liked_count": 0,
          "note_a": "D--",
          "note_b": "B",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "like_rate": 0.0,
          "liked_count": 0,
          "note_a": "D-",
          "note_b": "B-",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "like_rate": 0.0,
          "liked_count": 0,
          "note_a": "C",
          "note_b": "E",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "like_rate": 0.0,
          "liked_count": 0,
          "note_a": "G-",
          "note_b": "C",
          "preference_score": -1.0
        },
        {
          "disliked_count": 2,
          "like_rate": 0.0,
          "liked_count": 0,
          "note_a": "G-",
          "note_b": "D",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "like_rate": 0.0,
          "liked_count": 0,
          "note_a": "E-",
          "note_b": "F-",
          "preference_score": -1.0
        },
        {
          "disliked_count": 2,
          "like_rate": 0.0,
          "liked_count": 0,
          "note_a": "E",
          "note_b": "G",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "like_rate": 0.0,
          "liked_count": 0,
          "note_a": "D--",
          "note_b": "A",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "like_rate": 0.0,
          "liked_count": 0,
          "note_a": "D-",
          "note_b": "F",
          "preference_score": -1.0
        },
        {
          "disliked_count": 1,
          "like_rate": 0.0,
          "liked_count": 0,
          "note_a": "D-",
          "note_b": "A",
          "preference_score": -1.0
        }
      ],
      "top_liked": [
        {
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 4,
          "note_a": "D",
          "note_b": "D",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 1,
          "note_a": "A--",
          "note_b": "G",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 1,
          "note_a": "E",
          "note_b": "E",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 1,
          "note_a": "D--",
          "note_b": "G--",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 1,
          "note_a": "E-",
          "note_b": "G",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 1,
          "note_a": "A#",
          "note_b": "C#",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 1,
          "note_a": "E--",
          "note_b": "C-",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 1,
          "note_a": "D#",
          "note_b": "F#",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 4,
          "note_a": "F",
          "note_b": "F",
          "preference_score": 1.0
        },
        {
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 2,
          "note_a": "B--",
          "note_b": "B--",
          "preference_score": 1.0
        }
      ],
      "total_ratings": 209
    },
    "like_count": 422,
    "liked_patterns": {
      "avg_bucket_dist": {
        "long": 0.4073,
        "medium": 0.3959,
        "short": 0.3446
      },
      "avg_pitch_variety": 5.4211,
      "avg_tension": 0.2365,
      "count": 19
    },
    "note_transition_signals": {
      "top_disliked": [
        {
          "disliked_count": 1,
          "from": "F#3",
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "F3"
        },
        {
          "disliked_count": 1,
          "from": "F#4",
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "E4"
        },
        {
          "disliked_count": 1,
          "from": "E-3",
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "A--4"
        },
        {
          "disliked_count": 1,
          "from": "D--6",
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "G-5"
        },
        {
          "disliked_count": 2,
          "from": "D4",
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "E-4"
        },
        {
          "disliked_count": 1,
          "from": "F5",
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "F#4"
        },
        {
          "disliked_count": 1,
          "from": "E--4",
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "D4"
        },
        {
          "disliked_count": 7,
          "from": "A4",
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "D4"
        },
        {
          "disliked_count": 1,
          "from": "A--3",
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "D--4"
        },
        {
          "disliked_count": 1,
          "from": "A5",
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "C4"
        }
      ],
      "top_liked": [
        {
          "disliked_count": 0,
          "from": "G-",
          "liked_count": 4,
          "preference_score": 1.0,
          "to": "E-"
        },
        {
          "disliked_count": 0,
          "from": "C3",
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "F4"
        },
        {
          "disliked_count": 0,
          "from": "D4",
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "E-3"
        },
        {
          "disliked_count": 0,
          "from": "A4",
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "E--7"
        },
        {
          "disliked_count": 0,
          "from": "B-2",
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "B-2"
        },
        {
          "disliked_count": 0,
          "from": "D",
          "liked_count": 2,
          "preference_score": 1.0,
          "to": "B-"
        },
        {
          "disliked_count": 0,
          "from": "F4",
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "E4"
        },
        {
          "disliked_count": 0,
          "from": "A-",
          "liked_count": 3.0,
          "preference_score": 1.0,
          "to": "D-"
        },
        {
          "disliked_count": 0,
          "from": "A4",
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "B--5"
        },
        {
          "disliked_count": 0,
          "from": "D-3",
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "A4"
        }
      ]
    },
    "overall_like_rate": 0.5223,
    "phrase_signals": {
      "05594a7e-d21f-4efe-86f5-541f052abfe1": {
        "avg_tension": 0.2643,
        "bucket_dist": {
          "long": 0.1429,
          "medium": 0.3571,
          "short": 0.5
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 3,
        "preference_score": -1.0
      },
      "0835adb0-f43d-44ad-b342-c2a52d35c053": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.25,
          "medium": 0.25,
          "short": 0.5
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "0c65b9d1-bcee-41ea-b0b4-98c6a94af4b2": {
        "avg_tension": 0.1,
        "bucket_dist": {
          "long": 0.2222,
          "medium": 0.5556,
          "short": 0.2222
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "13458643-f1d1-4c99-a7a8-7b5957d5420d": {
        "avg_tension": 0.1909,
        "bucket_dist": {
          "long": 0.3636,
          "medium": 0.4545,
          "short": 0.1818
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "1503f463-b467-4a4c-aade-2d98f014a2a2": {
        "avg_tension": 0.3273,
        "bucket_dist": {
          "long": 0.2727,
          "medium": 0.4545,
          "short": 0.2727
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "18fe97ce-088a-4376-a9d6-0c765a7a1467": {
        "avg_tension": 0.2333,
        "bucket_dist": {
          "long": 0.1667,
          "medium": 0.5,
          "short": 0.3333
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "1aa64bd3-f3ad-4806-86ce-0e5ca174d938": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.2727,
          "medium": 0.3636,
          "short": 0.3636
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 4,
        "preference_score": -1.0
      },
      "1c8a0b2c-e071-4f19-86a9-a18421fdfb93": {
        "avg_tension": 0.2167,
        "bucket_dist": {
          "long": 0.25,
          "medium": 0.1667,
          "short": 0.5833
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "220b1082-13e1-4adb-b408-21fc6727b879": {
        "avg_tension": 0.215,
        "bucket_dist": {
          "long": 0.45,
          "medium": 0.3,
          "short": 0.25
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "26ae7151-8197-4338-9129-c7bb899fa54f": {
        "avg_tension": 0.1444,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.6667
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "2899b853-890f-4db7-896d-dc3fa058cdab": {
        "avg_tension": 0.1455,
        "bucket_dist": {
          "long": 0.4545,
          "medium": 0.0909,
          "short": 0.4545
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "28be37cb-fa39-42a3-a3ac-8c365a3a99b8": {
        "avg_tension": 0.2143,
        "bucket_dist": {
          "long": 0.2857,
          "medium": 0.5714,
          "short": 0.1429
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "2bb28a92-b4d6-45e2-b4f8-75e7243b42f8": {
        "avg_tension": 0.1875,
        "bucket_dist": {
          "long": 0.5,
          "medium": 0.5
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 7,
        "preference_score": 1.0
      },
      "2c7331f7-2060-4aef-bab6-030243485897": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.375,
          "medium": 0.5,
          "short": 0.125
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 4,
        "preference_score": -1.0
      },
      "2cc0f973-17a0-4d59-bac6-242afef06d18": {
        "avg_tension": 0.3154,
        "bucket_dist": {
          "long": 0.2308,
          "medium": 0.3077,
          "short": 0.4615
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "30be7756-d48a-4796-9759-a851d33e1b44": {
        "avg_tension": 0.2364,
        "bucket_dist": {
          "long": 0.3636,
          "medium": 0.2727,
          "short": 0.3636
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "35d62482-b46d-4840-a023-ab862b63718f": {
        "avg_tension": 0.3333,
        "bucket_dist": {
          "long": 0.4444,
          "medium": 0.3333,
          "short": 0.2222
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 4,
        "preference_score": -1.0
      },
      "37f6660e-8782-4fd7-9933-90aefe8568bd": {
        "avg_tension": 0.08,
        "bucket_dist": {
          "long": 0.3,
          "medium": 0.3,
          "short": 0.4
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 5,
        "preference_score": 1.0
      },
      "38836647-19d1-4645-a5a5-015599d54f2a": {
        "avg_tension": 0.3667,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.5556,
          "short": 0.1111
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 5,
        "preference_score": 1.0
      },
      "39ff717d-f1a8-4e43-8195-210b7b588430": {
        "avg_tension": 0.2632,
        "bucket_dist": {
          "long": 0.1053,
          "medium": 0.2632,
          "short": 0.6316
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 8,
        "preference_score": -1.0
      },
      "3afb5d2a-af1c-41fa-8851-760b6c1d3726": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.25,
          "short": 0.4167
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 8,
        "preference_score": -1.0
      },
      "3afe616c-4517-4954-ae1f-5fd7e822fd56": {
        "avg_tension": 0.2375,
        "bucket_dist": {
          "long": 0.5,
          "medium": 0.5
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 6,
        "preference_score": 1.0
      },
      "3c857d41-628d-4d86-a505-6f342d9ccdbf": {
        "avg_tension": 0.2583,
        "bucket_dist": {
          "long": 0.25,
          "medium": 0.3333,
          "short": 0.4167
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 5,
        "preference_score": 1.0
      },
      "3ca58b72-d735-4c4f-9893-71ed38a65b9b": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.1818,
          "medium": 0.6364,
          "short": 0.1818
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 10,
        "preference_score": -1.0
      },
      "40110917-15e7-4d90-9c54-742e78abb3b4": {
        "avg_tension": 0.2692,
        "bucket_dist": {
          "long": 0.3077,
          "medium": 0.3077,
          "short": 0.3846
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 7,
        "preference_score": 1.0
      },
      "40d92ee1-b934-4ab0-97cb-cd39556755dd": {
        "avg_tension": 0.33,
        "bucket_dist": {
          "long": 0.3,
          "medium": 0.5,
          "short": 0.2
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 5,
        "preference_score": 1.0
      },
      "42396356-eec5-4a1e-849a-0d219200dd8d": {
        "avg_tension": 0.2545,
        "bucket_dist": {
          "long": 0.1818,
          "medium": 0.6364,
          "short": 0.1818
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 3,
        "preference_score": -1.0
      },
      "435be924-c10d-4766-be30-5cd81cdb6bf0": {
        "avg_tension": 0.2909,
        "bucket_dist": {
          "long": 0.1818,
          "medium": 0.5455,
          "short": 0.2727
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 5,
        "preference_score": -1.0
      },
      "489e87d9-5fb2-418b-ba63-f5c5ad4649e0": {
        "avg_tension": 0.2583,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.25,
          "short": 0.4167
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 5,
        "preference_score": -1.0
      },
      "48f27f97-4866-42bd-be89-d79a80a57107": {
        "avg_tension": 0.225,
        "bucket_dist": {
          "long": 0.125,
          "medium": 0.25,
          "short": 0.625
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "49e68b96-4309-4d48-8c98-7f7269e0eca4": {
        "avg_tension": 0.2455,
        "bucket_dist": {
          "long": 0.2727,
          "medium": 0.6364,
          "short": 0.0909
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "4c61d20b-71b6-482e-aecf-90edae41eafc": {
        "avg_tension": 0.31,
        "bucket_dist": {
          "long": 0.3,
          "medium": 0.4,
          "short": 0.3
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "4cb36397-397f-4949-8c1a-5f767c6cb58d": {
        "avg_tension": 0.2462,
        "bucket_dist": {
          "long": 0.2308,
          "medium": 0.3077,
          "short": 0.4615
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "4de86db6-bd7a-4252-8a86-1935f357db5f": {
        "avg_tension": 0.2455,
        "bucket_dist": {
          "long": 0.2727,
          "medium": 0.4545,
          "short": 0.2727
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 5,
        "preference_score": -1.0
      },
      "4ef629df-89c4-4c98-8a86-ab97c02b16e0": {
        "avg_tension": 0.3091,
        "bucket_dist": {
          "long": 0.1818,
          "medium": 0.6364,
          "short": 0.1818
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "4f165cfa-73cf-4f97-ad19-0d48a5bd65fa": {
        "avg_tension": 0.3034,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.2667,
          "short": 0.4
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 15,
        "preference_score": -1.0
      },
      "53c0169b-0135-4c60-90f2-cc450b0c13a6": {
        "avg_tension": 0.23,
        "bucket_dist": {
          "long": 0.2,
          "medium": 0.4,
          "short": 0.4
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 4,
        "preference_score": -1.0
      },
      "5467e528-5235-4b2b-9ab1-63dabfbbbf30": {
        "avg_tension": 0.26,
        "bucket_dist": {
          "long": 1.0
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 4,
        "preference_score": 1.0
      },
      "59076b00-3ca2-41f4-9dbd-ce2b05884668": {
        "avg_tension": 0.26,
        "bucket_dist": {
          "long": 0.2667,
          "medium": 0.2,
          "short": 0.5333
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "594501f7-4b82-48ff-842e-509cd5cc0eba": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.3,
          "medium": 0.3,
          "short": 0.4
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 8,
        "preference_score": -1.0
      },
      "5ca599d7-071c-459e-b63e-acb582a06529": {
        "avg_tension": 0.1,
        "bucket_dist": {
          "long": 0.3636,
          "medium": 0.1818,
          "short": 0.4545
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 5,
        "preference_score": -1.0
      },
      "5d30c002-5647-48a3-a1b9-a01284529c4c": {
        "avg_tension": 0.2429,
        "bucket_dist": {
          "long": 0.1905,
          "medium": 0.5238,
          "short": 0.2857
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 15,
        "preference_score": -1.0
      },
      "5e0508d4-658b-4bcc-8288-9752b29b35c6": {
        "avg_tension": 0.2929,
        "bucket_dist": {
          "long": 0.2143,
          "medium": 0.2143,
          "short": 0.5714
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 3,
        "preference_score": 1.0
      },
      "601bfb97-bf57-43db-a9ad-75756a95e15e": {
        "avg_tension": 0.2333,
        "bucket_dist": {
          "long": 0.4444,
          "medium": 0.4444,
          "short": 0.1111
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 2,
        "preference_score": -1.0
      },
      "6140b276-b752-4ff5-8e2f-a1a1a2541bb8": {
        "avg_tension": 0.2842,
        "bucket_dist": {
          "long": 0.4211,
          "medium": 0.3684,
          "short": 0.2105
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 8,
        "preference_score": -1.0
      },
      "61f9d0e4-6e9d-44f4-af88-23f0fed9172a": {
        "avg_tension": 0.31,
        "bucket_dist": {
          "long": 0.35,
          "medium": 0.25,
          "short": 0.4
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 11,
        "preference_score": -1.0
      },
      "6249e82d-eee1-4091-bf4a-885856cfb089": {
        "avg_tension": 0.15,
        "bucket_dist": {
          "long": 0.375,
          "medium": 0.625
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "6a29e5c3-f435-469f-83dd-9474240f8735": {
        "avg_tension": 0.4556,
        "bucket_dist": {
          "long": 0.4444,
          "medium": 0.4444,
          "short": 0.1111
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "6ae3e97b-109f-4e4b-9347-934e7ca85689": {
        "avg_tension": 0.32,
        "bucket_dist": {
          "long": 0.1333,
          "medium": 0.4,
          "short": 0.4667
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 4,
        "preference_score": 1.0
      },
      "701909be-ecc7-4bc6-a94f-7386ded0d737": {
        "avg_tension": 0.2556,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.6667
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 3,
        "preference_score": 1.0
      },
      "72bb483f-05d5-43a6-b9b0-d4b1bf21df02": {
        "avg_tension": 0.35,
        "bucket_dist": {
          "long": 0.5,
          "medium": 0.5
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 3,
        "preference_score": -1.0
      },
      "748923c1-6a28-4ec9-8c34-1cfa4353979f": {
        "avg_tension": 0.3417,
        "bucket_dist": {
          "long": 0.1667,
          "medium": 0.4167,
          "short": 0.4167
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 6,
        "preference_score": 1.0
      },
      "74e8ae5f-3769-4ae8-a36d-26bd4e5ff21a": {
        "avg_tension": 0.1769,
        "bucket_dist": {
          "long": 0.2308,
          "medium": 0.3846,
          "short": 0.3846
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 10,
        "preference_score": 1.0
      },
      "76110181-4e63-4934-a3a7-19d10c7d577f": {
        "avg_tension": 0.2,
        "bucket_dist": {
          "long": 0.3,
          "medium": 0.1,
          "short": 0.6
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "77bd15a7-b600-4ee6-97f5-0733bb04ed13": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.3636,
          "medium": 0.2727,
          "short": 0.3636
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "796bd74c-bb36-4d93-a7cd-4774cd5ef022": {
        "avg_tension": 0.2083,
        "bucket_dist": {
          "long": 0.25,
          "medium": 0.3333,
          "short": 0.4167
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "7a1d7bb5-6a5c-4699-88ee-6457dc4b7073": {
        "avg_tension": 0.2556,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.4444,
          "short": 0.2222
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "7d0cc39a-7622-470e-b383-dbe720708507": {
        "avg_tension": 0.2818,
        "bucket_dist": {
          "long": 0.1818,
          "medium": 0.7273,
          "short": 0.0909
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "7dcad7df-abce-4e8c-b323-b677d1eb4554": {
        "avg_tension": 0.29,
        "bucket_dist": {
          "long": 0.3,
          "medium": 0.5,
          "short": 0.2
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "81bbbcf5-52fb-4f62-a9b8-a16e05558f60": {
        "avg_tension": 0.1778,
        "bucket_dist": {
          "long": 0.5556,
          "medium": 0.4444
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "89236998-5d67-40f7-8aea-fc7225c0cac4": {
        "avg_tension": 0.1333,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.4444,
          "short": 0.2222
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 6,
        "preference_score": 1.0
      },
      "89a4cf40-ef57-4ef9-9e7c-fff1defd5af1": {
        "avg_tension": 0.1462,
        "bucket_dist": {
          "long": 0.1538,
          "medium": 0.5385,
          "short": 0.3077
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 4,
        "preference_score": -1.0
      },
      "8a690df2-7934-4e3e-88e6-3dc6b74376a8": {
        "avg_tension": 0.1727,
        "bucket_dist": {
          "long": 0.2727,
          "medium": 0.3636,
          "short": 0.3636
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 8,
        "preference_score": -1.0
      },
      "8e35d750-3951-40e1-a17b-1370a873a4d1": {
        "avg_tension": 0.1733,
        "bucket_dist": {
          "long": 0.1333,
          "medium": 0.3333,
          "short": 0.5333
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 10,
        "preference_score": -1.0
      },
      "8ef93403-de1e-4146-9b73-a5971a5e8908": {
        "avg_tension": 0.3136,
        "bucket_dist": {
          "long": 0.3636,
          "medium": 0.2273,
          "short": 0.4091
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 10,
        "preference_score": -1.0
      },
      "93b061e5-34d8-418a-bb6f-afa01175f35e": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.2,
          "medium": 0.7,
          "short": 0.1
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "9836c68d-717b-4d3f-a567-0903e6dcdcdf": {
        "avg_tension": 0.2333,
        "bucket_dist": {
          "long": 0.1667,
          "medium": 0.5833,
          "short": 0.25
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 10,
        "preference_score": -1.0
      },
      "98d46dd9-e42b-458d-9af5-93b66de8e7bd": {
        "avg_tension": 0.16,
        "bucket_dist": {
          "long": 0.1,
          "medium": 0.7,
          "short": 0.2
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 8,
        "preference_score": -1.0
      },
      "9969501d-bba9-409f-bb29-3ba48d28fadf": {
        "avg_tension": 0.2857,
        "bucket_dist": {
          "long": 0.7143,
          "medium": 0.2857
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 3,
        "preference_score": 1.0
      },
      "9a310e09-2a63-4254-bcaf-425235a98585": {
        "avg_tension": 0.3538,
        "bucket_dist": {
          "long": 0.2308,
          "medium": 0.3077,
          "short": 0.4615
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 7,
        "preference_score": 1.0
      },
      "9b1cb605-2ef0-43a2-89d3-87bbb3ae2d93": {
        "avg_tension": 0.2455,
        "bucket_dist": {
          "long": 0.1818,
          "medium": 0.6364,
          "short": 0.1818
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "9c2fa89c-0bc6-478b-a8ce-59ca9a16125f": {
        "avg_tension": 0.2833,
        "bucket_dist": {
          "long": 0.0833,
          "medium": 0.4167,
          "short": 0.5
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "9cbe7f0e-4c54-4ccb-9410-04bd67ff95a4": {
        "avg_tension": 0.3222,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.5556,
          "short": 0.1111
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "a08c1019-fd36-4786-afa0-61d4577e70ca": {
        "avg_tension": 0.1375,
        "bucket_dist": {
          "long": 0.375,
          "medium": 0.375,
          "short": 0.25
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 5,
        "preference_score": -1.0
      },
      "a7f7f98d-6d86-45a1-8387-2add3ed83bfc": {
        "avg_tension": 0.275,
        "bucket_dist": {
          "long": 0.25,
          "medium": 0.4167,
          "short": 0.3333
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "a9223e09-d893-43bc-a1c9-ecc26529304f": {
        "avg_tension": 0.14,
        "bucket_dist": {
          "long": 0.3,
          "medium": 0.5,
          "short": 0.2
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "aa285ab6-e1cf-44db-81ef-588a847b3ac9": {
        "avg_tension": 0.1778,
        "bucket_dist": {
          "long": 0.4444,
          "medium": 0.5556
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "aef26d7f-7ea7-4fbc-99c5-c5f49ae73c41": {
        "avg_tension": 0.33,
        "bucket_dist": {
          "long": 0.2,
          "medium": 0.8
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "aff2e014-b1be-44a8-9bb2-d8dbd0d90a60": {
        "avg_tension": 0.17,
        "bucket_dist": {
          "long": 0.2,
          "medium": 0.7,
          "short": 0.1
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 7,
        "preference_score": 1.0
      },
      "b2201283-b996-44b8-a748-82661f64e4f1": {
        "avg_tension": 0.2444,
        "bucket_dist": {
          "long": 0.4444,
          "medium": 0.4444,
          "short": 0.1111
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 5,
        "preference_score": -1.0
      },
      "b7515b8c-17e6-4205-9ee0-df76069d6dd1": {
        "avg_tension": 0.2643,
        "bucket_dist": {
          "long": 0.1429,
          "medium": 0.3571,
          "short": 0.5
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "bcadb6a6-a28e-4cca-8111-3ed3dde58e77": {
        "avg_tension": 0.0571,
        "bucket_dist": {
          "long": 0.8571,
          "medium": 0.1429
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 5,
        "preference_score": 1.0
      },
      "bf15c64f-1508-44f2-85bb-f21676164494": {
        "avg_tension": 0.2437,
        "bucket_dist": {
          "long": 0.1875,
          "medium": 0.1875,
          "short": 0.625
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "bf691e2f-bbb2-4a35-9ff9-72d1cce285eb": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.1333,
          "medium": 0.3333,
          "short": 0.5333
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "c041ba6b-355f-4720-a6a8-5da689c1d954": {
        "avg_tension": 0.275,
        "bucket_dist": {
          "long": 0.5,
          "medium": 0.375,
          "short": 0.125
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "c5a825f3-04b7-4603-8514-3bfe969cd7ef": {
        "avg_tension": 0.1556,
        "bucket_dist": {
          "long": 0.5556,
          "medium": 0.2222,
          "short": 0.2222
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 5,
        "preference_score": -1.0
      },
      "ca1ed25b-fcb8-4864-a9d1-5ee2335fd989": {
        "avg_tension": 0.1111,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.5556,
          "short": 0.1111
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 8,
        "preference_score": -1.0
      },
      "cd8fbc68-fc82-4bae-901b-00b29dda6902": {
        "avg_tension": 0.2083,
        "bucket_dist": {
          "long": 0.1667,
          "medium": 0.5833,
          "short": 0.25
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 10,
        "preference_score": -1.0
      },
      "cdbd55de-9827-4361-a1af-c56de9e3fcef": {
        "avg_tension": 0.39,
        "bucket_dist": {
          "long": 0.4,
          "medium": 0.3,
          "short": 0.3
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "d50ce051-114e-48d8-ba20-fddb573bfb1a": {
        "avg_tension": 0.2636,
        "bucket_dist": {
          "long": 0.2727,
          "medium": 0.5455,
          "short": 0.1818
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "d7555060-927a-47e1-b97f-bc505ac8d760": {
        "avg_tension": 0.3571,
        "bucket_dist": {
          "long": 0.5714,
          "medium": 0.4286
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 4,
        "preference_score": -1.0
      },
      "d8609155-c534-49d3-80f2-bca130fa6f7d": {
        "avg_tension": 0.25,
        "bucket_dist": {
          "long": 0.2,
          "medium": 0.7,
          "short": 0.1
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 6,
        "preference_score": -1.0
      },
      "da8e5273-c511-4e5e-beac-69f82c9b101d": {
        "avg_tension": 0.25,
        "bucket_dist": {
          "long": 0.3,
          "medium": 0.6,
          "short": 0.1
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "ddaec19f-88b0-4c57-9e99-bb6da5f07018": {
        "avg_tension": 0.2812,
        "bucket_dist": {
          "long": 0.25,
          "medium": 0.0625,
          "short": 0.6875
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 11,
        "preference_score": -1.0
      },
      "e5b8bb01-a9e9-4167-883c-60b083211ac8": {
        "avg_tension": 0.2615,
        "bucket_dist": {
          "long": 0.1538,
          "medium": 0.4615,
          "short": 0.3846
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 5,
        "preference_score": -1.0
      },
      "e7c46d40-482f-4435-94f6-fe23a78216df": {
        "avg_tension": 0.1895,
        "bucket_dist": {
          "long": 0.4737,
          "medium": 0.2632,
          "short": 0.2632
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "e8ad45ab-f618-4b25-97a9-a4e054218a8e": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.3636,
          "medium": 0.1818,
          "short": 0.4545
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 4,
        "preference_score": -1.0
      },
      "ea7c5ff9-e649-4d63-b04b-9c62e8418e13": {
        "avg_tension": 0.2286,
        "bucket_dist": {
          "long": 0.1429,
          "medium": 0.4286,
          "short": 0.4286
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 12,
        "preference_score": -1.0
      },
      "ed204f78-2f98-4525-b429-547def399d56": {
        "avg_tension": 0.2636,
        "bucket_dist": {
          "long": 0.1818,
          "medium": 0.5455,
          "short": 0.2727
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "eeb2551f-34a5-4744-86b7-85c367485305": {
        "avg_tension": 0.175,
        "bucket_dist": {
          "long": 0.1875,
          "medium": 0.25,
          "short": 0.5625
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 10,
        "preference_score": -1.0
      },
      "f12cf168-7c2d-4e61-ba17-51501865744d": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.5,
          "medium": 0.5
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 3,
        "preference_score": -1.0
      },
      "f3d72c01-9f63-400c-a192-6f4eea15552e": {
        "avg_tension": 0.1875,
        "bucket_dist": {
          "long": 0.75,
          "short": 0.25
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 4,
        "preference_score": -1.0
      },
      "f460f25c-5abf-4c4d-8034-af524e728699": {
        "avg_tension": 0.2,
        "bucket_dist": {
          "long": 0.2222,
          "medium": 0.7778
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "f461ed74-b3ad-4e5a-a22b-738cd6385a9e": {
        "avg_tension": 0.2091,
        "bucket_dist": {
          "long": 0.1818,
          "medium": 0.7273,
          "short": 0.0909
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      "f6307a71-b8f3-40e3-aa43-5dffc24e8b93": {
        "avg_tension": 0.325,
        "bucket_dist": {
          "long": 0.1667,
          "medium": 0.4167,
          "short": 0.4167
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "fa34c908-e68d-4d01-8933-bf51ccf78bd0": {
        "avg_tension": 0.1167,
        "bucket_dist": {
          "long": 0.8333,
          "medium": 0.1667
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "pitch_variety": 5,
        "preference_score": 1.0
      },
      "fd8b8c51-35b7-4ee7-b281-2f958a3b43e1": {
        "avg_tension": 0.0917,
        "bucket_dist": {
          "long": 0.25,
          "medium": 0.5833,
          "short": 0.1667
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 7,
        "preference_score": -1.0
      },
      "fecf85e7-fe01-486f-b083-be7a870792f2": {
        "avg_tension": 0.3,
        "bucket_dist": {
          "long": 0.1875,
          "medium": 0.25,
          "short": 0.5625
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "pitch_variety": 8,
        "preference_score": -1.0
      }
    },
    "rhythm_signals": {
      "top_disliked": [
        {
          "beats": [
            1,
            1,
            2
          ],
          "disliked_count": 1,
          "like_rate": 0.0,
          "liked_count": 0,
          "pattern_key": "[1, 1, 2]",
          "preference_score": -1.0
        },
        {
          "beats": [
            1,
            1,
            1,
            1
          ],
          "disliked_count": 4,
          "like_rate": 0.0,
          "liked_count": 0,
          "pattern_key": "[1, 1, 1, 1]",
          "preference_score": -1.0
        },
        {
          "beats": [
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5
          ],
          "disliked_count": 4,
          "like_rate": 0.0,
          "liked_count": 0,
          "pattern_key": "[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
          "preference_score": -1.0
        },
        {
          "beats": [
            4,
            4
          ],
          "disliked_count": 1,
          "like_rate": 0.6667,
          "liked_count": 2,
          "pattern_key": "[4, 4]",
          "preference_score": 0.3333
        },
        {
          "beats": [
            1,
            0.5,
            0.5,
            0.5,
            0.5,
            1
          ],
          "disliked_count": 1,
          "like_rate": 0.8,
          "liked_count": 4,
          "pattern_key": "[1, 0.5, 0.5, 0.5, 0.5, 1]",
          "preference_score": 0.6
        }
      ],
      "top_liked": [
        {
          "beats": [
            2,
            2
          ],
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 4,
          "pattern_key": "[2, 2]",
          "preference_score": 1.0
        },
        {
          "beats": [
            1.5,
            0.5,
            1.5,
            0.5
          ],
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 4,
          "pattern_key": "[1.5, 0.5, 1.5, 0.5]",
          "preference_score": 1.0
        },
        {
          "beats": [
            0.5,
            1,
            1,
            1,
            0.5
          ],
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 3,
          "pattern_key": "[0.5, 1, 1, 1, 0.5]",
          "preference_score": 1.0
        },
        {
          "beats": [
            1,
            1
          ],
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 8,
          "pattern_key": "[1, 1]",
          "preference_score": 1.0
        },
        {
          "beats": [
            0.67,
            0.33,
            0.67,
            0.33,
            0.67,
            0.33,
            0.67,
            0.33
          ],
          "disliked_count": 0,
          "like_rate": 1.0,
          "liked_count": 1,
          "pattern_key": "[0.67, 0.33, 0.67, 0.33, 0.67, 0.33, 0.67, 0.33]",
          "preference_score": 1.0
        }
      ],
      "total_ratings": 43
    },
    "sequence_signals": {
      "top_disliked": [
        {
          "disliked_count": 1,
          "from": "D-",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "source": "sequence",
          "to": "C"
        },
        {
          "disliked_count": 2,
          "from": "C",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "source": "sequence",
          "to": "E"
        },
        {
          "disliked_count": 1,
          "from": "C-",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "source": "sequence",
          "to": "G-"
        },
        {
          "disliked_count": 1,
          "from": "F-",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "source": "sequence",
          "to": "F-"
        },
        {
          "disliked_count": 1,
          "from": "B-",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "source": "sequence",
          "to": "G"
        },
        {
          "disliked_count": 2,
          "from": "E-",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "source": "sequence",
          "to": "F"
        },
        {
          "disliked_count": 1,
          "from": "E--",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "source": "sequence",
          "to": "F-"
        },
        {
          "disliked_count": 1,
          "from": "E",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "source": "sequence",
          "to": "F#"
        },
        {
          "disliked_count": 1,
          "from": "A-",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "source": "sequence",
          "to": "B-"
        },
        {
          "disliked_count": 2,
          "from": "C#",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "source": "sequence",
          "to": "C#"
        }
      ],
      "top_liked": [
        {
          "disliked_count": 0,
          "from": "G-",
          "like_rate": 1.0,
          "liked_count": 2,
          "preference_score": 1.0,
          "source": "sequence",
          "to": "E-"
        },
        {
          "disliked_count": 0,
          "from": "E-",
          "like_rate": 1.0,
          "liked_count": 3,
          "preference_score": 1.0,
          "source": "sequence",
          "to": "G"
        },
        {
          "disliked_count": 0,
          "from": "E--",
          "like_rate": 1.0,
          "liked_count": 4,
          "preference_score": 1.0,
          "source": "sequence",
          "to": "C-"
        },
        {
          "disliked_count": 0,
          "from": "C#",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "source": "sequence",
          "to": "A"
        },
        {
          "disliked_count": 0,
          "from": "G-",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "source": "sequence",
          "to": "B--"
        },
        {
          "disliked_count": 0,
          "from": "A",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "source": "sequence",
          "to": "E"
        },
        {
          "disliked_count": 0,
          "from": "G-",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "source": "sequence",
          "to": "E--"
        },
        {
          "disliked_count": 0,
          "from": "D-",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "source": "sequence",
          "to": "E-"
        },
        {
          "disliked_count": 0,
          "from": "B--",
          "like_rate": 1.0,
          "liked_count": 3,
          "preference_score": 1.0,
          "source": "sequence",
          "to": "B--"
        },
        {
          "disliked_count": 0,
          "from": "B--",
          "like_rate": 1.0,
          "liked_count": 6,
          "preference_score": 1.0,
          "source": "sequence",
          "to": "E--"
        }
      ],
      "total_ratings": 308
    },
    "slider_correlations": {
      "disliked": {
        "long_volume": 0.2027,
        "medium_volume": 0.5438,
        "short_volume": 0.3715,
        "suspension_risk": 0.3
      },
      "liked": {
        "long_volume": 0.2,
        "medium_volume": 0.5711,
        "short_volume": 0.3342,
        "suspension_risk": 0.3
      }
    },
    "staccato_signals": {
      "top_disliked": [
        {
          "disliked_count": 2,
          "from": "D",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "E"
        },
        {
          "disliked_count": 1,
          "from": "D-",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "C"
        },
        {
          "disliked_count": 2,
          "from": "B",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "E"
        },
        {
          "disliked_count": 3,
          "from": "C--",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "C--"
        },
        {
          "disliked_count": 1,
          "from": "D",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "F"
        },
        {
          "disliked_count": 4,
          "from": "F-",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "C-"
        },
        {
          "disliked_count": 2,
          "from": "A--",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "F-"
        },
        {
          "disliked_count": 5,
          "from": "C-",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "G-"
        },
        {
          "disliked_count": 1,
          "from": "B",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "G"
        },
        {
          "disliked_count": 2,
          "from": "C",
          "like_rate": 0.0,
          "liked_count": 0,
          "preference_score": -1.0,
          "to": "G"
        }
      ],
      "top_liked": [
        {
          "disliked_count": 0,
          "from": "F-",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "G-"
        },
        {
          "disliked_count": 0,
          "from": "E--",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "G--"
        },
        {
          "disliked_count": 0,
          "from": "A",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "F"
        },
        {
          "disliked_count": 0,
          "from": "G-",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "E--"
        },
        {
          "disliked_count": 0,
          "from": "D-",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "E-"
        },
        {
          "disliked_count": 0,
          "from": "A-",
          "like_rate": 1.0,
          "liked_count": 3,
          "preference_score": 1.0,
          "to": "G-"
        },
        {
          "disliked_count": 0,
          "from": "B--",
          "like_rate": 1.0,
          "liked_count": 3,
          "preference_score": 1.0,
          "to": "B--"
        },
        {
          "disliked_count": 0,
          "from": "D--",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "B--"
        },
        {
          "disliked_count": 0,
          "from": "G",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "F"
        },
        {
          "disliked_count": 0,
          "from": "G-",
          "like_rate": 1.0,
          "liked_count": 1,
          "preference_score": 1.0,
          "to": "D--"
        }
      ],
      "total_ratings": 113
    },
    "top_disliked_phrases": [
      {
        "avg_tension": 0.2437,
        "bucket_dist": {
          "long": 0.1875,
          "medium": 0.1875,
          "short": 0.625
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "phrase_id": "bf15c64f-1508-44f2-85bb-f21676164494",
        "pitch_variety": 9,
        "preference_score": -1.0
      },
      {
        "avg_tension": 0.3034,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.2667,
          "short": 0.4
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "phrase_id": "4f165cfa-73cf-4f97-ad19-0d48a5bd65fa",
        "pitch_variety": 15,
        "preference_score": -1.0
      },
      {
        "avg_tension": 0.31,
        "bucket_dist": {
          "long": 0.35,
          "medium": 0.25,
          "short": 0.4
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "phrase_id": "61f9d0e4-6e9d-44f4-af88-23f0fed9172a",
        "pitch_variety": 11,
        "preference_score": -1.0
      },
      {
        "avg_tension": 0.2429,
        "bucket_dist": {
          "long": 0.1905,
          "medium": 0.5238,
          "short": 0.2857
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "phrase_id": "5d30c002-5647-48a3-a1b9-a01284529c4c",
        "pitch_variety": 15,
        "preference_score": -1.0
      },
      {
        "avg_tension": 0.3136,
        "bucket_dist": {
          "long": 0.3636,
          "medium": 0.2273,
          "short": 0.4091
        },
        "dislike_count": 1,
        "like_count": 0,
        "like_rate": 0.0,
        "phrase_id": "8ef93403-de1e-4146-9b73-a5971a5e8908",
        "pitch_variety": 10,
        "preference_score": -1.0
      }
    ],
    "top_liked_phrases": [
      {
        "avg_tension": 0.2857,
        "bucket_dist": {
          "long": 0.7143,
          "medium": 0.2857
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "phrase_id": "9969501d-bba9-409f-bb29-3ba48d28fadf",
        "pitch_variety": 3,
        "preference_score": 1.0
      },
      {
        "avg_tension": 0.3667,
        "bucket_dist": {
          "long": 0.3333,
          "medium": 0.5556,
          "short": 0.1111
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "phrase_id": "38836647-19d1-4645-a5a5-015599d54f2a",
        "pitch_variety": 5,
        "preference_score": 1.0
      },
      {
        "avg_tension": 0.08,
        "bucket_dist": {
          "long": 0.3,
          "medium": 0.3,
          "short": 0.4
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "phrase_id": "37f6660e-8782-4fd7-9933-90aefe8568bd",
        "pitch_variety": 5,
        "preference_score": 1.0
      },
      {
        "avg_tension": 0.32,
        "bucket_dist": {
          "long": 0.1333,
          "medium": 0.4,
          "short": 0.4667
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "phrase_id": "6ae3e97b-109f-4e4b-9347-934e7ca85689",
        "pitch_variety": 4,
        "preference_score": 1.0
      },
      {
        "avg_tension": 0.1875,
        "bucket_dist": {
          "long": 0.5,
          "medium": 0.5
        },
        "dislike_count": 0,
        "like_count": 1,
        "like_rate": 1.0,
        "phrase_id": "2bb28a92-b4d6-45e2-b4f8-75e7243b42f8",
        "pitch_variety": 7,
        "preference_score": 1.0
      }
    ],
    "total_ratings": 808
  },
  "trajectoryTensionCurve": {
    "curveSamples": [
      {
        "progress": 0.0,
        "tensionTarget": 0.3963
      },
      {
        "progress": 0.05,
        "tensionTarget": 0.3994
      },
      {
        "progress": 0.1,
        "tensionTarget": 0.405
      },
      {
        "progress": 0.15,
        "tensionTarget": 0.4118
      },
      {
        "progress": 0.2,
        "tensionTarget": 0.4224
      },
      {
        "progress": 0.25,
        "tensionTarget": 0.4413
      },
      {
        "progress": 0.3,
        "tensionTarget": 0.4748
      },
      {
        "progress": 0.35,
        "tensionTarget": 0.5262
      },
      {
        "progress": 0.4,
        "tensionTarget": 0.5898
      },
      {
        "progress": 0.45,
        "tensionTarget": 0.6477
      },
      {
        "progress": 0.5,
        "tensionTarget": 0.677
      },
      {
        "progress": 0.55,
        "tensionTarget": 0.6645
      },
      {
        "progress": 0.6,
        "tensionTarget": 0.6159
      },
      {
        "progress": 0.65,
        "tensionTarget": 0.552
      },
      {
        "progress": 0.7,
        "tensionTarget": 0.4941
      },
      {
        "progress": 0.75,
        "tensionTarget": 0.4531
      },
      {
        "progress": 0.8,
        "tensionTarget": 0.4289
      },
      {
        "progress": 0.85,
        "tensionTarget": 0.4155
      },
      {
        "progress": 0.9,
        "tensionTarget": 0.2517
      },
      {
        "progress": 0.95,
        "tensionTarget": 0.2458
      }
    ],
    "climaxLocation": 0.5104,
    "climaxTension": 0.677,
    "baselineTension": 0.2458,
    "bucketTargetsByProgress": {
      "0.0": {
        "long": 0.2722,
        "medium": 0.4549,
        "short": 0.6549
      },
      "0.1": {
        "long": 0.2755,
        "medium": 0.4594,
        "short": 0.6594
      },
      "0.2": {
        "long": 0.2822,
        "medium": 0.4684,
        "short": 0.6684
      },
      "0.3": {
        "long": 0.3023,
        "medium": 0.4955,
        "short": 0.6955
      },
      "0.4": {
        "long": 0.3465,
        "medium": 0.5549,
        "short": 0.7549
      },
      "0.5": {
        "long": 0.38,
        "medium": 0.6,
        "short": 0.8
      },
      "0.6": {
        "long": 0.3565,
        "medium": 0.5684,
        "short": 0.7684
      },
      "0.7": {
        "long": 0.3098,
        "medium": 0.5054,
        "short": 0.7054
      },
      "0.8": {
        "long": 0.2847,
        "medium": 0.4717,
        "short": 0.6717
      },
      "0.9": {
        "long": 0.2167,
        "medium": 0.3801,
        "short": 0.5801
      },
      "1.0": {
        "long": 0.2144,
        "medium": 0.3771,
        "short": 0.5771
      }
    },
    "sectionTargets": [
      {
        "role": "development",
        "start": 0.0208,
        "end": 1.0,
        "target": 0.3963
      }
    ]
  },
  "tensionHoldRules": {
    "holdProbability": 0.2855,
    "holdTensionFloor": 0.2894,
    "phraseHoldThreshold": 0.72,
    "probabilityByRole": {
      "setup": 0.0514,
      "development": 0.1998,
      "climax": 0.314,
      "resolution": 0.0714
    },
    "cadenceProfiles": {
      "half": {
        "prebeatBeats": 2.4,
        "silenceBeats": 1.6,
        "releaseEnabled": false,
        "observedCount": 1
      },
      "perfect_authentic": {
        "prebeatBeats": 1.0,
        "silenceBeats": 0.5,
        "releaseEnabled": true,
        "observedCount": 0
      },
      "deceptive": {
        "prebeatBeats": 0.5,
        "silenceBeats": 0.75,
        "releaseEnabled": true,
        "observedCount": 0
      },
      "plagal": {
        "prebeatBeats": 1.5,
        "silenceBeats": 0.5,
        "releaseEnabled": true,
        "observedCount": 0
      },
      "default": {
        "prebeatBeats": 1.0,
        "silenceBeats": 0.75,
        "releaseEnabled": false,
        "observedCount": 0
      }
    },
    "tensionSustainFallback": "D4",
    "maxConsecutiveHolds": 1,
    "minMeasuresBetweenHolds": 4.0,
    "climaxLocation": 0.5104,
    "observedDelayEvents": 6
  },
  "tokenNgramRules": {
    "unigram_probs": {
      "D|4|medium|SAME|2|mid|verse": 0.06622516556291391,
      "G|4|medium|UP|2|mid|verse": 0.0728476821192053,
      "G|4|medium|SAME|2|mid|verse": 0.06181015452538632,
      "A|4|medium|UP|2|mid|verse": 0.05739514348785872,
      "A|4|medium|SAME|2|mid|verse": 0.037527593818984545,
      "B|4|medium|UP|2|mid|verse": 0.04856512141280353,
      "D|4|medium|DOWN|2|mid|verse": 0.0772626931567329,
      "G|3|medium|DOWN|2|mid|verse": 0.06622516556291391,
      "G|4|medium|DOWN|2|mid|verse": 0.03090507726269316,
      "E|4|medium|DOWN|2|mid|verse": 0.03090507726269316,
      "E|4|medium|SAME|2|mid|verse": 0.01545253863134658,
      "F#|4|medium|SAME|2|mid|verse": 0.008830022075055188,
      "B|3|medium|DOWN|2|mid|verse": 0.06622516556291391,
      "B|4|medium|SAME|2|mid|verse": 0.03090507726269316,
      "C|5|medium|SAME|2|mid|verse": 0.017660044150110375,
      "A|3|medium|DOWN|2|mid|verse": 0.02869757174392936,
      "D|5|medium|UP|2|mid|verse": 0.013245033112582781,
      "D|5|medium|SAME|2|mid|verse": 0.008830022075055188,
      "C|5|medium|UP|2|mid|verse": 0.01545253863134658,
      "A|4|medium|DOWN|2|mid|verse": 0.004415011037527594,
      "B|3|medium|SAME|2|mid|verse": 0.03090507726269316,
      "C|4|medium|DOWN|2|mid|verse": 0.037527593818984545,
      "C|4|medium|SAME|2|mid|verse": 0.019867549668874173,
      "E|4|medium|UP|2|mid|verse": 0.01545253863134658,
      "G|3|medium|SAME|2|mid|verse": 0.01545253863134658,
      "D|4|medium|UP|2|mid|verse": 0.017660044150110375,
      "D|3|medium|DOWN|2|mid|verse": 0.013245033112582781,
      "D|3|medium|SAME|2|mid|verse": 0.002207505518763797,
      "F#|4|medium|UP|2|mid|verse": 0.011037527593818985,
      "A|3|medium|SAME|2|mid|verse": 0.006622516556291391,
      "F#|3|medium|DOWN|2|mid|verse": 0.006622516556291391,
      "F#|3|medium|SAME|2|mid|verse": 0.004415011037527594,
      "E|3|medium|DOWN|2|mid|verse": 0.019867549668874173,
      "E|3|medium|SAME|2|mid|verse": 0.006622516556291391,
      "B|3|medium|UP|2|mid|verse": 0.008830022075055188,
      "G|3|medium|UP|2|mid|verse": 0.004415011037527594,
      "F#|4|medium|DOWN|2|mid|verse": 0.008830022075055188,
      "A|2|medium|DOWN|2|mid|verse": 0.004415011037527594,
      "A|3|medium|UP|2|mid|verse": 0.002207505518763797,
      "B|4|medium|DOWN|2|mid|verse": 0.002207505518763797,
      "C|3|medium|DOWN|2|mid|verse": 0.002207505518763797
    },
    "bigram_probs": {
      "D|4|medium|SAME|2|mid|verse": [
        {
          "token": "D|4|medium|SAME|2|mid|verse",
          "prob": 0.5769230769230769,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 0.19230769230769232,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 0.15384615384615385,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.07692307692307693,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|UP|2|mid|verse": [
        {
          "token": "G|4|medium|SAME|2|mid|verse",
          "prob": 0.46875,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 0.3125,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "E|4|medium|DOWN|2|mid|verse",
          "prob": 0.15625,
          "token_data": {
            "pitch_class": "E",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.0625,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|SAME|2|mid|verse": [
        {
          "token": "G|4|medium|SAME|2|mid|verse",
          "prob": 0.32,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 0.28,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "C|4|medium|DOWN|2|mid|verse",
          "prob": 0.16,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "A|4|medium|UP|2|mid|verse",
          "prob": 0.08,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 0.08,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "E|3|medium|DOWN|2|mid|verse",
          "prob": 0.08,
          "token_data": {
            "pitch_class": "E",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|4|medium|UP|2|mid|verse": [
        {
          "token": "A|4|medium|SAME|2|mid|verse",
          "prob": 0.625,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "A|3|medium|DOWN|2|mid|verse",
          "prob": 0.125,
          "token_data": {
            "pitch_class": "A",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "E|4|medium|DOWN|2|mid|verse",
          "prob": 0.125,
          "token_data": {
            "pitch_class": "E",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "F#|4|medium|DOWN|2|mid|verse",
          "prob": 0.125,
          "token_data": {
            "pitch_class": "F#",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|4|medium|SAME|2|mid|verse": [
        {
          "token": "B|4|medium|UP|2|mid|verse",
          "prob": 0.21428571428571427,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|DOWN|2|mid|verse",
          "prob": 0.21428571428571427,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "C|4|medium|DOWN|2|mid|verse",
          "prob": 0.21428571428571427,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 0.21428571428571427,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "A|4|medium|SAME|2|mid|verse",
          "prob": 0.14285714285714285,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|4|medium|UP|2|mid|verse": [
        {
          "token": "B|4|medium|SAME|2|mid|verse",
          "prob": 0.5263157894736842,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|DOWN|2|mid|verse",
          "prob": 0.3157894736842105,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 0.15789473684210525,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|4|medium|DOWN|2|mid|verse": [
        {
          "token": "D|4|medium|SAME|2|mid|verse",
          "prob": 0.3125,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 0.3125,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 0.15625,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|3|medium|DOWN|2|mid|verse",
          "prob": 0.15625,
          "token_data": {
            "pitch_class": "D",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|4|medium|UP|2|mid|verse",
          "prob": 0.0625,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|3|medium|DOWN|2|mid|verse": [
        {
          "token": "G|3|medium|SAME|2|mid|verse",
          "prob": 0.2692307692307692,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "A|4|medium|UP|2|mid|verse",
          "prob": 0.23076923076923078,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 0.23076923076923078,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|4|medium|UP|2|mid|verse",
          "prob": 0.11538461538461539,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "C|5|medium|UP|2|mid|verse",
          "prob": 0.07692307692307693,
          "token_data": {
            "pitch_class": "C",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|5|medium|UP|2|mid|verse",
          "prob": 0.07692307692307693,
          "token_data": {
            "pitch_class": "D",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|DOWN|2|mid|verse": [
        {
          "token": "G|4|medium|SAME|2|mid|verse",
          "prob": 0.2857142857142857,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.2857142857142857,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 0.2857142857142857,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "E|4|medium|DOWN|2|mid|verse",
          "prob": 0.14285714285714285,
          "token_data": {
            "pitch_class": "E",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|4|medium|DOWN|2|mid|verse": [
        {
          "token": "C|4|medium|DOWN|2|mid|verse",
          "prob": 0.42857142857142855,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "E|4|medium|SAME|2|mid|verse",
          "prob": 0.2857142857142857,
          "token_data": {
            "pitch_class": "E",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 0.14285714285714285,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "A|2|medium|DOWN|2|mid|verse",
          "prob": 0.14285714285714285,
          "token_data": {
            "pitch_class": "A",
            "octave": 2,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|4|medium|SAME|2|mid|verse": [
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.6,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 0.4,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|4|medium|SAME|2|mid|verse": [
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 0.3,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.3,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "C|5|medium|SAME|2|mid|verse",
          "prob": 0.2,
          "token_data": {
            "pitch_class": "C",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|4|medium|SAME|2|mid|verse",
          "prob": 0.2,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|5|medium|SAME|2|mid|verse": [
        {
          "token": "C|5|medium|SAME|2|mid|verse",
          "prob": 0.3333333333333333,
          "token_data": {
            "pitch_class": "C",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|4|medium|SAME|2|mid|verse",
          "prob": 0.3333333333333333,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "A|3|medium|DOWN|2|mid|verse",
          "prob": 0.3333333333333333,
          "token_data": {
            "pitch_class": "A",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|3|medium|DOWN|2|mid|verse": [
        {
          "token": "A|4|medium|UP|2|mid|verse",
          "prob": 0.5454545454545454,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "A|3|medium|SAME|2|mid|verse",
          "prob": 0.2727272727272727,
          "token_data": {
            "pitch_class": "A",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "F#|4|medium|UP|2|mid|verse",
          "prob": 0.18181818181818182,
          "token_data": {
            "pitch_class": "F#",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|5|medium|UP|2|mid|verse": [
        {
          "token": "D|5|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|5|medium|UP|2|mid|verse": [
        {
          "token": "C|5|medium|SAME|2|mid|verse",
          "prob": 0.6666666666666666,
          "token_data": {
            "pitch_class": "C",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|DOWN|2|mid|verse",
          "prob": 0.3333333333333333,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|3|medium|DOWN|2|mid|verse": [
        {
          "token": "B|3|medium|SAME|2|mid|verse",
          "prob": 0.4642857142857143,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.21428571428571427,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|4|medium|UP|2|mid|verse",
          "prob": 0.17857142857142858,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "A|4|medium|UP|2|mid|verse",
          "prob": 0.07142857142857142,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "E|3|medium|DOWN|2|mid|verse",
          "prob": 0.07142857142857142,
          "token_data": {
            "pitch_class": "E",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|4|medium|DOWN|2|mid|verse": [
        {
          "token": "C|4|medium|SAME|2|mid|verse",
          "prob": 0.6923076923076923,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "E|3|medium|DOWN|2|mid|verse",
          "prob": 0.3076923076923077,
          "token_data": {
            "pitch_class": "E",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|4|medium|SAME|2|mid|verse": [
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.42857142857142855,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|4|medium|UP|2|mid|verse",
          "prob": 0.2857142857142857,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 0.2857142857142857,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|4|medium|UP|2|mid|verse": [
        {
          "token": "C|4|medium|DOWN|2|mid|verse",
          "prob": 0.5714285714285714,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "E|4|medium|SAME|2|mid|verse",
          "prob": 0.42857142857142855,
          "token_data": {
            "pitch_class": "E",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|3|medium|SAME|2|mid|verse": [
        {
          "token": "D|4|medium|UP|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "C|5|medium|UP|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "C",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|4|medium|UP|2|mid|verse": [
        {
          "token": "D|4|medium|SAME|2|mid|verse",
          "prob": 0.5714285714285714,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 0.42857142857142855,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|3|medium|SAME|2|mid|verse": [
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.45454545454545453,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|4|medium|UP|2|mid|verse",
          "prob": 0.2727272727272727,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 0.2727272727272727,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "F#|4|medium|UP|2|mid|verse": [
        {
          "token": "F#|4|medium|SAME|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "F#",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "F#|3|medium|DOWN|2|mid|verse": [
        {
          "token": "F#|3|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "F#",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|5|medium|SAME|2|mid|verse": [
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|3|medium|DOWN|2|mid|verse": [
        {
          "token": "E|3|medium|SAME|2|mid|verse",
          "prob": 0.6,
          "token_data": {
            "pitch_class": "E",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "E|4|medium|UP|2|mid|verse",
          "prob": 0.4,
          "token_data": {
            "pitch_class": "E",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|3|medium|UP|2|mid|verse": [
        {
          "token": "A|4|medium|UP|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "F#|4|medium|DOWN|2|mid|verse": [
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|3|medium|DOWN|2|mid|verse": [
        {
          "token": "C|5|medium|UP|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "C",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ]
    },
    "trigram_probs": {
      "D|4|medium|SAME|2|mid|verse -> D|4|medium|SAME|2|mid|verse": [
        {
          "token": "D|4|medium|SAME|2|mid|verse",
          "prob": 0.6153846153846154,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 0.23076923076923078,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 0.15384615384615385,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|4|medium|SAME|2|mid|verse -> G|4|medium|UP|2|mid|verse": [
        {
          "token": "G|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|UP|2|mid|verse -> G|4|medium|SAME|2|mid|verse": [
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 0.38461538461538464,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|SAME|2|mid|verse",
          "prob": 0.23076923076923078,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "C|4|medium|DOWN|2|mid|verse",
          "prob": 0.23076923076923078,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "E|3|medium|DOWN|2|mid|verse",
          "prob": 0.15384615384615385,
          "token_data": {
            "pitch_class": "E",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|SAME|2|mid|verse -> G|4|medium|SAME|2|mid|verse": [
        {
          "token": "G|4|medium|SAME|2|mid|verse",
          "prob": 0.6666666666666666,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "A|4|medium|UP|2|mid|verse",
          "prob": 0.3333333333333333,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|SAME|2|mid|verse -> A|4|medium|UP|2|mid|verse": [
        {
          "token": "A|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|4|medium|UP|2|mid|verse -> A|4|medium|SAME|2|mid|verse": [
        {
          "token": "B|4|medium|UP|2|mid|verse",
          "prob": 0.2727272727272727,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "C|4|medium|DOWN|2|mid|verse",
          "prob": 0.2727272727272727,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 0.2727272727272727,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|DOWN|2|mid|verse",
          "prob": 0.18181818181818182,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|3|medium|DOWN|2|mid|verse -> A|4|medium|UP|2|mid|verse": [
        {
          "token": "A|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|4|medium|SAME|2|mid|verse -> G|4|medium|DOWN|2|mid|verse": [
        {
          "token": "G|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|4|medium|DOWN|2|mid|verse -> E|4|medium|SAME|2|mid|verse": [
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|4|medium|SAME|2|mid|verse -> D|4|medium|DOWN|2|mid|verse": [
        {
          "token": "D|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|4|medium|DOWN|2|mid|verse -> D|4|medium|SAME|2|mid|verse": [
        {
          "token": "D|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|4|medium|SAME|2|mid|verse -> B|4|medium|UP|2|mid|verse": [
        {
          "token": "B|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|4|medium|UP|2|mid|verse -> B|4|medium|SAME|2|mid|verse": [
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 0.375,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.375,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "C|5|medium|SAME|2|mid|verse",
          "prob": 0.25,
          "token_data": {
            "pitch_class": "C",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|4|medium|SAME|2|mid|verse -> C|5|medium|SAME|2|mid|verse": [
        {
          "token": "C|5|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "C",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|5|medium|SAME|2|mid|verse -> B|4|medium|SAME|2|mid|verse": [
        {
          "token": "B|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|3|medium|DOWN|2|mid|verse -> A|4|medium|UP|2|mid|verse": [
        {
          "token": "A|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|3|medium|DOWN|2|mid|verse -> C|5|medium|UP|2|mid|verse": [
        {
          "token": "C|5|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "C",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|3|medium|DOWN|2|mid|verse -> G|4|medium|UP|2|mid|verse": [
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 0.6,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|SAME|2|mid|verse",
          "prob": 0.4,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|SAME|2|mid|verse -> B|3|medium|DOWN|2|mid|verse": [
        {
          "token": "B|3|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|4|medium|SAME|2|mid|verse -> C|4|medium|DOWN|2|mid|verse": [
        {
          "token": "C|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|4|medium|DOWN|2|mid|verse -> C|4|medium|SAME|2|mid|verse": [
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.42857142857142855,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|4|medium|UP|2|mid|verse",
          "prob": 0.2857142857142857,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 0.2857142857142857,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|4|medium|SAME|2|mid|verse -> B|4|medium|UP|2|mid|verse": [
        {
          "token": "B|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|4|medium|SAME|2|mid|verse -> D|4|medium|DOWN|2|mid|verse": [
        {
          "token": "D|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|4|medium|SAME|2|mid|verse -> D|4|medium|DOWN|2|mid|verse": [
        {
          "token": "D|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|SAME|2|mid|verse -> C|4|medium|DOWN|2|mid|verse": [
        {
          "token": "C|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|4|medium|UP|2|mid|verse -> E|4|medium|SAME|2|mid|verse": [
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|4|medium|SAME|2|mid|verse -> G|3|medium|DOWN|2|mid|verse": [
        {
          "token": "G|3|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|3|medium|DOWN|2|mid|verse -> G|3|medium|SAME|2|mid|verse": [
        {
          "token": "D|4|medium|UP|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "C|5|medium|UP|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "C",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|3|medium|SAME|2|mid|verse -> D|4|medium|UP|2|mid|verse": [
        {
          "token": "D|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|4|medium|UP|2|mid|verse -> D|4|medium|SAME|2|mid|verse": [
        {
          "token": "D|4|medium|SAME|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|4|medium|SAME|2|mid|verse -> B|3|medium|DOWN|2|mid|verse": [
        {
          "token": "B|3|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|3|medium|DOWN|2|mid|verse -> B|3|medium|SAME|2|mid|verse": [
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "D|4|medium|UP|2|mid|verse",
          "prob": 0.3,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 0.2,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|3|medium|SAME|2|mid|verse -> D|4|medium|UP|2|mid|verse": [
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|4|medium|SAME|2|mid|verse -> G|3|medium|DOWN|2|mid|verse": [
        {
          "token": "G|3|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|5|medium|UP|2|mid|verse -> C|5|medium|SAME|2|mid|verse": [
        {
          "token": "A|3|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "A",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|5|medium|SAME|2|mid|verse -> A|3|medium|DOWN|2|mid|verse": [
        {
          "token": "A|3|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "A",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|5|medium|UP|2|mid|verse -> D|5|medium|SAME|2|mid|verse": [
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|5|medium|SAME|2|mid|verse -> B|3|medium|DOWN|2|mid|verse": [
        {
          "token": "B|3|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|SAME|2|mid|verse -> E|3|medium|DOWN|2|mid|verse": [
        {
          "token": "E|3|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "E",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|4|medium|SAME|2|mid|verse -> G|4|medium|UP|2|mid|verse": [
        {
          "token": "G|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|3|medium|SAME|2|mid|verse -> G|4|medium|UP|2|mid|verse": [
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|UP|2|mid|verse -> D|4|medium|DOWN|2|mid|verse": [
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 0.75,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 0.25,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|4|medium|UP|2|mid|verse -> G|4|medium|UP|2|mid|verse": [
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|4|medium|DOWN|2|mid|verse -> B|3|medium|DOWN|2|mid|verse": [
        {
          "token": "G|3|medium|DOWN|2|mid|verse",
          "prob": 0.625,
          "token_data": {
            "pitch_class": "G",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|4|medium|UP|2|mid|verse",
          "prob": 0.375,
          "token_data": {
            "pitch_class": "B",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|3|medium|DOWN|2|mid|verse -> G|3|medium|DOWN|2|mid|verse": [
        {
          "token": "G|4|medium|UP|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "A|4|medium|UP|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "A",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|4|medium|UP|2|mid|verse -> E|4|medium|DOWN|2|mid|verse": [
        {
          "token": "C|4|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|4|medium|UP|2|mid|verse -> G|4|medium|DOWN|2|mid|verse": [
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|DOWN|2|mid|verse -> D|4|medium|DOWN|2|mid|verse": [
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|4|medium|DOWN|2|mid|verse -> G|4|medium|UP|2|mid|verse": [
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "B|3|medium|DOWN|2|mid|verse -> B|4|medium|UP|2|mid|verse": [
        {
          "token": "G|4|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "G",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|4|medium|UP|2|mid|verse -> F#|4|medium|DOWN|2|mid|verse": [
        {
          "token": "D|4|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "F#|4|medium|DOWN|2|mid|verse -> D|4|medium|DOWN|2|mid|verse": [
        {
          "token": "D|3|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|UP|2|mid|verse -> E|4|medium|DOWN|2|mid|verse": [
        {
          "token": "C|4|medium|DOWN|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        },
        {
          "token": "B|3|medium|DOWN|2|mid|verse",
          "prob": 0.5,
          "token_data": {
            "pitch_class": "B",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|4|medium|DOWN|2|mid|verse -> C|4|medium|DOWN|2|mid|verse": [
        {
          "token": "E|3|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "E",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|4|medium|DOWN|2|mid|verse -> E|3|medium|DOWN|2|mid|verse": [
        {
          "token": "E|4|medium|UP|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "E",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|3|medium|DOWN|2|mid|verse -> E|4|medium|UP|2|mid|verse": [
        {
          "token": "C|4|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|4|medium|UP|2|mid|verse -> C|4|medium|DOWN|2|mid|verse": [
        {
          "token": "C|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "C",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "C|4|medium|SAME|2|mid|verse -> G|3|medium|DOWN|2|mid|verse": [
        {
          "token": "D|4|medium|UP|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|3|medium|DOWN|2|mid|verse -> D|4|medium|UP|2|mid|verse": [
        {
          "token": "D|4|medium|SAME|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "SAME",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "E|4|medium|DOWN|2|mid|verse -> B|3|medium|DOWN|2|mid|verse": [
        {
          "token": "E|3|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "E",
            "octave": 3,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "D|4|medium|DOWN|2|mid|verse -> D|3|medium|DOWN|2|mid|verse": [
        {
          "token": "C|5|medium|UP|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "C",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|DOWN|2|mid|verse -> E|4|medium|DOWN|2|mid|verse": [
        {
          "token": "A|2|medium|DOWN|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "A",
            "octave": 2,
            "duration_bucket": "medium",
            "contour": "DOWN",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "A|4|medium|UP|2|mid|verse -> A|3|medium|DOWN|2|mid|verse": [
        {
          "token": "F#|4|medium|UP|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "F#",
            "octave": 4,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ],
      "G|4|medium|DOWN|2|mid|verse -> G|3|medium|DOWN|2|mid|verse": [
        {
          "token": "D|5|medium|UP|2|mid|verse",
          "prob": 1.0,
          "token_data": {
            "pitch_class": "D",
            "octave": 5,
            "duration_bucket": "medium",
            "contour": "UP",
            "tension_bin": 2,
            "phrase_position": "mid",
            "structural_role": "verse"
          }
        }
      ]
    },
    "vocab": {
      "D|4|medium|SAME|2|mid|verse": {
        "pitch_class": "D",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "G|4|medium|UP|2|mid|verse": {
        "pitch_class": "G",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "UP",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "G|4|medium|SAME|2|mid|verse": {
        "pitch_class": "G",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "A|4|medium|UP|2|mid|verse": {
        "pitch_class": "A",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "UP",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "A|4|medium|SAME|2|mid|verse": {
        "pitch_class": "A",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "B|4|medium|UP|2|mid|verse": {
        "pitch_class": "B",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "UP",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "D|4|medium|DOWN|2|mid|verse": {
        "pitch_class": "D",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "G|3|medium|DOWN|2|mid|verse": {
        "pitch_class": "G",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "G|4|medium|DOWN|2|mid|verse": {
        "pitch_class": "G",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "E|4|medium|DOWN|2|mid|verse": {
        "pitch_class": "E",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "E|4|medium|SAME|2|mid|verse": {
        "pitch_class": "E",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "F#|4|medium|SAME|2|mid|verse": {
        "pitch_class": "F#",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "B|3|medium|DOWN|2|mid|verse": {
        "pitch_class": "B",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "B|4|medium|SAME|2|mid|verse": {
        "pitch_class": "B",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "C|5|medium|SAME|2|mid|verse": {
        "pitch_class": "C",
        "octave": 5,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "A|3|medium|DOWN|2|mid|verse": {
        "pitch_class": "A",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "D|5|medium|UP|2|mid|verse": {
        "pitch_class": "D",
        "octave": 5,
        "duration_bucket": "medium",
        "contour": "UP",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "D|5|medium|SAME|2|mid|verse": {
        "pitch_class": "D",
        "octave": 5,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "C|5|medium|UP|2|mid|verse": {
        "pitch_class": "C",
        "octave": 5,
        "duration_bucket": "medium",
        "contour": "UP",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "A|4|medium|DOWN|2|mid|verse": {
        "pitch_class": "A",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "B|3|medium|SAME|2|mid|verse": {
        "pitch_class": "B",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "C|4|medium|DOWN|2|mid|verse": {
        "pitch_class": "C",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "C|4|medium|SAME|2|mid|verse": {
        "pitch_class": "C",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "E|4|medium|UP|2|mid|verse": {
        "pitch_class": "E",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "UP",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "G|3|medium|SAME|2|mid|verse": {
        "pitch_class": "G",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "D|4|medium|UP|2|mid|verse": {
        "pitch_class": "D",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "UP",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "D|3|medium|DOWN|2|mid|verse": {
        "pitch_class": "D",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "D|3|medium|SAME|2|mid|verse": {
        "pitch_class": "D",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "F#|4|medium|UP|2|mid|verse": {
        "pitch_class": "F#",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "UP",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "A|3|medium|SAME|2|mid|verse": {
        "pitch_class": "A",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "F#|3|medium|DOWN|2|mid|verse": {
        "pitch_class": "F#",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "F#|3|medium|SAME|2|mid|verse": {
        "pitch_class": "F#",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "E|3|medium|DOWN|2|mid|verse": {
        "pitch_class": "E",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "E|3|medium|SAME|2|mid|verse": {
        "pitch_class": "E",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "SAME",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "B|3|medium|UP|2|mid|verse": {
        "pitch_class": "B",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "UP",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "G|3|medium|UP|2|mid|verse": {
        "pitch_class": "G",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "UP",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "F#|4|medium|DOWN|2|mid|verse": {
        "pitch_class": "F#",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "A|2|medium|DOWN|2|mid|verse": {
        "pitch_class": "A",
        "octave": 2,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "A|3|medium|UP|2|mid|verse": {
        "pitch_class": "A",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "UP",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "B|4|medium|DOWN|2|mid|verse": {
        "pitch_class": "B",
        "octave": 4,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      },
      "C|3|medium|DOWN|2|mid|verse": {
        "pitch_class": "C",
        "octave": 3,
        "duration_bucket": "medium",
        "contour": "DOWN",
        "tension_bin": 2,
        "phrase_position": "mid",
        "structural_role": "verse"
      }
    }
  }
};

export const ruleLibrary = {
  "schema_version": "6.0",
  "generated_at": "2026-06-17T22:48:08.316480",
  "tempo_independent": true,
  "description": "Compositional rule library \u2013 meowREMIX v6.0.",
  "rule_library": {
    "phrase_destination_rules": {
      "4_bar_phrase": {
        "1": 0.2258,
        "2": 0.0968,
        "3": 0.2581,
        "4": 0.0645,
        "5": 0.2581,
        "6": 0.0968
      }
    },
    "tension_arc_templates": [
      {
        "type": "multiple_peak",
        "frequency": 0.9677,
        "average_duration_beats": 3.3,
        "average_peak_location": 0.2708
      },
      {
        "type": "flat",
        "frequency": 0.0323,
        "average_duration_beats": 6.0,
        "average_peak_location": 0.5165
      }
    ],
    "motif_rules": {
      "average_return_distance": 14.7,
      "variation_probability": 0.0,
      "exact_repeat_probability": 1.0
    },
    "familiarity_model": {
      "reuse_probability": 1.0,
      "variation_probability": 0.0,
      "familiarity_score": 0.7674,
      "novelty_score": 0.2326
    },
    "section_templates": [
      {
        "section_id": "A",
        "average_length_bars": 48.0,
        "cadence_density": 0.2258,
        "tension_profile": {
          "average": 0.2707,
          "peak": 0.6586
        },
        "structural_role": "development"
      }
    ],
    "cadence_rules": {
      "half": 1.0
    },
    "expectation_rules": {
      "delay_probability": 0.1935,
      "average_delay_length": -17.0
    },
    "role_transitions": {
      "setup": {
        "development": 0.72,
        "climax": 0.28
      },
      "development": {
        "climax": 0.55,
        "development": 0.3,
        "resolution": 0.15
      },
      "climax": {
        "resolution": 0.8,
        "development": 0.2
      },
      "resolution": {
        "setup": 0.6,
        "development": 0.4
      }
    },
    "scale_degree_patterns": [
      {
        "pattern": [
          1,
          1
        ],
        "frequency": 0.1613
      },
      {
        "pattern": [
          3,
          5
        ],
        "frequency": 0.129
      },
      {
        "pattern": [
          5,
          2
        ],
        "frequency": 0.0968
      },
      {
        "pattern": [
          2,
          3
        ],
        "frequency": 0.0968
      },
      {
        "pattern": [
          3,
          3
        ],
        "frequency": 0.0968
      },
      {
        "pattern": [
          5,
          5
        ],
        "frequency": 0.0645
      },
      {
        "pattern": [
          1,
          5
        ],
        "frequency": 0.0645
      },
      {
        "pattern": [
          3,
          6
        ],
        "frequency": 0.0645
      },
      {
        "pattern": [
          5,
          1
        ],
        "frequency": 0.0323
      },
      {
        "pattern": [
          2,
          6
        ],
        "frequency": 0.0323
      },
      {
        "pattern": [
          5,
          4
        ],
        "frequency": 0.0323
      },
      {
        "pattern": [
          1,
          4
        ],
        "frequency": 0.0323
      },
      {
        "pattern": [
          3,
          1
        ],
        "frequency": 0.0323
      },
      {
        "pattern": [
          1,
          3
        ],
        "frequency": 0.0323
      },
      {
        "pattern": [
          5,
          3
        ],
        "frequency": 0.0323
      }
    ],
    "song_trajectory_templates": {
      "climax_position_average": 0.5104,
      "resolution_position_average": 0.93
    },
    "emotional_profiles": {
      "profile_A": {
        "stepwise": true
      }
    },
    "rule_priority": {
      "motif_reuse": 0.95,
      "cadence_behavior": 0.88,
      "phrase_destination": 0.85,
      "familiarity": 0.82,
      "tension_arc": 0.8,
      "note_length_bucket": 0.75,
      "trajectory": 0.75,
      "structural_role": 0.7,
      "scale_degree_attraction": 0.6,
      "interval_choice": 0.52
    },
    "rule_sets": {
      "motif_rules": {
        "average_return_distance": 14.7,
        "variation_probability": 0.0,
        "exact_repeat_probability": 1.0
      },
      "phrase_rules": {
        "4_bar_phrase": {
          "1": 0.2258,
          "2": 0.0968,
          "3": 0.2581,
          "4": 0.0645,
          "5": 0.2581,
          "6": 0.0968
        }
      },
      "cadence_rules": {
        "half": 1.0
      },
      "tension_rules": [
        {
          "type": "multiple_peak",
          "frequency": 0.9677,
          "average_duration_beats": 3.3,
          "average_peak_location": 0.2708
        },
        {
          "type": "flat",
          "frequency": 0.0323,
          "average_duration_beats": 6.0,
          "average_peak_location": 0.5165
        }
      ],
      "section_rules": [
        {
          "section_id": "A",
          "average_length_bars": 48.0,
          "cadence_density": 0.2258,
          "tension_profile": {
            "average": 0.2707,
            "peak": 0.6586
          },
          "structural_role": "development"
        }
      ],
      "familiarity_rules": {
        "reuse_probability": 1.0,
        "variation_probability": 0.0,
        "familiarity_score": 0.7674,
        "novelty_score": 0.2326
      },
      "role_rules": {
        "setup": {
          "development": 0.72,
          "climax": 0.28
        },
        "development": {
          "climax": 0.55,
          "development": 0.3,
          "resolution": 0.15
        },
        "climax": {
          "resolution": 0.8,
          "development": 0.2
        },
        "resolution": {
          "setup": 0.6,
          "development": 0.4
        }
      },
      "scale_degree_rules": [
        {
          "pattern": [
            1,
            1
          ],
          "frequency": 0.1613
        },
        {
          "pattern": [
            3,
            5
          ],
          "frequency": 0.129
        },
        {
          "pattern": [
            5,
            2
          ],
          "frequency": 0.0968
        },
        {
          "pattern": [
            2,
            3
          ],
          "frequency": 0.0968
        },
        {
          "pattern": [
            3,
            3
          ],
          "frequency": 0.0968
        },
        {
          "pattern": [
            5,
            5
          ],
          "frequency": 0.0645
        },
        {
          "pattern": [
            1,
            5
          ],
          "frequency": 0.0645
        },
        {
          "pattern": [
            3,
            6
          ],
          "frequency": 0.0645
        },
        {
          "pattern": [
            5,
            1
          ],
          "frequency": 0.0323
        },
        {
          "pattern": [
            2,
            6
          ],
          "frequency": 0.0323
        },
        {
          "pattern": [
            5,
            4
          ],
          "frequency": 0.0323
        },
        {
          "pattern": [
            1,
            4
          ],
          "frequency": 0.0323
        },
        {
          "pattern": [
            3,
            1
          ],
          "frequency": 0.0323
        },
        {
          "pattern": [
            1,
            3
          ],
          "frequency": 0.0323
        },
        {
          "pattern": [
            5,
            3
          ],
          "frequency": 0.0323
        }
      ],
      "trajectory_rules": {
        "climax_position_average": 0.5104,
        "resolution_position_average": 0.93
      },
      "emotional_profiles": {
        "profile_A": {
          "stepwise": true
        }
      }
    },
    "gravity_model": {
      "tonic_pull": 0.81,
      "dominant_pull": 0.63,
      "mediant_pull": 0.41
    },
    "emotional_memory_rules": {
      "average_motif_return_distance": 14.7,
      "return_variation_rate": 0.0,
      "recognition_strength": 0.7674
    },
    "confidence_notes": {
      "phrase_destinations": 1.2,
      "tension_arcs": 0.4,
      "cadences": 0.25,
      "motifs": 0.1
    }
  }
};

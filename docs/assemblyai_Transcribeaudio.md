Transcribe audio
POST
https://api.assemblyai.com/v2/transcript
POST
/v2/transcript

curl -X POST https://api.assemblyai.com/v2/transcript \
     -H "Authorization: <apiKey>" \
     -H "Content-Type: application/json" \
     -d '{
  "audio_url": "https://assembly.ai/wildfires.mp3",
  "audio_end_at": 280,
  "audio_start_from": 10,
  "auto_chapters": true,
  "auto_highlights": true,
  "boost_param": "high",
  "content_safety": true,
  "custom_spelling": [],
  "disfluencies": false,
  "entity_detection": true,
  "filter_profanity": true,
  "format_text": true,
  "iab_categories": true,
  "language_code": "en_us",
  "language_confidence_threshold": 0.7,
  "language_detection": true,
  "multichannel": true,
  "punctuate": true,
  "redact_pii": true,
  "redact_pii_audio": true,
  "redact_pii_audio_quality": "mp3",
  "redact_pii_policies": [
    "us_social_security_number",
    "credit_card_number"
  ],
  "redact_pii_sub": "hash",
  "sentiment_analysis": true,
  "speaker_labels": true,
  "speakers_expected": 2,
  "speech_threshold": 0.5,
  "summarization": true,
  "summary_model": "informative",
  "summary_type": "bullets",
  "topics": [],
  "webhook_auth_header_name": "webhook-secret",
  "webhook_auth_header_value": "webhook-secret-value",
  "webhook_url": "https://your-webhook-url/path",
  "custom_topics": true,
  "dual_channel": false,
  "word_boost": [
    "aws",
    "azure",
    "google cloud"
  ]
}'
Try it
200
Successful

{
  "id": "9ea68fd3-f953-42c1-9742-976c447fb463",
  "audio_url": "https://assembly.ai/wildfires.mp3",
  "status": "completed",
  "webhook_auth": true,
  "auto_highlights": true,
  "redact_pii": true,
  "summarization": true,
  "language_model": "assemblyai_default",
  "acoustic_model": "assemblyai_default",
  "language_code": "en_us",
  "language_detection": true,
  "language_confidence_threshold": 0.7,
  "language_confidence": 0.9959,
  "speech_model": null,
  "text": "Smoke from hundreds of wildfires in Canada is triggering air quality alerts throughout the US. Skylines from Maine to Maryland to Minnesota are gray and smoggy. And in some places, the air quality warnings include the warning to stay inside. We wanted to better understand what's happening here and why, so we called Peter de Carlo, an associate professor in the Department of Environmental Health and Engineering at Johns Hopkins University Varsity. Good morning, professor. Good morning. What is it about the conditions right now that have caused this round of wildfires to affect so many people so far away? Well, there's a couple of things. The season has been pretty dry already. And then the fact that we're getting hit in the US. Is because there's a couple of weather systems that are essentially channeling the smoke from those Canadian wildfires through Pennsylvania into the Mid Atlantic and the Northeast and kind of just dropping the smoke there. So what is it in this haze that makes it harmful? And I'm assuming it is harmful. It is. The levels outside right now in Baltimore are considered unhealthy. And most of that is due to what's called particulate matter, which are tiny particles, microscopic smaller than the width of your hair that can get into your lungs and impact your respiratory system, your cardiovascular system, and even your neurological your brain. What makes this particularly harmful? Is it the volume of particulant? Is it something in particular? What is it exactly? Can you just drill down on that a little bit more? Yeah. So the concentration of particulate matter I was looking at some of the monitors that we have was reaching levels of what are, in science, big 150 micrograms per meter cubed, which is more than ten times what the annual average should be and about four times higher than what you're supposed to have on a 24 hours average. And so the concentrations of these particles in the air are just much, much higher than we typically see. And exposure to those high levels can lead to a host of health problems. And who is most vulnerable? I noticed that in New York City, for example, they're canceling outdoor activities. And so here it is in the early days of summer, and they have to keep all the kids inside. So who tends to be vulnerable in a situation like this? It's the youngest. So children, obviously, whose bodies are still developing. The elderly, who are their bodies are more in decline and they're more susceptible to the health impacts of breathing, the poor air quality. And then people who have preexisting health conditions, people with respiratory conditions or heart conditions can be triggered by high levels of air pollution. Could this get worse? That's a good question. In some areas, it's much worse than others. And it just depends on kind of where the smoke is concentrated. I think New York has some of the higher concentrations right now, but that's going to change as that air moves away from the New York area. But over the course of the next few days, we will see different areas being hit at different times with the highest concentrations. I was going to ask you about more fires start burning. I don't expect the concentrations to go up too much higher. I was going to ask you how and you started to answer this, but how much longer could this last? Or forgive me if I'm asking you to speculate, but what do you think? Well, I think the fires are going to burn for a little bit longer, but the key for us in the US. Is the weather system changing. And so right now, it's kind of the weather systems that are pulling that air into our mid Atlantic and Northeast region. As those weather systems change and shift, we'll see that smoke going elsewhere and not impact us in this region as much. And so I think that's going to be the defining factor. And I think the next couple of days we're going to see a shift in that weather pattern and start to push the smoke away from where we are. And finally, with the impacts of climate change, we are seeing more wildfires. Will we be seeing more of these kinds of wide ranging air quality consequences or circumstances? I mean, that is one of the predictions for climate change. Looking into the future, the fire season is starting earlier and lasting longer, and we're seeing more frequent fires. So, yeah, this is probably something that we'll be seeing more frequently. This tends to be much more of an issue in the Western US. So the eastern US. Getting hit right now is a little bit new. But yeah, I think with climate change moving forward, this is something that is going to happen more frequently. That's Peter De Carlo, associate professor in the Department of Environmental Health and Engineering at Johns Hopkins University. Sergeant Carlo, thanks so much for joining us and sharing this expertise with us. Thank you for having me.",
  "words": [
    {
      "confidence": 0.97465,
      "start": 250,
      "end": 650,
      "text": "Smoke",
      "speaker": null
    },
    {
      "confidence": 0.99999,
      "start": 730,
      "end": 1022,
      "text": "from",
      "speaker": null
    },
    {
      "confidence": 0.99844,
      "start": 1076,
      "end": 1418,
      "text": "hundreds",
      "speaker": null
    },
    {
      "confidence": 0.84,
      "start": 1434,
      "end": 1614,
      "text": "of",
      "speaker": null
    },
    {
      "confidence": 0.89572,
      "start": 1652,
      "end": 2346,
      "text": "wildfires",
      "speaker": null
    },
    {
      "confidence": 0.99994,
      "start": 2378,
      "end": 2526,
      "text": "in",
      "speaker": null
    },
    {
      "confidence": 0.93953,
      "start": 2548,
      "end": 3130,
      "text": "Canada",
      "speaker": null
    },
    {
      "confidence": 0.999,
      "start": 3210,
      "end": 3454,
      "text": "is",
      "speaker": null
    },
    {
      "confidence": 0.74794,
      "start": 3492,
      "end": 3946,
      "text": "triggering",
      "speaker": null
    },
    {
      "confidence": 1,
      "start": 3978,
      "end": 4174,
      "text": "air",
      "speaker": null
    },
    {
      "confidence": 0.88077,
      "start": 4212,
      "end": 4558,
      "text": "quality",
      "speaker": null
    },
    {
      "confidence": 0.94814,
      "start": 4644,
      "end": 5114,
      "text": "alerts",
      "speaker": null
    },
    {
      "confidence": 0.99726,
      "start": 5162,
      "end": 5466,
      "text": "throughout",
      "speaker": null
    },
    {
      "confidence": 0.79,
      "start": 5498,
      "end": 5694,
      "text": "the",
      "speaker": null
    },
    {
      "confidence": 0.89,
      "start": 5732,
      "end": 6382,
      "text": "US.",
      "speaker": null
    }
  ],
  "utterances": [
    {
      "confidence": 0.9359033333333334,
      "start": 250,
      "end": 26950,
      "text": "Smoke from hundreds of wildfires in Canada is triggering air quality alerts throughout the US. Skylines from Maine to Maryland to Minnesota are gray and smoggy. And in some places, the air quality warnings include the warning to stay inside. We wanted to better understand what's happening here and why, so we called Peter de Carlo, an associate professor in the Department of Environmental Health and Engineering at Johns Hopkins University Varsity. Good morning, professor.",
      "words": [
        {
          "confidence": 0.97503,
          "start": 250,
          "end": 650,
          "text": "Smoke",
          "speaker": "A"
        },
        {
          "confidence": 0.99999,
          "start": 730,
          "end": 1022,
          "text": "from",
          "speaker": "A"
        },
        {
          "confidence": 0.99843,
          "start": 1076,
          "end": 1418,
          "text": "hundreds",
          "speaker": "A"
        },
        {
          "confidence": 0.85,
          "start": 1434,
          "end": 1614,
          "text": "of",
          "speaker": "A"
        },
        {
          "confidence": 0.89657,
          "start": 1652,
          "end": 2346,
          "text": "wildfires",
          "speaker": "A"
        },
        {
          "confidence": 0.99994,
          "start": 2378,
          "end": 2526,
          "text": "in",
          "speaker": "A"
        },
        {
          "confidence": 0.93864,
          "start": 2548,
          "end": 3130,
          "text": "Canada",
          "speaker": "A"
        },
        {
          "confidence": 0.999,
          "start": 3210,
          "end": 3454,
          "text": "is",
          "speaker": "A"
        },
        {
          "confidence": 0.75366,
          "start": 3492,
          "end": 3946,
          "text": "triggering",
          "speaker": "A"
        },
        {
          "confidence": 1,
          "start": 3978,
          "end": 4174,
          "text": "air",
          "speaker": "A"
        },
        {
          "confidence": 0.87745,
          "start": 4212,
          "end": 4558,
          "text": "quality",
          "speaker": "A"
        },
        {
          "confidence": 0.94739,
          "start": 4644,
          "end": 5114,
          "text": "alerts",
          "speaker": "A"
        },
        {
          "confidence": 0.99726,
          "start": 5162,
          "end": 5466,
          "text": "throughout",
          "speaker": "A"
        },
        {
          "confidence": 0.79,
          "start": 5498,
          "end": 5694,
          "text": "the",
          "speaker": "A"
        },
        {
          "confidence": 0.88,
          "start": 5732,
          "end": 6382,
          "text": "US.",
          "speaker": "A"
        }
      ],
      "speaker": "A"
    }
  ],
  "confidence": 0.9404651451800253,
  "audio_duration": 281,
  "punctuate": true,
  "format_text": true,
  "disfluencies": false,
  "multichannel": false,
  "webhook_url": "https://your-webhook-url.tld/path",
  "webhook_status_code": 200,
  "webhook_auth_header_name": "webhook-secret",
  "auto_highlights_result": {
    "status": "success",
    "results": [
      {
        "count": 1,
        "rank": 0.08,
        "text": "air quality alerts",
        "timestamps": [
          {
            "start": 3978,
            "end": 5114
          }
        ]
      },
      {
        "count": 1,
        "rank": 0.08,
        "text": "wide ranging air quality consequences",
        "timestamps": [
          {
            "start": 235388,
            "end": 238694
          }
        ]
      },
      {
        "count": 1,
        "rank": 0.07,
        "text": "more wildfires",
        "timestamps": [
          {
            "start": 230972,
            "end": 232354
          }
        ]
      },
      {
        "count": 1,
        "rank": 0.07,
        "text": "air pollution",
        "timestamps": [
          {
            "start": 156004,
            "end": 156910
          }
        ]
      },
      {
        "count": 3,
        "rank": 0.07,
        "text": "weather systems",
        "timestamps": [
          {
            "start": 47344,
            "end": 47958
          },
          {
            "start": 205268,
            "end": 205818
          },
          {
            "start": 211588,
            "end": 213434
          }
        ]
      },
      {
        "count": 2,
        "rank": 0.06,
        "text": "high levels",
        "timestamps": [
          {
            "start": 121128,
            "end": 121646
          },
          {
            "start": 155412,
            "end": 155866
          }
        ]
      },
      {
        "count": 1,
        "rank": 0.06,
        "text": "health conditions",
        "timestamps": [
          {
            "start": 152138,
            "end": 152666
          }
        ]
      },
      {
        "count": 2,
        "rank": 0.06,
        "text": "Peter de Carlo",
        "timestamps": [
          {
            "start": 18948,
            "end": 19930
          },
          {
            "start": 268298,
            "end": 269194
          }
        ]
      },
      {
        "count": 1,
        "rank": 0.06,
        "text": "New York City",
        "timestamps": [
          {
            "start": 125768,
            "end": 126274
          }
        ]
      },
      {
        "count": 1,
        "rank": 0.05,
        "text": "respiratory conditions",
        "timestamps": [
          {
            "start": 152964,
            "end": 153786
          }
        ]
      },
      {
        "count": 3,
        "rank": 0.05,
        "text": "New York",
        "timestamps": [
          {
            "start": 125768,
            "end": 126034
          },
          {
            "start": 171448,
            "end": 171938
          },
          {
            "start": 176008,
            "end": 176322
          }
        ]
      },
      {
        "count": 3,
        "rank": 0.05,
        "text": "climate change",
        "timestamps": [
          {
            "start": 229548,
            "end": 230230
          },
          {
            "start": 244576,
            "end": 245162
          },
          {
            "start": 263348,
            "end": 263950
          }
        ]
      },
      {
        "count": 1,
        "rank": 0.05,
        "text": "Johns Hopkins University Varsity",
        "timestamps": [
          {
            "start": 23972,
            "end": 25490
          }
        ]
      },
      {
        "count": 1,
        "rank": 0.05,
        "text": "heart conditions",
        "timestamps": [
          {
            "start": 153988,
            "end": 154506
          }
        ]
      },
      {
        "count": 1,
        "rank": 0.05,
        "text": "air quality warnings",
        "timestamps": [
          {
            "start": 12308,
            "end": 13434
          }
        ]
      }
    ]
  },
  "audio_start_from": 10,
  "audio_end_at": 280,
  "boost_param": "high",
  "filter_profanity": true,
  "redact_pii_audio": true,
  "redact_pii_audio_quality": "mp3",
  "redact_pii_policies": [
    "us_social_security_number",
    "credit_card_number"
  ],
  "redact_pii_sub": "hash",
  "speaker_labels": true,
  "speakers_expected": 2,
  "content_safety": true,
  "content_safety_labels": {
    "status": "success",
    "results": [
      {
        "text": "Smoke from hundreds of wildfires in Canada is triggering air quality alerts throughout the US. Skylines from Maine to Maryland to Minnesota are gray and smoggy. And in some places, the air quality warnings include the warning to stay inside. We wanted to better understand what's happening here and why, so we called Peter de Carlo, an associate professor in the Department of Environmental Health and Engineering at Johns Hopkins University Varsity. Good morning, professor. Good morning.",
        "labels": [
          {
            "label": "disasters",
            "confidence": 0.8142836093902588,
            "severity": 0.4093044400215149
          }
        ],
        "sentences_idx_start": 0,
        "sentences_idx_end": 5,
        "timestamp": {
          "start": 250,
          "end": 28840
        }
      }
    ],
    "summary": {
      "disasters": 0.9940800441842205,
      "health_issues": 0.9216489289040967
    },
    "severity_score_summary": {
      "disasters": {
        "low": 0.5733263024656846,
        "medium": 0.42667369753431533,
        "high": 0
      },
      "health_issues": {
        "low": 0.22863814977924785,
        "medium": 0.45014154926938227,
        "high": 0.32122030095136983
      }
    }
  },
  "iab_categories": true,
  "iab_categories_result": {
    "status": "success",
    "results": [
      {
        "text": "Smoke from hundreds of wildfires in Canada is triggering air quality alerts throughout the US. Skylines from Maine to Maryland to Minnesota are gray and smoggy. And in some places, the air quality warnings include the warning to stay inside. We wanted to better understand what's happening here and why, so we called Peter de Carlo, an associate professor in the Department of Environmental Health and Engineering at Johns Hopkins University Varsity. Good morning, professor. Good morning.",
        "labels": [
          {
            "relevance": 0.988274097442627,
            "label": "Home&Garden>IndoorEnvironmentalQuality"
          },
          {
            "relevance": 0.5821335911750793,
            "label": "NewsAndPolitics>Weather"
          },
          {
            "relevance": 0.0042327106930315495,
            "label": "MedicalHealth>DiseasesAndConditions>LungAndRespiratoryHealth"
          },
          {
            "relevance": 0.0033971222583204508,
            "label": "NewsAndPolitics>Disasters"
          },
          {
            "relevance": 0.002469958271831274,
            "label": "BusinessAndFinance>Business>GreenSolutions"
          },
          {
            "relevance": 0.0014376690378412604,
            "label": "MedicalHealth>DiseasesAndConditions>Cancer"
          },
          {
            "relevance": 0.0014294233405962586,
            "label": "Science>Environment"
          },
          {
            "relevance": 0.001234519761055708,
            "label": "Travel>TravelLocations>PolarTravel"
          },
          {
            "relevance": 0.0010231725173071027,
            "label": "MedicalHealth>DiseasesAndConditions>ColdAndFlu"
          },
          {
            "relevance": 0.0007445293595083058,
            "label": "BusinessAndFinance>Industries>PowerAndEnergyIndustry"
          }
        ],
        "timestamp": {
          "start": 250,
          "end": 28840
        }
      }
    ],
    "summary": {
      "NewsAndPolitics>Weather": 1,
      "Home&Garden>IndoorEnvironmentalQuality": 0.9043831825256348,
      "Science>Environment": 0.16117265820503235,
      "BusinessAndFinance>Industries>EnvironmentalServicesIndustry": 0.14393523335456848,
      "MedicalHealth>DiseasesAndConditions>LungAndRespiratoryHealth": 0.11401086300611496,
      "BusinessAndFinance>Business>GreenSolutions": 0.06348437070846558,
      "NewsAndPolitics>Disasters": 0.05041387677192688,
      "Travel>TravelLocations>PolarTravel": 0.01308488193899393,
      "HealthyLiving": 0.008222488686442375,
      "MedicalHealth>DiseasesAndConditions>ColdAndFlu": 0.0022315620444715023,
      "MedicalHealth>DiseasesAndConditions>HeartAndCardiovascularDiseases": 0.00213034451007843,
      "HealthyLiving>Wellness>SmokingCessation": 0.001540527562610805,
      "MedicalHealth>DiseasesAndConditions>Injuries": 0.0013950627762824297,
      "BusinessAndFinance>Industries>PowerAndEnergyIndustry": 0.0012570273829624057,
      "MedicalHealth>DiseasesAndConditions>Cancer": 0.001097781932912767,
      "MedicalHealth>DiseasesAndConditions>Allergies": 0.0010148967849090695,
      "MedicalHealth>DiseasesAndConditions>MentalHealth": 0.000717321818228811,
      "Style&Fashion>PersonalCare>DeodorantAndAntiperspirant": 0.0006022014422342181,
      "Technology&Computing>Computing>ComputerNetworking": 0.0005461975233629346,
      "MedicalHealth>DiseasesAndConditions>Injuries>FirstAid": 0.0004885646631009877
    }
  },
  "auto_chapters": true,
  "chapters": [
    {
      "gist": "Smoggy air quality alerts across US",
      "headline": "Smoke from hundreds of wildfires in Canada is triggering air quality alerts across US",
      "summary": "Smoke from hundreds of wildfires in Canada is triggering air quality alerts throughout the US. Skylines from Maine to Maryland to Minnesota are gray and smoggy. In some places, the air quality warnings include the warning to stay inside.",
      "start": 250,
      "end": 28840
    },
    {
      "gist": "What is it about the conditions right now that have caused this round",
      "headline": "High particulate matter in wildfire smoke can lead to serious health problems",
      "summary": "Air pollution levels in Baltimore are considered unhealthy. Exposure to high levels can lead to a host of health problems. With climate change, we are seeing more wildfires. Will we be seeing more of these kinds of wide ranging air quality consequences?",
      "start": 29610,
      "end": 280340
    }
  ],
  "summary_type": "bullets",
  "summary_model": "informative",
  "summary": "- Smoke from hundreds of wildfires in Canada is triggering air quality alerts throughout the US. Skylines from Maine to Maryland to Minnesota are gray and smoggy. In some places, the air quality warnings include the warning to stay inside.\\n- Air pollution levels in Baltimore are considered unhealthy. Exposure to high levels can lead to a host of health problems. With climate change, we are seeing more wildfires. Will we be seeing more of these kinds of wide ranging air quality consequences?",
  "topics": [],
  "sentiment_analysis": true,
  "entity_detection": true,
  "entities": [
    {
      "entity_type": "location",
      "text": "Canada",
      "start": 2548,
      "end": 3130
    },
    {
      "entity_type": "location",
      "text": "the US",
      "start": 5498,
      "end": 6382
    },
    {
      "entity_type": "location",
      "text": "Maine",
      "start": 7492,
      "end": 7914
    },
    {
      "entity_type": "location",
      "text": "Maryland",
      "start": 8212,
      "end": 8634
    },
    {
      "entity_type": "location",
      "text": "Minnesota",
      "start": 8932,
      "end": 9578
    },
    {
      "entity_type": "person_name",
      "text": "Peter de Carlo",
      "start": 18948,
      "end": 19930
    },
    {
      "entity_type": "occupation",
      "text": "associate professor",
      "start": 20292,
      "end": 21194
    },
    {
      "entity_type": "organization",
      "text": "Department of Environmental Health and Engineering",
      "start": 21508,
      "end": 23706
    },
    {
      "entity_type": "organization",
      "text": "Johns Hopkins University Varsity",
      "start": 23972,
      "end": 25490
    },
    {
      "entity_type": "occupation",
      "text": "professor",
      "start": 26076,
      "end": 26950
    },
    {
      "entity_type": "location",
      "text": "the US",
      "start": 45184,
      "end": 45898
    },
    {
      "entity_type": "nationality",
      "text": "Canadian",
      "start": 49728,
      "end": 50086
    }
  ],
  "speech_threshold": 0.5,
  "dual_channel": false,
  "word_boost": [
    "aws",
    "azure",
    "google cloud"
  ],
  "custom_topics": true
}
To use our EU server for transcription, replace api.assemblyai.com with api.eu.assemblyai.com.
Create a transcript from a media file that is accessible via a URL.

Headers
Authorization
string
Required
Request
Params to create a transcript
audio_url
string
Required
format: "url"
The URL of the audio or video file to transcribe.
audio_end_at
integer
Optional
The point in time, in milliseconds, to stop transcribing in your media file
audio_start_from
integer
Optional
The point in time, in milliseconds, to begin transcribing in your media file
auto_chapters
boolean
Optional
Defaults to false
Enable Auto Chapters, can be true or false

auto_highlights
boolean
Optional
Defaults to false
Enable Key Phrases, either true or false
boost_param
enum
Optional
How much to boost specified words
Allowed values:
low
default
high
content_safety
boolean
Optional
Defaults to false
Enable Content Moderation, can be true or false

content_safety_confidence
integer
Optional
>=25
<=100
Defaults to 50
The confidence threshold for the Content Moderation model. Values must be between 25 and 100.
custom_spelling
list of objects
Optional
Customize how words are spelled and formatted using to and from values

Show 2 properties
disfluencies
boolean
Optional
Defaults to false
Transcribe Filler Words, like “umm”, in your media file; can be true or false

entity_detection
boolean
Optional
Defaults to false
Enable Entity Detection, can be true or false

filter_profanity
boolean
Optional
Defaults to false
Filter profanity from the transcribed text, can be true or false
format_text
boolean
Optional
Defaults to true
Enable Text Formatting, can be true or false
iab_categories
boolean
Optional
Defaults to false
Enable Topic Detection, can be true or false

keyterms_prompt
list of strings
Optional
keyterms_prompt is only supported when the speech_model is specified as slam-1
Improve accuracy with up to 1000 domain-specific words or phrases (maximum 6 words per phrase).

language_code
enum
Optional
The language of your audio file. Possible values are found in Supported Languages. The default value is ‘en_us’.


Show 102 enum values
language_confidence_threshold
double
Optional
The confidence threshold for the automatically detected language. An error will be returned if the language confidence is below this threshold. Defaults to 0.
language_detection
boolean
Optional
Defaults to false
Enable Automatic language detection, either true or false.

multichannel
boolean
Optional
Defaults to false
Enable Multichannel transcription, can be true or false.

punctuate
boolean
Optional
Defaults to true
Enable Automatic Punctuation, can be true or false
redact_pii
boolean
Optional
Defaults to false
Redact PII from the transcribed text using the Redact PII model, can be true or false
redact_pii_audio
boolean
Optional
Defaults to false
Generate a copy of the original media file with spoken PII “beeped” out, can be true or false. See PII redaction for more details.

redact_pii_audio_options
object
Optional
Specify options for PII redacted audio files.

Show 1 properties
redact_pii_audio_quality
enum
Optional
Controls the filetype of the audio created by redact_pii_audio. Currently supports mp3 (default) and wav. See PII redaction for more details.

Allowed values:
mp3
wav
redact_pii_policies
list of enums
Optional
The list of PII Redaction policies to enable. See PII redaction for more details.


Show 44 enum values
redact_pii_sub
enum
Optional
The replacement logic for detected PII, can be entity_type or hash. See PII redaction for more details.

Allowed values:
entity_name
hash
sentiment_analysis
boolean
Optional
Defaults to false
Enable Sentiment Analysis, can be true or false

speaker_labels
boolean
Optional
Defaults to false
Enable Speaker diarization, can be true or false

speaker_options
object
Optional
Specify options for speaker diarization.

Show 2 properties
speakers_expected
integer
Optional
Tells the speaker label model how many speakers it should attempt to identify, up to 10. See Speaker diarization for more details.

speech_model
enum
Optional
The speech model to use for the transcription. When null, the universal model is used.

Allowed values:
best
nano
slam-1
universal
speech_threshold
double
Optional
Reject audio files that contain less than this fraction of speech. Valid values are in the range [0, 1] inclusive.

summarization
boolean
Optional
Defaults to false
Enable Summarization, can be true or false

summary_model
enum
Optional
The model to summarize the transcript
Allowed values:
informative
conversational
catchy
summary_type
enum
Optional
The type of summary
Allowed values:
bullets
bullets_verbose
gist
headline
paragraph
topics
list of strings
Optional
The list of custom topics
webhook_auth_header_name
string
Optional
The header name to be sent with the transcript completed or failed webhook requests
webhook_auth_header_value
string
Optional
The header value to send back with the transcript completed or failed webhook requests for added security
webhook_url
string
Optional
format: "url"
The URL to which we send webhook requests. We sends two different types of webhook requests. One request when a transcript is completed or failed, and one request when the redacted audio is ready if redact_pii_audio is enabled.

custom_topics
boolean
Optional
Defaults to false
Deprecated
Enable custom topics, either true or false
dual_channel
boolean
Optional
Defaults to false
Deprecated
Enable Dual Channel transcription, can be true or false.

prompt
string
Optional
Deprecated
This parameter does not currently have any functionality attached to it.
word_boost
list of strings
Optional
Deprecated
The list of custom vocabulary to boost transcription probability for
Response
Transcript created and queued for processing
id
string
format: "uuid"
The unique identifier of your transcript
audio_url
string
format: "url"
The URL of the media that was transcribed
status
enum
The status of your transcript. Possible values are queued, processing, completed, or error.
Allowed values:
queued
processing
completed
error
webhook_auth
boolean
Whether webhook authentication details were provided
auto_highlights
boolean
Whether Key Phrases is enabled, either true or false
redact_pii
boolean
Whether PII Redaction is enabled, either true or false

summarization
boolean
Whether Summarization is enabled, either true or false

language_model
string
Deprecated
The language model that was used for the transcript
acoustic_model
string
Deprecated
The acoustic model that was used for the transcript
language_code
enum or null
The language of your audio file. Possible values are found in Supported Languages. The default value is ‘en_us’.


Show 102 enum values
language_detection
boolean or null
Whether Automatic language detection is enabled, either true or false

language_confidence_threshold
double or null
The confidence threshold for the automatically detected language. An error will be returned if the language confidence is below this threshold.
language_confidence
double or null
>=0
<=1
The confidence score for the detected language, between 0.0 (low confidence) and 1.0 (high confidence)

speech_model
enum or null
The speech model used for the transcription. When null, the universal model is used.

Allowed values:
best
nano
slam-1
universal
text
string or null
The textual transcript of your media file
words
list of objects or null
An array of temporally-sequential word objects, one for each word in the transcript. See Speech recognition for more information.


Show 6 properties
utterances
list of objects or null
When multichannel or speaker_labels is enabled, a list of turn-by-turn utterance objects. See Speaker diarization and Multichannel transcription for more information.


Show 7 properties
confidence
double or null
>=0
<=1
The confidence score for the transcript, between 0.0 (low confidence) and 1.0 (high confidence)

audio_duration
integer or null
The duration of this transcript object's media file, in seconds
punctuate
boolean or null
Whether Automatic Punctuation is enabled, either true or false
format_text
boolean or null
Whether Text Formatting is enabled, either true or false
disfluencies
boolean or null
Transcribe Filler Words, like “umm”, in your media file; can be true or false

multichannel
boolean or null
Whether Multichannel transcription was enabled in the transcription request, either true or false

audio_channels
integer or null
The number of audio channels in the audio file. This is only present when multichannel is enabled.
webhook_url
string or null
format: "url"
The URL to which we send webhook requests. We sends two different types of webhook requests. One request when a transcript is completed or failed, and one request when the redacted audio is ready if redact_pii_audio is enabled.

webhook_status_code
integer or null
The status code we received from your server when delivering the transcript completed or failed webhook request, if a webhook URL was provided
webhook_auth_header_name
string or null
The header name to be sent with the transcript completed or failed webhook requests
auto_highlights_result
object or null
An array of results for the Key Phrases model, if it is enabled. See Key Phrases for more information.


Show 2 properties
audio_start_from
integer or null
The point in time, in milliseconds, in the file at which the transcription was started
audio_end_at
integer or null
The point in time, in milliseconds, in the file at which the transcription was terminated
boost_param
string or null
The word boost parameter value
filter_profanity
boolean or null
Whether Profanity Filtering is enabled, either true or false

redact_pii_audio
boolean or null
Whether a redacted version of the audio file was generated, either true or false. See PII redaction for more information.

redact_pii_audio_quality
enum or null
The audio quality of the PII-redacted audio file, if redact_pii_audio is enabled. See PII redaction for more information.

Allowed values:
mp3
wav
redact_pii_policies
list of enums or null
The list of PII Redaction policies that were enabled, if PII Redaction is enabled. See PII redaction for more information.


Show 44 enum values
redact_pii_sub
enum or null
The replacement logic for detected PII, can be entity_type or hash. See PII redaction for more details.

Allowed values:
entity_name
hash
speaker_labels
boolean or null
Whether Speaker diarization is enabled, can be true or false

speakers_expected
integer or null
Tell the speaker label model how many speakers it should attempt to identify, up to 10. See Speaker diarization for more details.

content_safety
boolean or null
Whether Content Moderation is enabled, can be true or false

content_safety_labels
object or null
An array of results for the Content Moderation model, if it is enabled. See Content moderation for more information.


Show 4 properties
iab_categories
boolean or null
Whether Topic Detection is enabled, can be true or false

iab_categories_result
object or null
The result of the Topic Detection model, if it is enabled. See Topic Detection for more information.


Show 3 properties
custom_spelling
list of objects or null
Customize how words are spelled and formatted using to and from values

Show 2 properties
keyterms_prompt
list of strings or null
Improve accuracy with up to 1000 domain-specific words or phrases (maximum 6 words per phrase).

auto_chapters
boolean or null
Whether Auto Chapters is enabled, can be true or false

chapters
list of objects or null
An array of temporally sequential chapters for the audio file

Show 5 properties
summary_type
string or null
The type of summary generated, if Summarization is enabled

summary_model
string or null
The Summarization model used to generate the summary, if Summarization is enabled

summary
string or null
The generated summary of the media file, if Summarization is enabled

topics
list of strings or null
The list of custom topics provided if custom topics is enabled
sentiment_analysis
boolean or null
Whether Sentiment Analysis is enabled, can be true or false

sentiment_analysis_results
list of objects or null
An array of results for the Sentiment Analysis model, if it is enabled. See Sentiment Analysis for more information.


Show 7 properties
entity_detection
boolean or null
Whether Entity Detection is enabled, can be true or false

entities
list of objects or null
An array of results for the Entity Detection model, if it is enabled. See Entity detection for more information.


Show 4 properties
speech_threshold
double or null
Defaults to null. Reject audio files that contain less than this fraction of speech. Valid values are in the range [0, 1] inclusive.

throttled
boolean or null
True while a request is throttled and false when a request is no longer throttled
error
string or null
Error message of why the transcript failed
dual_channel
boolean or null
Deprecated
Whether Dual channel transcription was enabled in the transcription request, either true or false

speed_boost
boolean or null
Deprecated
Whether speed boost is enabled
word_boost
list of strings or null
Deprecated
The list of custom vocabulary to boost transcription probability for
prompt
string or null
Deprecated
This parameter does not currently have any functionality attached to it.
custom_topics
boolean or null
Deprecated
Whether custom topics is enabled, either true or false
Errors

400
Bad Request Error

401
Unauthorized Error

404
Not Found Error

429
Too Many Requests Error

500
Internal Server Error

503
Service Unavailable Error

504
Gateway Timeout Error
Was this page helpful?
Yes

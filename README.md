# 🛫💭 ATC Voice Recognition

Voice to speech conversion and evaluation for ATC

## Important Links

- <https://github.com/pandermatt/pa-19-atc>
- <https://github.com/pandermatt/pa-19-atc-doc>
- RML: <https://github.zhaw.ch/anderpas/pa-19-atc-rml>
- Data: <https://github.zhaw.ch/anderpas/pa-19-atc-data>
- Custom speech portal: <https://speech.microsoft.com/customspeech>
- LUIS: <https://luis.ai/>


## Developing
### Setup

```bash
git clone git@github.com:pandermatt/pa-19-atc.git
cd pa-19-atc
pip install -r requirements.txt
```

#### Configuration

```bash
cp application.example.yml application.yml
```

Fill in all your keys

### Packages
```
.
├── audio - Modify audio samples
├── bin - Scripts folder
├── context_check - Evaluate the Context
├── io_module - Load/Store files
├── keyword - Extract and Evaluate Keywords
├── language_understanding - Convertion with LUIS
├── regex_markup_language - Convertion with RML (xml-Files)
├── speech - Extract and Evaluate Speech-To-Text
├── util - Helper functions
└── word_error_rate - github.com/zszyellow/WER-in-python/blob/master/wer.py
```

# Contributors
![](https://avatars2.githubusercontent.com/u/20790833?s=20) Pascal Andermatt

![](https://avatars0.githubusercontent.com/u/43876424?s=20) Jennifer Schürch

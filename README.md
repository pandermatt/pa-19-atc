# 🛫💭 ATC Voice Recognition

Voice to speech conversion and evaluation for ATC

> Nowadays pilots and Air Traﬃc Control Operator (ATCO) are assisted by various electronic and technical systems, for example in the form of collision prevention or landing assistance.
> Nevertheless, due to the ever-increasing amount of air traffic, their work becomes progressively more hectic and demanding and the most important form of communication is still carried out with the help of radio technology.
> The biggest problems of this communication method are the poor transmission quality of the radio signal as well as the varying pronunciations and accents of the speakers.
> These factors can lead to misunderstandings, which could have serious consequences.
> This project is a continuation of a previous bachelor thesis, which examined various automatic speech recognition services for their performance in relation to these radio messages.
> The aim of this project is to determine to what extent the Speech-To-Text service of Microsoft, called Custom Speech, can be improved.
> Furthermore, the Microsoft service, called Language Understanding (LUIS), and the Regex Markup Language (RML) software are compared to each other regarding the extraction of the data required for further processing and to inspect the context of the existing Air Traﬃc Control (ATC) radio messages.
> With the Microsoft Custom Speech service, it turns out that conventional techniques for data augmentation did not contribute to the improvement of the models and that the performance of the model using noisy radio messages is not optimal.
> With regards to LUIS, the extraction of the important keywords already works well, but the Regex approach using RML performs better with the data at hand.
> Further, LUIS does not offer the possibility to include a context to check the ATC radio messages. Therefore, only the RML software is evaluated.
> As long as the recognized keywords for the context check do not deviate strongly from the expected value, the context can be checked and corrected by a fuzzy search.
> Based on the results, there is potential for further application of automatic speech recognition in the ATC environment.
> Nevertheless, the Speech-To-Text model needs further improvement before this system can work reliably.


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

If you want to change the directory structure or modify the environment variables, you can do so in `config.py`

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
![](https://avatars2.githubusercontent.com/u/20790833?s=20) [Pascal Andermatt](https://github.com/pandermatt)

![](https://avatars0.githubusercontent.com/u/43876424?s=20) [Jennifer Schürch](https://github.com/jschuerch)

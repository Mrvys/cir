# pip install spacy
# python -m spacy download en_core_web_sm

import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en')

# Determine semantic similarities
greeting = nlp(u"hello")

while True:
    user_input = input('Enter your input:')
    user_input_nlp = nlp(user_input)
    if user_input_nlp.similarity(greeting) > 0.7:
        print("Good evening!")
    else:
        print("Im sorry I don't understand")

# pip install spacy
# python -m spacy download en_core_web_sm

import spacy


class TextRecognizer:

    def __init__(self):
        self.__nlp = spacy.load('en')  # Load English tokenizer, tagger, parser, NER and word vectors

    def choose_most_sufficient(self, user_input, actions):
        return user_input.lower()
        # TODO Change to choose the most similar phrase

        # user_input_nlp = nlp(user_input)
        # if user_input_nlp.similarity(greeting) > 0.7:
        #     print("Good evening!")
        # else:
        #     print("Im sorry I don't understand")

    # sentiment for yes/no

# pip install spacy
# python -m spacy download en_core_web_sm

import spacy


class TextRecognizer:

    def __init__(self):
        self.__nlp = spacy.load('en')  # Load English tokenizer, tagger, parser, NER and word vectors

    def choose_most_sufficient(self, user_input, actions):
        if user_input == "red" or user_input == "white":
            user_input = user_input + ' wine'
            return user_input.lower()

        # Determine semantic similarities
        user_input = user_input.lower()
        doc1 = self.__nlp(user_input)
        top_score = {
            'score': 0,
            'input': None
        }

        for action in actions:
            doc2 = self.__nlp(action)
            similarity = doc1.similarity(doc2)
            #print(doc1.text, doc2.text, similarity)
            #if action in user_input:
                #return action
            if top_score['score'] < similarity:
                top_score['score'] = similarity
                top_score['input'] = action

        if top_score['score'] > 0.6:
            #print(top_score['input'])
            return top_score['input']
        return -1

        # TODO Change to choose the most similar phrase

        # user_input_nlp = nlp(user_input)
        # if user_input_nlp.similarity(greeting) > 0.7:
        #     print("Good evening!")
        # else:
        #     print("Im sorry I don't understand")

    # sentiment for yes/no

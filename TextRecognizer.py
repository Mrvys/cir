# pip install spacy
# python -m spacy download en_core_web_sm

import spacy


class TextRecognizer:

    def __init__(self):
        self.__nlp = spacy.load('en')  # Load English tokenizer, tagger, parser, NER and word vectors

    def choose_most_sufficient(self, user_input, actions):
        if "red" in user_input:
            index = user_input.find('red')
            user_input = user_input[:index + 3] + ' wine ' + user_input[index + 4:]
        if "white" in user_input:
            index = user_input.find('white')
            user_input = user_input[:index + 5] + ' wine ' + user_input[index + 6:]

        # Determine semantic similarities
        user_input = user_input.lower()
        doc1 = self.__nlp(user_input)
        top_score = {
            'score': 0,
            'input': None
        }
        actions_contained = []

        for action in actions:
            doc2 = self.__nlp(action)
            similarity = doc1.similarity(doc2)
            if action in user_input:
                actions_contained.append(action)
            if top_score['score'] < similarity:
                top_score['score'] = similarity
                top_score['input'] = action

        if len(actions_contained) > 1:
            return self.find_most_sufficient(actions_contained, user_input)
        elif top_score['score'] > 0.6:
            return top_score['input']
        return -1

        # TODO Change to choose the most similar phrase

    def find_most_sufficient(self, actions_contained, user_input):
        top_score = {
            'score': 0,
            'input': None
        }
        for action in actions_contained:
            if action != "yes" and action != "no":
                want_product = self.__nlp("I would like " + action)
                dont_want_product = self.__nlp("I would not like " + action)

                if "no" in actions_contained:
                    user_input = user_input.replace("no", "")
                input_nlp = self.__nlp(user_input)
                similarity = input_nlp.similarity(want_product)
                similarity_dont = input_nlp.similarity(dont_want_product)

                if similarity_dont > similarity and similarity_dont > top_score['score']:
                    top_score['score'] = similarity_dont
                    top_score['input'] = 'no'

                if similarity > top_score['score']:
                    top_score['score'] = similarity
                    top_score['input'] = action

        if top_score['score'] > 0.5:
            return top_score['input']
        return -1

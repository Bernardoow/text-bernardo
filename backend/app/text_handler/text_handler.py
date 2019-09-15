from collections import OrderedDict
import string
import re

import attr

from app.text_handler.text_handler_utils import stop_words_portuguese
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

check_if_word_start_with_number = re.compile(r"^\d.*")


@attr.s(frozen=True)
class TextHandler:
    """
        This class will handler the text.

        the sw is abbreviation of single word.

        the ng is abbreviation of number of gram.

        every word will be converted to lower case.
    """

    texts = attr.ib()

    @texts.validator
    def texts_check(self, attribute, value):

        if not isinstance(value, list):
            raise ValueError("the value must be list.")

        if not all([isinstance(v, str) for v in value]):
            raise ValueError("Every item inside the list must me string.")

    def _remove_stop_words(self, words):
        return [word for word in words if word not in stop_words_portuguese]

    def _remove_words_start_with_number(self, words):
        return [word for word in words if check_if_word_start_with_number.match(word) is None]

    def _word_tokenize_texts(self, text):
        return word_tokenize(text, language="portuguese")

    def _transform_to_lower_each_word(self, words):
        return [word.lower() for word in words]

    def _remove_punctuation(self, words):
        return [word for word in words if word not in string.punctuation]

    def _remove_duplicated_without_lost_order(self, words):
        return OrderedDict.fromkeys(words)

    def _calcule_frequence(self, words):
        return FreqDist(words)

    def _replace_hyphen(self, string_words):
        return string_words.replace("-", " ")

    def _base(self, text):
        words = self._word_tokenize_texts(text)
        words = self._transform_to_lower_each_word(words)
        words = self._remove_stop_words(words)
        words = self._remove_punctuation(words)
        words = self._remove_words_start_with_number(words)

        return words

    def sw_vocabulary(self):
        words = self._base(self._replace_hyphen(" ".join(self.texts)))
        words = OrderedDict.fromkeys(words)
        words = list(words)

        return words

    def sw_frequency_distribution(self):
        words_every_texts = self._base(self._replace_hyphen(" ".join(self.texts)))

        words_every_texts = OrderedDict.fromkeys(words_every_texts)
        words_every_texts = list(words_every_texts)

        frequency_distribution_result = {}

        for index, text in enumerate(self.texts, start=1):
            words = self._base(self._replace_hyphen(text))
            freq_dist = self._calcule_frequence(words)
            words = self._remove_duplicated_without_lost_order(words)
            frequency_distribution_result.update(
                {f"text{index}": [freq_dist[word] for word in words_every_texts]}
            )

        return frequency_distribution_result

    def ng_vocabulary(self, num_gram=2):
        vocabulary_result = []

        for text in self.texts:
            words = self._base(text)

            vocabulary_result.extend(ngrams(words, num_gram))

        vocabulary_result = self._remove_duplicated_without_lost_order(vocabulary_result)

        vocabulary_result = list(vocabulary_result)
        return vocabulary_result

    def ng_frequency_distribution(self, num_gram=2):
        words_every_texts = []

        for index, text in enumerate(self.texts, start=1):
            words = self._base(self._replace_hyphen(text))
            words_every_texts.extend(list(ngrams(words, num_gram)))

        words_every_texts = OrderedDict.fromkeys(words_every_texts)
        words_every_texts = list(words_every_texts)

        frequency_distribution_result = {}

        for index, text in enumerate(self.texts, start=1):
            words = self._base(self._replace_hyphen(text))
            words = list(ngrams(words, num_gram))
            freq_dist = self._calcule_frequence(words)
            words = self._remove_duplicated_without_lost_order(words)
            frequency_distribution_result.update(
                {f"text{index}": [freq_dist[word] for word in words_every_texts]}
            )

        return frequency_distribution_result

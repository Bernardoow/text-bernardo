import string
import attr

from text_handler_utils import stop_words_portuguese

# from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# word_tokenize(text, language='english', preserve_line=False)


@attr.s
class TextHandler:
    """
        This class will handler the text.

        the sw is abreviation of single word.

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

    def _word_tokenize_texts(self):
        return word_tokenize(" ".join(self.texts), language="portuguese")

    def _transform_to_lower_each_word(self, words):
        return [word.lower() for word in words]

    def sw_vocabulary(self):
        words = self._word_tokenize_texts()
        words = self._remove_stop_words(words)
        words = self._transform_to_lower_each_word(words)
        words = set(words)
        words = words - set(string.punctuation)
        words = list(words)
        words.sort()

        return words
        # return TreebankWordTokenizer().tokenize("".join(self.texts))

    def sw_frequency_distribution(self):
        words = self._word_tokenize_texts()
        words = self._remove_stop_words(words)
        words = self._transform_to_lower_each_word(words)
        words = [word for word in words if word not in string.punctuation]
        words.sort()

        freq_dist = FreqDist(words)

        return [freq for freq in freq_dist.values()]


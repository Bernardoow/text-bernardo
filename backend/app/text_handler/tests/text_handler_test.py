# -*- coding: utf-8 -*-
import inspect
import pytest
from app.text_handler.text_handler import TextHandler


class TestTextHandler:
    def test_it_should_be_a_class(self):
        text_handler = TextHandler([""])
        assert isinstance(text_handler, TextHandler)

    def test_it_should_throw_exception_with_wrong_param(self):
        with pytest.raises(ValueError):
            TextHandler("bufalo bufalo bufalo")

    def test_it_should_throw_exception_with_wrong_child_param(self):
        with pytest.raises(ValueError):
            TextHandler(["teste", None, 1, 2.3, True])

    def test_it_should_receive_list_of_text_by_param(self):
        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert isinstance(text_handler.texts, list)

    def test_it_should_has_a_method_sw_vocabulary(self):
        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert inspect.ismethod(text_handler.sw_vocabulary)

    def test_it_should_has_a_method_sw_frequency_distribution(self):
        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert inspect.ismethod(text_handler.sw_frequency_distribution)

    def test_it_should_has_a_method_ng_vocabulary(self):
        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert inspect.ismethod(text_handler.ng_vocabulary)

    def test_it_should_has_a_method_ng_frequency_distribution(self):
        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert inspect.ismethod(text_handler.ng_frequency_distribution)


class TestSwVocabularyMethod:
    def test_if_return_list_with_of_empty_text(self):
        text_handler = TextHandler([""])
        assert text_handler.sw_vocabulary() == []

    def test_if_return_list_with_single_words_and_unique_items(self):
        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert text_handler.sw_vocabulary() == ["bufalo"]

    def test_if_return_list_with_single_words_in_order(self):
        text_handler = TextHandler(["bernardo gomes abreu"])
        assert text_handler.sw_vocabulary() == ["bernardo", "gomes", "abreu"]

    def test_if_return_list_with_ignored_punctuation(self):
        text_handler = TextHandler(
            [
                "bernardo gomes; abreu. yasmine! yasmine# yasmine% yasmine$ yasmine' yasmine& yasmine) yasmine( yasmine, yasmine; yasmine: yasmine< yasmine? yasmine> yasmine@ yasmine[ yasmine] yasmine` yasmine{ yasmine} "
            ]
        )
        assert text_handler.sw_vocabulary() == ["bernardo", "gomes", "abreu", "yasmine"]

    def test_if_return_list_with_ignored_case(self):
        text_handler = TextHandler(["bernardo GOMES; Abreu."])
        assert text_handler.sw_vocabulary() == ["bernardo", "gomes", "abreu"]

    def test_if_return_list_when_the_params_is_multiple_texts(self):
        text_handler = TextHandler(
            ["bernardo GOMES; Abreu.", "YASMINE", "Melo", "Costa", "Leonardo Gomes Abreu"]
        )
        assert text_handler.sw_vocabulary() == [
            "bernardo",
            "gomes",
            "abreu",
            "yasmine",
            "melo",
            "costa",
            "leonardo",
        ]

    def test_if_return_list_without_stop_words(self):
        text_handler = TextHandler(
            [
                "bernardo GOMES; de Abreu.",
                "YASMINE",
                "de",
                "Melo",
                "Costa",
                "Leonardo Gomes de Abreu",
            ]
        )
        assert text_handler.sw_vocabulary() == [
            "bernardo",
            "gomes",
            "abreu",
            "yasmine",
            "melo",
            "costa",
            "leonardo",
        ]

    def test_if_return_list_without_words_that_started_with_number(self):
        text_handler = TextHandler(
            [
                "bernardo GOMES; de Abreu.",
                "YASMINE",
                "de",
                "Melo",
                "Costa",
                "Leonardo Gomes de Abreu",
                "1Teste",
            ]
        )
        assert text_handler.sw_vocabulary() == [
            "bernardo",
            "gomes",
            "abreu",
            "yasmine",
            "melo",
            "costa",
            "leonardo",
        ]


class TestSwFrequencyDistributionMethod:
    def test_if_return_list_the_frequence_of_list_with_unique_word(self):
        text_handler = TextHandler(["bufalo"])
        assert text_handler.sw_frequency_distribution() == {"text1": [1]}

        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert text_handler.sw_frequency_distribution() == {"text1": [3]}

    def test_if_return_list_the_frequence_of_text_empty(self):
        text_handler = TextHandler([""])
        assert text_handler.sw_frequency_distribution() == {"text1": []}

    def test_if_return_list_the_frequence_of_multiples_text(self):
        text_handler = TextHandler(
            [
                "bernardo GOMES; Abreu. gomes abreu",
                "YASMINE",
                "Melo",
                "Costa",
                "gomes abreu Leonardo Gomes Abreu 1teste",
            ]
        )
        bernardo = 1
        gomes = 2
        abreu = 2
        yasmine = 1
        melo = 1
        costa = 1
        leonardo = 1

        assert text_handler.sw_frequency_distribution() == {
            "text1": [bernardo, gomes, abreu, 0, 0, 0, 0],
            "text2": [0, 0, 0, yasmine, 0, 0, 0],
            "text3": [0, 0, 0, 0, melo, 0, 0],
            "text4": [0, 0, 0, 0, 0, costa, 0],
            "text5": [0, gomes, abreu, 0, 0, 0, leonardo],
        }


class TestNgVocabularyMethod:
    def test_if_return_list_with_of_empty_text(self):
        text_handler = TextHandler([""])
        assert text_handler.sw_vocabulary() == []

    def test_if_return_list_with_single_words_and_unique_items(self):
        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert text_handler.ng_vocabulary() == [("bufalo", "bufalo")]

    def test_if_return_list_with_single_words_in_order(self):
        text_handler = TextHandler(["bernardo gomes abreu"])
        assert text_handler.ng_vocabulary() == [("bernardo", "gomes"), ("gomes", "abreu")]

    def test_if_return_list_with_ignored_punctuation(self):
        text_handler = TextHandler(["bernardo gomes; abreu."])
        assert text_handler.ng_vocabulary() == [("bernardo", "gomes"), ("gomes", "abreu")]

    def test_if_return_list_with_ignored_case(self):
        text_handler = TextHandler(["bernardo GOMES; Abreu."])
        assert text_handler.ng_vocabulary() == [("bernardo", "gomes"), ("gomes", "abreu")]

    def test_if_return_list_when_the_params_is_multiple_texts(self):
        text_handler = TextHandler(
            ["bernardo GOMES; Abreu.", "YASMINE", "Melo", "Costa", "Leonardo Gomes Abreu"]
        )
        assert text_handler.ng_vocabulary() == [
            ("bernardo", "gomes"),
            ("gomes", "abreu"),
            ("leonardo", "gomes"),
        ]

    def test_if_return_list_without_stop_words(self):
        text_handler = TextHandler(
            [
                "bernardo GOMES; de Abreu.",
                "YASMINE",
                "de",
                "Melo",
                "Costa",
                "Leonardo Gomes de Abreu",
            ]
        )
        assert text_handler.ng_vocabulary() == [
            ("bernardo", "gomes"),
            ("gomes", "abreu"),
            ("leonardo", "gomes"),
        ]

    def test_if_return_list_without_words_started_with_numbers(self):
        text_handler = TextHandler(
            [
                "bernardo GOMES; de Abreu.",
                "YASMINE",
                "de",
                "Melo",
                "Costa",
                "Leonardo Gomes de Abreu",
                "1Teste gomes de abreu",
            ]
        )
        assert text_handler.ng_vocabulary() == [
            ("bernardo", "gomes"),
            ("gomes", "abreu"),
            ("leonardo", "gomes"),
        ]


class TestNgFrequencyDistributionMethod:
    def test_if_return_list_the_frequence_of_list_with_unique_word(self):
        text_handler = TextHandler(["bufalo"])
        assert text_handler.ng_frequency_distribution() == {"text1": []}

        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert text_handler.ng_frequency_distribution() == {"text1": [2]}

    def test_if_return_list_the_frequence_of_text_empty(self):
        text_handler = TextHandler([])
        assert text_handler.ng_frequency_distribution() == {}

    def test_if_return_list_the_frequence_of_multiples_text(self):
        text_handler = TextHandler(
            [
                "bernardo GOMES; Abreu. gomes abreu",
                "YASMINE",
                "Melo",
                "Costa",
                "Leonardo Gomes Abreu 1teste",
            ]
        )
        bernardo_gomes = 1
        gomes_abreu = 2
        abreu_gomes = 1
        leonardo_gomes = 1
        text_5_gomes_abreu = 1
        assert text_handler.ng_frequency_distribution() == {
            "text1": [bernardo_gomes, gomes_abreu, abreu_gomes, 0],
            "text2": [0, 0, 0, 0],
            "text3": [0, 0, 0, 0],
            "text4": [0, 0, 0, 0],
            "text5": [0, text_5_gomes_abreu, 0, leonardo_gomes],
        }


class TestFromDocument:
    def test_if_has_17_words_and_the_vocabulary_has_11(self):
        text_handler = TextHandler(
            [
                "Falar é fácil. Mostre-me o código.",
                "É fácil escrever código. Difícil é escrever código que funcione.",
            ]
        )
        assert text_handler.sw_vocabulary() == [
            "falar",
            # "é",
            "fácil",
            "mostre",
            # "me",
            # "o",
            "código",
            "escrever",
            "difícil",
            # "que",
            "funcione",
        ]

    def test_if_result_is_equal_a_document_base(self):
        text_handler = TextHandler(
            [
                "Falar é fácil. Mostre-me o código.",
                "É fácil escrever código. Difícil é escrever código que funcione.",
            ]
        )
        assert text_handler.sw_frequency_distribution() == {
            "text1": [1, 1, 1, 1, 0, 0, 0],
            "text2": [0, 1, 0, 2, 2, 1, 1],
        }


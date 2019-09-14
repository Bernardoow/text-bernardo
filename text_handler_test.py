# -*- coding: utf-8 -*-
import inspect
import pytest
from text_handler import TextHandler


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


class TestSwVocabularyMethod:
    def test_if_return_list_with_of_empty_text(self):
        text_handler = TextHandler([""])
        assert text_handler.sw_vocabulary() == []

    def test_if_return_list_with_single_words_and_unique_items(self):
        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert text_handler.sw_vocabulary() == ["bufalo"]

    def test_if_return_list_with_single_words_in_order(self):
        text_handler = TextHandler(["bernardo gomes abreu"])
        assert text_handler.sw_vocabulary() == ["abreu", "bernardo", "gomes"]

    def test_if_return_list_with_ignored_punctuation(self):
        text_handler = TextHandler(
            [
                "bernardo gomes; abreu. yasmine! yasmine# yasmine% yasmine$ yasmine' yasmine& yasmine) yasmine( yasmine, yasmine; yasmine: yasmine< yasmine? yasmine> yasmine@ yasmine[ yasmine] yasmine` yasmine{ yasmine} "
            ]
        )
        assert text_handler.sw_vocabulary() == ["abreu", "bernardo", "gomes", "yasmine"]

    def test_if_return_list_with_ignored_case(self):
        text_handler = TextHandler(["bernardo GOMES; Abreu."])
        assert text_handler.sw_vocabulary() == ["abreu", "bernardo", "gomes"]

    def test_if_return_list_when_the_params_is_multiple_texts(self):
        text_handler = TextHandler(
            ["bernardo GOMES; Abreu.", "YASMINE", "Melo", "Costa", "Leonardo Gomes Abreu"]
        )
        assert text_handler.sw_vocabulary() == [
            "abreu",
            "bernardo",
            "costa",
            "gomes",
            "leonardo",
            "melo",
            "yasmine",
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
            "abreu",
            "bernardo",
            "costa",
            "gomes",
            "leonardo",
            "melo",
            "yasmine",
        ]


class TestSwFrequencyDistributionMethod:
    def test_if_return_list_the_frequence_of_list_with_unique_word(self):
        text_handler = TextHandler(["bufalo"])
        assert text_handler.sw_frequency_distribution() == [1]

        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert text_handler.sw_frequency_distribution() == [3]

    def test_if_return_list_the_frequence_of_text_empty(self):
        text_handler = TextHandler([""])
        assert text_handler.sw_frequency_distribution() == []

    def test_if_return_list_the_frequence_of_multiples_text(self):
        text_handler = TextHandler(
            ["bernardo GOMES; Abreu.", "YASMINE", "Melo", "Costa", "Leonardo Gomes Abreu"]
        )
        assert text_handler.sw_frequency_distribution() == [2, 1, 1, 2, 1, 1, 1]


class TestNgVocabularyMethod:
    def test_if_return_list_with_of_empty_text(self):
        text_handler = TextHandler([""])
        assert text_handler.sw_vocabulary() == []

    def test_if_return_list_with_single_words_and_unique_items(self):
        text_handler = TextHandler(["bufalo bufalo bufalo"])
        assert text_handler.ng_vocabulary() == []

    def test_if_return_list_with_single_words_in_order(self):
        text_handler = TextHandler(["bernardo gomes abreu"])
        assert text_handler.ng_vocabulary() == [("abreu", "bernardo"), ("bernardo", "gomes")]

    def test_if_return_list_with_ignored_punctuation(self):
        text_handler = TextHandler(["bernardo gomes; abreu."])
        assert text_handler.ng_vocabulary() == [("abreu", "bernardo"), ("bernardo", "gomes")]

    def test_if_return_list_with_ignored_case(self):
        text_handler = TextHandler(["bernardo GOMES; Abreu."])
        assert text_handler.ng_vocabulary() == [("abreu", "bernardo"), ("bernardo", "gomes")]

    def test_if_return_list_when_the_params_is_multiple_texts(self):
        text_handler = TextHandler(
            ["bernardo GOMES; Abreu.", "YASMINE", "Melo", "Costa", "Leonardo Gomes Abreu"]
        )
        assert text_handler.ng_vocabulary() == [
            ("abreu", "bernardo"),
            ("bernardo", "costa"),
            ("costa", "gomes"),
            ("gomes", "leonardo"),
            ("leonardo", "melo"),
            ("melo", "yasmine"),
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
            ("abreu", "bernardo"),
            ("bernardo", "costa"),
            ("costa", "gomes"),
            ("gomes", "leonardo"),
            ("leonardo", "melo"),
            ("melo", "yasmine"),
        ]

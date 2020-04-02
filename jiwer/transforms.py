#
# JiWER - Jitsi Word Error Rate
#
# Copyright @ 2018 - present 8x8, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This file implements methods to transform text input. It implements some useful
processing steps which are advised when calculating the WER,
such as filtering out common words and standardizing abbreviations.
"""

import re
import string

from typing import Union, List, Mapping


__all__ = [
    "AbstractTransform",
    "Compose",
    "ExpandCommonEnglishContractions",
    "SentencesToListOfWords",
    "RemoveEmptyStrings",
    "RemoveKaldiNonWords",
    "RemoveMultipleSpaces",
    "RemovePunctuation",
    "RemoveSpecificWords",
    "RemoveWhiteSpace",
    "Strip",
    "SubstituteRegexes",
    "SubstituteWords",
    "ToLowerCase",
    "ToUpperCase",
]


class AbstractTransform(object):
    def __call__(self, sentences: Union[str, List[str]]):
        if isinstance(sentences, str):
            return self.process_string(sentences)
        elif isinstance(sentences, list):
            return self.process_list(sentences)
        else:
            raise ValueError(
                "input {} was expected to be a string or list of strings".format(
                    sentences
                )
            )

    def process_string(self, s: str):
        raise NotImplementedError()

    def process_list(self, inp: List[str]):
        return [self.process_string(s) for s in inp]


class Compose(object):
    def __init__(self, transforms: List[AbstractTransform]):
        self.transforms = transforms

    def __call__(self, text):
        for tr in self.transforms:
            text = tr(text)

        return text


class BaseRemoveTransform(AbstractTransform):
    def __init__(self, tokens_to_remove: List[str], replace_token=""):
        self.tokens_to_remove = tokens_to_remove
        self.replace_token = replace_token

    def process_string(self, s: str):
        for w in self.tokens_to_remove:
            s = s.replace(w, self.replace_token)

        return s

    def process_list(self, inp: List[str]):
        return [self.process_string(s) for s in inp]


class SentencesToListOfWords(AbstractTransform):
    def __init__(self, word_delimiter: str = " "):
        """
        Transforms one or more sentences into a list of words. A sentence is
        assumed to be a string, where words are delimited by a token
        (such as ` `, space). Each string is expected to contain only a single sentence.

        :param word_delimiter: the character which delimits words. Default is ` ` (space).
        Default is None (sentences are not delimited)
        """
        self.word_delimiter = word_delimiter

    def process_string(self, s: str):
        return s.split(self.word_delimiter)

    def process_list(self, inp: List[str]):
        words = []

        for sentence in inp:
            words.extend(self.process_string(sentence))

        return words


class RemoveSpecificWords(BaseRemoveTransform):
    def __init__(self, words_to_remove: List[str]):
        super().__init__(words_to_remove)


class RemoveWhiteSpace(BaseRemoveTransform):
    def __init__(self, replace_by_space: bool = False):
        characters = [c for c in string.whitespace]

        if replace_by_space:
            replace_token = " "
        else:
            replace_token = ""

        super().__init__(characters, replace_token=replace_token)


class RemovePunctuation(BaseRemoveTransform):
    def __init__(self):
        characters = [c for c in string.punctuation]

        super().__init__(characters)


class RemoveMultipleSpaces(AbstractTransform):
    def process_string(self, s: str):
        return re.sub(r"\s\s+", " ", s)

    def process_list(self, inp: List[str]):
        return [self.process_string(s) for s in inp]


class Strip(AbstractTransform):
    def process_string(self, s: str):
        return s.strip()


class RemoveEmptyStrings(AbstractTransform):
    def process_string(self, s: str):
        return s.strip()

    def process_list(self, inp: List[str]):
        return [s for s in inp if self.process_string(s) != ""]


class ExpandCommonEnglishContractions(AbstractTransform):
    def process_string(self, s: str):
        # definitely a non exhaustive list

        # specific words
        s = re.sub(r"won't", "will not", s)
        s = re.sub(r"can\'t", "can not", s)
        s = re.sub(r"let\'s", "let us", s)

        # general attachments
        s = re.sub(r"n\'t", " not", s)
        s = re.sub(r"\'re", " are", s)
        s = re.sub(r"\'s", " is", s)
        s = re.sub(r"\'d", " would", s)
        s = re.sub(r"\'ll", " will", s)
        s = re.sub(r"\'t", " not", s)
        s = re.sub(r"\'ve", " have", s)
        s = re.sub(r"\'m", " am", s)

        return s


class SubstituteWords(AbstractTransform):
    def __init__(self, substitutions: Mapping[str, str]):
        self.substitutions = substitutions

    def process_string(self, s: str):
        for key, value in self.substitutions.items():
            s = re.sub(r"\b{}\b".format(re.escape(key)), value, s)

        return s


class SubstituteRegexes(AbstractTransform):
    def __init__(self, substitutions: Mapping[str, str]):
        self.substitutions = substitutions

    def process_string(self, s: str):
        for key, value in self.substitutions.items():
            s = re.sub(key, value, s)

        return s


class ToLowerCase(AbstractTransform):
    def process_string(self, s: str):
        return s.lower()


class ToUpperCase(AbstractTransform):
    def process_string(self, s: str):
        return s.upper()


class RemoveKaldiNonWords(AbstractTransform):
    def process_string(self, s: str):
        return re.sub(r"[<\[][^>\]]*[>\]]", "", s)

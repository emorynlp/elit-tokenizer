# ========================================================================
# Copyright 2021 Emory University
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
# ========================================================================

__author__ = 'Jinho D. Choi'

import string
from typing import List, Tuple, Set, Optional

Offset = Tuple[int, int]


class TokenList:
    def __init__(self, tokens: List[str], offsets: List[Offset]):
        """
        :param tokens: a list of tokens.
        :param offsets: a list of offsets corresponding to the tokens where an offset is represented by (begin_index, end_index) (begin_index: incluisve, end_index: exclusive).
        """
        self._iter = -1
        self.tokens = tokens
        self.offsets = offsets

    def __len__(self):
        """
        :return: the number of tokens in the sentence.
        """
        return len(self.tokens)

    def __iter__(self):
        self._iter = -1
        return self

    def __next__(self):
        self._iter += 1
        if self._iter >= len(self.tokens):
            raise StopIteration
        return self.tokens[self._iter], self.offsets[self._iter]

    def token(self, index) -> Optional[str]:
        """
        :param index: a token index.
        :return: the index'th token if exists; otherwise, None.
        """
        return self.tokens[index] if 0 <= index < len(self.tokens) else None

    def offset(self, index) -> Offset:
        """
        :param index: a token index.
        :return: the index'th offset if exists; otherwise, (-1, -1)
        """
        return self.offsets[index] if 0 <= index < len(self.offsets) else (-1, -1)


def read_word_set(filename) -> Set[str]:
    """
    :param filename: the name of the file containing one key per line.
    :return: a set containing all keys in the file.
    """
    with open(filename, encoding='utf-8') as fin:
        s = set(line.strip() for line in fin)
    return s


def read_concat_word_dict(filename) -> dict:
    """
    :param filename: the name of the file containing one key per line.
    :return: a dictionary whose key is the concatenated word and value is the list of split points.
    """

    def key_value(line):
        l = [i for i, c in enumerate(line) if c == ' ']
        l = [i - o for o, i in enumerate(l)]
        line = line.replace(' ', '')
        l.append(len(line))
        return line, l

    with open(filename, encoding='utf-8') as fin:
        d = dict(key_value(line.strip()) for line in fin)
    return d


def is_range(c, begin, end):
    return begin <= c <= end


def is_single_quote(c):
    return c in {'\'', '`'} or is_range(c, u'\u2018', u'\u201B')


def is_double_quote(c):
    return c == '"' or is_range(c, u'\u201C', u'\u201F')


def is_left_bracket(c):
    return c in {'(', '{', '[', '<'}


def is_right_bracket(c):
    return c in {')', '}', ']', '>'}


def is_bracket(c):
    return is_left_bracket(c) or is_right_bracket(c)


def is_hyphen(c):
    return c == '-' or is_range(c, u'\u2010', u'\u2014')


def is_arrow(c):
    return is_range(c, u'\u2190', u'\u21FF') or is_range(c, u'\u27F0', u'\u27FF') or is_range(c, u'\u2900', u'\u297F')


def is_currency(c):
    return c == '$' or is_range(c, u'\u00A2', u'\u00A5') or is_range(c, u'\u20A0', u'\u20CF')


def is_final_mark(c):
    return c in {'.', '?', '!', u'\u203C'} or is_range(c, u'\u2047', u'\u2049')


def is_punct(c):
    return c in string.punctuation

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
import pytest

__author__ = 'Jinho D. Choi'

from elit_tokenizer.util import TokenList

# def test_eng_tokenizer_load(english_tokenizer):
#     assert len(english_tokenizer.ABBREVIATION_PERIOD) == 159
#     assert len(english_tokenizer.APOSTROPHE_FRONT) == 7
#     assert len(english_tokenizer.HYPHEN_PREFIX) == 156
#     assert len(english_tokenizer.HYPHEN_SUFFIX) == 39


@pytest.mark.parametrize('input, offset, expected', [
    ('  Hello\t\r, world  !\n\n', 0, [TokenList(['Hello', ',', 'world', '!'], [(2, 7), (9, 10), (11, 16), (18, 19)])]),
    ('  Hello\t\r, world  !\n\n', 1, [TokenList(['Hello', ',', 'world', '!'], [(3, 8), (10, 11), (12, 17), (19, 20)])])
])
def test_space_tokenizer(space_tokenizer, test_sentences, input, offset, expected):
    result = space_tokenizer.decode(input, offset, segment=2)
    test_sentences(result, expected)


@pytest.mark.parametrize('input, expected', [
    ('', TokenList([], [])),
    (' \t\n\r', TokenList([], [])),
    ('abc', TokenList(['abc'], [(0, 3)])),
    (' A\tBC  D12 \n', TokenList(['A', 'BC', 'D12'], [(1, 2), (3, 5), (7, 10)]))
])
def test_eng_tokenizer_space(english_tokenizer, test_sentence, input, expected):
    result = english_tokenizer.decode(input, segment=0)
    test_sentence(result, expected)


@pytest.mark.parametrize('input, offset, expected', [
    ('Hello, world!', 5, TokenList(['Hello', ',', 'world', '!'], [(5, 10), (10, 11), (12, 17), (17, 18)]))
])
def test_eng_tokenizer_offset(english_tokenizer, test_sentence, input, offset, expected):
    result = english_tokenizer.decode(input, offset, segment=0)
    test_sentence(result, expected)


@pytest.mark.parametrize('input, expected', [
    # html entity
    ('ab&larr;cd&#8592;&#x2190;ef&rarr;',
     TokenList(['ab', '&larr;', 'cd', '&#8592;', '&#x2190;', 'ef', '&rarr;'],
               [(0, 2), (2, 8), (8, 10), (10, 17), (17, 25), (25, 27), (27, 33)])),
    # email address
    ('a;jinho@elit.com,b;jinho.choi@elit.com,choi@elit.emory.edu,jinho:choi@0.0.0.0',
     TokenList(['a', ';', 'jinho@elit.com', ',', 'b', ';', 'jinho.choi@elit.com', ',', 'choi@elit.emory.edu', ',', 'jinho:choi@0.0.0.0'],
               [(0, 1), (1, 2), (2, 16), (16, 17), (17, 18), (18, 19), (19, 38), (38, 39), (39, 58), (58, 59), (59, 77)])),
    # hyperlink
    ('a:http://ab sftp://ef abeftp://',
     TokenList(['a', ':', 'http://ab', 'sftp://ef', 'abe', 'ftp://'], [(0, 1), (1, 2), (2, 11), (12, 21), (22, 25), (25, 31)])),
    # list item
    ('[a](1)(1.a)[11.22.a.33](A.1)[a1][hello]{22}',
     TokenList(['[a]', '(1)', '(1.a)', '[11.22.a.33]', '(A.1)', '[a1]', '[', 'hello', ']', '{22}'],
               [(0, 3), (3, 6), (6, 11), (11, 23), (23, 28), (28, 32), (32, 33), (33, 38), (38, 39), (39, 43)])),
    ("don't he's can't does'nt 0's DON'IN ab'cd",
     TokenList(['do', "n't", 'he', "'s", 'ca', "n't", 'does', "'nt", "0's", "DON'IN", "ab'cd"],
               [(0, 2), (2, 5), (6, 8), (8, 10), (11, 13), (13, 16), (17, 21), (21, 24), (25, 28), (29, 35), (36, 41)])),
    # handle symbols with digits
    (".1 +1 -1 1,000,000.00 1,00 '97 '90s '1990 10:30 1:2 a:b",
     TokenList(['.1', '+1', '-1', '1,000,000.00', '1', ',', '00', "'97", "'90s", "'", '1990', '10:30', '1:2', 'a', ':', 'b'],
               [(0, 2), (3, 5), (6, 8), (9, 21), (22, 23), (23, 24), (24, 26), (27, 30), (31, 35), (36, 37), (37, 41), (42, 47), (48, 51), (52, 53), (53, 54), (54, 55)])),
    # separator and edge symbols
    ("aa;;;b: c\"\"d\"\" 0'''s ''a''a'' 'a'a'a'.?!..",
     TokenList(['aa', ';;;', 'b', ':', 'c', '""', 'd', '""', '0', "'''", 's', "''", 'a', "''", 'a', "''", "'", "a'a'a", "'", '.?!..'],
               [(0, 2), (2, 5), (5, 6), (6, 7), (8, 9), (9, 11), (11, 12), (12, 14), (15, 16), (16, 19), (19, 20), (21, 23), (23, 24), (24, 26), (26, 27), (27, 29), (30, 31), (31, 36), (36, 37), (37, 42)])),
    # currency like
    ('#happy2018,@Jinho_Choi: ab@cde #1 $1 ',
     TokenList(['#happy2018', ',', '@Jinho_Choi', ':', 'ab@cde', '#', '1', '$', '1'],
               [(0, 10), (10, 11), (11, 22), (22, 23), (24, 30), (31, 32), (32, 33), (34, 35), (35, 36)])),
    # hyphen
    ("1997-2012,1990's-2000S '97-2012 '12-14's",
     TokenList(['1997', '-', '2012', ',', "1990's", '-', '2000S', "'97", '-', '2012', "'12", '-', "14's"],
               [(0, 4), (4, 5), (5, 9), (9, 10), (10, 16), (16, 17), (17, 22), (23, 26), (26, 27), (27, 31), (32, 35), (35, 36), (36, 40)]))
])
def test_eng_tokenizer_regex(english_tokenizer, test_sentence, input, expected):
    result = english_tokenizer.decode(input, segment=0)
    test_sentence(result, expected)


@pytest.mark.parametrize('input, expected', [
    # emoticon
    (':-) A:-( :). B:smile::sad: C:):(! :)., :-))) :---( Hi:).',
     [TokenList([':-)', 'A', ':-(', ':)', '.'], [(0, 3), (4, 5), (5, 8), (9, 11), (11, 12)]),
      TokenList(['B', ':smile:', ':sad:', 'C', ':)', ':(', '!'], [(13, 14), (14, 21), (21, 26), (27, 28), (28, 30), (30, 32), (32, 33)]),
      TokenList([':)', '.'], [(34, 36), (36, 37)]),
      TokenList([',', ':-)))', ':---(', 'Hi', ':)', '.'], [(37, 38), (39, 44), (45, 50), (51, 53), (53, 55), (55, 56)])]),
])
def test_eng_tokenizer_regex2(english_tokenizer, test_sentences, input, expected):
    result = english_tokenizer.decode(input, segment=2)
    test_sentences(result, expected)


@pytest.mark.parametrize('input, expected', [
    # apostrophe for abbreviation
    ("'CAUSE 'tis ' em 'happy",
     TokenList(["'CAUSE", "'tis", "'em", "'", 'happy'], [(0, 6), (7, 11), (12, 16), (17, 18), (18, 23)])),
    # acronym
    ('ab&cd AB|CD 1/2 a-1 1-2',
     TokenList(['ab&cd', 'AB|CD', '1/2', 'a-1', '1-2'], [(0, 5), (6, 11), (12, 15), (16, 19), (20, 23)])),
    # hyphenated
    ('mis-predict mic-predict book - able book-es 000-0000 000-000-000 p-u-s-h-1-2',
     TokenList(['mis-predict', 'mic', '-', 'predict', 'book-able', 'book', '-', 'es', '000-0000', '000-000-000', 'p-u-s-h-1-2'],
               [(0, 11), (12, 15), (15, 16), (16, 23), (24, 35), (36, 40), (40, 41), (41, 43), (44, 52), (53, 64), (65, 76)])),
])
def test_eng_tokenizer_concat(english_tokenizer, test_sentence, input, expected):
    result = english_tokenizer.decode(input, segment=0)
    test_sentence(result, expected)


@pytest.mark.parametrize('input, expected', [
    # abbreviation
    ('A.B. a.B.c AB.C. Ph.D. 1.2. A-1.',
     [TokenList(['A.B.', 'a.B.c', 'AB.C', '.'], [(0, 4), (5, 10), (11, 15), (15, 16)]),
      TokenList(['Ph.D.', '1.2.', 'A-1.'], [(17, 22), (23, 27), (28, 32)])]),
    # No. 1
    ('No. 1 No. a No.',
     [TokenList(['No.', '1', 'No', '.'], [(0, 3), (4, 5), (6, 8), (8, 9)]),
      TokenList(['a', 'No', '.'], [(10, 11), (12, 14), (14, 15)])])
])
def test_eng_tokenizer_concat2(english_tokenizer, test_sentences, input, expected):
    result = english_tokenizer.decode(input, segment=2)
    test_sentences(result, expected)


@pytest.mark.parametrize('input, expected', [
    # unit
    ('20mg 100cm 1st 11a.m. 10PM',
     TokenList(['20', 'mg', '100', 'cm', '1st', '11', 'a.m.', '10', 'PM'],
               [(0, 2), (2, 4), (5, 8), (8, 10), (11, 14), (15, 17), (17, 21), (22, 24), (24, 26)])),
    # concatenated word
    ("whadya DON'CHA",
     TokenList(['wha', 'd', 'ya', 'DO', "N'", 'CHA'], [(0, 3), (3, 4), (4, 6), (7, 9), (9, 11), (11, 14)])),
])
def test_eng_tokenizer_split(english_tokenizer, test_sentence, input, expected):
    result = english_tokenizer.decode(input, segment=0)
    test_sentence(result, expected)


@pytest.mark.parametrize('input, expected', [
    # final mark
    ('Mbaaah.Please hello.!?world',
     [TokenList(['Mbaaah', '.'], [(0, 6), (6, 7)]),
      TokenList(['Please', 'hello', '.!?'], [(7, 13), (14, 19), (19, 22)]),
      TokenList(['world'], [(22, 27)])]),
])
def test_eng_tokenizer_split2(english_tokenizer, test_sentences, input, expected):
    result = english_tokenizer.decode(input, segment=2)
    test_sentences(result, expected)

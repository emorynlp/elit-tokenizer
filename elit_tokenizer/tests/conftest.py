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

__author__ = "Jinho D. Choi"

import os
from typing import List

import pytest

from elit_tokenizer import Tokenizer, SpaceTokenizer, EnglishTokenizer
from elit_tokenizer.util import TokenList

current_path = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture()
def space_tokenizer():
    return SpaceTokenizer()


@pytest.fixture()
def english_tokenizer():
    return EnglishTokenizer()


@pytest.fixture
def test_sentence():
    def _aux(result: TokenList, expected: TokenList):
        assert result.tokens == expected.tokens
        assert result.offsets == expected.offsets
    return _aux


@pytest.fixture
def test_sentences():
    def _aux(result: List[TokenList], expected: List[TokenList]):
        for r, e in zip(result, expected):
            assert r.tokens == e.tokens
            assert r.offsets == e.offsets
    return _aux

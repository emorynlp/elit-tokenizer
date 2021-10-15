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
from elit_tokenizer import SpaceTokenizer, EnglishTokenizer

# tokenize by whitespaces
text = 'Emory NLP is a research lab in Atlanta, GA.\nIt is founded by Jinho D. Choi in 2014.\nDr. Choi is a professor at Emory University.'
tokenizer = SpaceTokenizer()

sentence = tokenizer.decode(text)
print(sentence.tokens)
print(sentence.offsets)

# tokenize by whitespaces and segment them into sentences by newlines
sentences = tokenizer.decode(text, segment=1)
for sentence in sentences:
    print([(token, offset) for token, offset in sentence])

# tokenize by heuristics
text = 'Emory NLP is a research lab in Atlanta, GA. It is founded by Jinho D. Choi in 2014. Dr. Choi is a professor at Emory University.'
tokenizer = EnglishTokenizer()

sentence = tokenizer.decode(text)
print(sentence.tokens)
print(sentence.offsets)

# tokenize by heuristics and segment them into sentences using heuristics
sentences = tokenizer.decode(text, segment=2)
for sentence in sentences:
    print([(token, offset) for token, offset in sentence])
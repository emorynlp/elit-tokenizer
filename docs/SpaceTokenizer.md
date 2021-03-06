# Space Tokenizer

Space Tokenizer splits tokens by whitespaces:

```python
from elit_tokenizer import SpaceTokenizer

text = 'Emory NLP is a research lab in Atlanta, GA.\nIt is founded by Jinho D. Choi in 2014.\nDr. Choi is a professor at Emory University.'
tokenizer = SpaceTokenizer()

sentence = tokenizer.decode(text)
print(sentence.tokens)
print(sentence.offsets)
```
* `segment=0`: no segmentation (default)
* `segment=1`: segment by newlines
* `segment=2`: segment using heuristics
* `segment=3`: segment by both newlines and heuristics

Output:
```python
['Emory', 'NLP', 'is', 'a', 'research', 'lab', 'in', 'Atlanta,', 'GA.', 'It', 'is', 'founded', 'by', 'Jinho', 'D.', 'Choi', 'in', '2014.', 'Dr.', 'Choi', 'is', 'a', 'professor', 'at', 'Emory', 'University.']
[(0, 5), (6, 9), (10, 12), (13, 14), (15, 23), (24, 27), (28, 30), (31, 39), (40, 43), (44, 46), (47, 49), (50, 57), (58, 60), (61, 66), (67, 69), (70, 74), (75, 77), (78, 83), (84, 87), (88, 92), (93, 95), (96, 97), (98, 107), (108, 110), (111, 116), (117, 128)]
```

If you set `segment=1`, it segments tokens into sentences by newlines:

```python
sentences = tokenizer.decode(text, segment=1)
for sentence in sentences:
    print([(token, offset) for token, offset in sentence])
```

Output:
```python
[('Emory', (0, 5)), ('NLP', (6, 9)), ('is', (10, 12)), ('a', (13, 14)), ('research', (15, 23)), ('lab', (24, 27)), ('in', (28, 30)), ('Atlanta,', (31, 39)), ('GA.', (40, 43))]
[('It', (44, 46)), ('is', (47, 49)), ('founded', (50, 57)), ('by', (58, 60)), ('Jinho', (61, 66)), ('D.', (67, 69)), ('Choi', (70, 74)), ('in', (75, 77)), ('2014.', (78, 83))]
[('Dr.', (84, 87)), ('Choi', (88, 92)), ('is', (93, 95)), ('a', (96, 97)), ('professor', (98, 107)), ('at', (108, 110)), ('Emory', (111, 116)), ('University.', (117, 128))]
```
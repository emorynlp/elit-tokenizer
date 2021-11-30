# English Tokenizer

English Tokenizer splits tokens using heuristics to handle common abbreviations, apostrophes, compound words, hyphens, network protocols, emojis, emails, html entities, list item units:

```python
from elit_tokenizer import EnglishTokenizer

text = 'Emory NLP is a research lab in Atlanta, GA. It is founded by Jinho D. Choi in 2014. Dr. Choi is a professor at Emory University.'
tokenizer = EnglishTokenizer()

sentence = tokenizer.decode(text)
print(sentence.tokens)
print(sentence.offsets)
```

Output:
```python
['Emory', 'NLP', 'is', 'a', 'research', 'lab', 'in', 'Atlanta', ',', 'GA', '.', 'It', 'is', 'founded', 'by', 'Jinho', 'D.', 'Choi', 'in', '2014', '.', 'Dr.', 'Choi', 'is', 'a', 'professor', 'at', 'Emory', 'University', '.']
[(0, 5), (6, 9), (10, 12), (13, 14), (15, 23), (24, 27), (28, 30), (31, 38), (38, 39), (40, 42), (42, 43), (44, 46), (47, 49), (50, 57), (58, 60), (61, 66), (67, 69), (70, 74), (75, 77), (78, 82), (82, 83), (84, 87), (88, 92), (93, 95), (96, 97), (98, 107), (108, 110), (111, 116), (117, 127), (127, 128)]
```

If you set `segment=2`, it segments tokens into sentences using heuristics:

```python
sentences = tokenizer.decode(text, segment=2)
for sentence in sentences:
    print([(token, offset) for token, offset in sentence])
```

Output:
```python
[('Emory', (0, 5)), ('NLP', (6, 9)), ('is', (10, 12)), ('a', (13, 14)), ('research', (15, 23)), ('lab', (24, 27)), ('in', (28, 30)), ('Atlanta', (31, 38)), (',', (38, 39)), ('GA', (40, 42)), ('.', (42, 43))]
[('It', (44, 46)), ('is', (47, 49)), ('founded', (50, 57)), ('by', (58, 60)), ('Jinho', (61, 66)), ('D.', (67, 69)), ('Choi', (70, 74)), ('in', (75, 77)), ('2014', (78, 82)), ('.', (82, 83))]
[('Dr.', (84, 87)), ('Choi', (88, 92)), ('is', (93, 95)), ('a', (96, 97)), ('professor', (98, 107)), ('at', (108, 110)), ('Emory', (111, 116)), ('University', (117, 127)), ('.', (127, 128))]
```

## Key Features

| Feature | Input Text | Tokens |
|---------|------------|--------|
| Email addresses | `Email (support@elit.cloud)`                    | [`Email`, `(`, `support@elit.cloud`, `)`] |
| Hyperlinks      | `URL: https://elit.cloud`                       | [`URL`, `:`, `https://elit.cloud`] |
| Emoticons       | `I love ELIT :-)!?.`                            | [`I`, `love`, `ELIT`, `:-)`, `!?.`] |
| Hashtags        | `ELIT is the #1 platform #elit2018.`            | [`ELIT`, `is`, `the`, `#`, `1`, `platform`, `#elit2018`, `.`] |
| HTML entities   | `A&larr;B`                                      | [`A`, `&larr;`, `B`] |
| Hyphens         | `(123) 456-7890, 123-456-7890, 2014-2018`       | [`(123)`, `456-7890`, `,`, `123-456-7890`, `,`, `2014`, `-`, `2018`] |
| List items      | `(A)First (A.1)Second [2a]Third [Forth]`        | [`(A)`, `First`, `(A.1)`, `Second`, `[2a]`, `Third`, `[`, `Forth`, `]`] |
| Units           | `$1,000 20mg 100cm 11:00a.m. 10:30PM`           | [`$`, `1,000`, `20`, `mg`, `100`, `cm`, `11:00`, `a.m.`, `10:30`, `PM`] |
| Acronyms        | `I'm gonna miss Dr. Choi 'cause he isn't here.` | [`I`, `'m`, `gon`, `na`, `miss`, `Dr.`, `Choi`, `'cause`, `he`, `is`, `n't`, `here`, `.`] |

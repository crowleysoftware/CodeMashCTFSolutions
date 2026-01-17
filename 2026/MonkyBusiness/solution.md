# Monky Business

### Challenge

There is a big clue in the title: "Monky Business". You may notice the typical phrase, Monkey Business, is misspelled. This is meant to clue you in to the fact that "Monk", not "Monkey" is what you shold be pondering.

What you open the supplied image file you see:

![Monky Business](monky.png "Monky Business")

Clearly this must be some sort of encoding that hides a message. But what kind of encoding???

If you Google "monk encoding" the first result is [Cistercian numerals](https://en.wikipedia.org/wiki/Cistercian_numerals).

Based on this information, you should be able to convert each symbol into a number. For instance:

![99](c.png)

represents 99, which is the code point for "c".

If you continue to decode all the symbols in the same say you will discover the flag.

In javascript you could :

    String.fromCharCode(...[99, 116, 102, 111, 109, 101, 103, 97, 102, 108, 117, 120, 99, 97, 114, 100, 112, 108, 117, 115])

output:
> ctfomegafluxcardplus

You just need to put the "-"'s in.
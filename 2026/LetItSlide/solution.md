# Let it slide

> Get the image: `docker pull crowcoder/codemash-ctf:letitslide`

This is a variation of a Caesar cipher known as the Vigenère Cipher. But instead of each letter using the same offset, each letter has a different offset. The offset is denoted by the key "CODEMASH". For each letter in the key you shift the encoded letter by the same distance that the key letter is from A. If the key is shorter than the message you simply start over at the start of the key.

The cipher: TWYIDSLVPSFPAUVMQFHWF

For example, the first letter of the key is "C". This is a shift of two places from "A". So, you would shift the first encrypted letter two places: T -> R

Here's the entire break down:

|Key | Offset from A | Encoded Letter | Shift by offset to Decode |  
|---|---|---|---|
|C|2|T|R|
|O|14|W|I|
|D|3|Y|V|
|E|4|I|E|
|M|12|D|R|
||||-|
|A|0|S|S|
|S|18|L|T|
|H|7|V|O|
|C|2|P|N|
|O|14|S|E|
||||-|
|D|3|F|C|
|E|4|P|L|
|M|12|A|O|
|A|0|U|U|
|S|18|V|D|
||||-|
|H|7|M|F|
|C|2|Q|O|
|O|14|F|R|
|D|3|H|E|
|E|4|W|S|
|M|12|F|T|

The sliders are there to help you get the shifts correct. Move the bottom bar so the key letter aligns with the top bar's "A". Then move the black box to the cipher's letter in the bottom bar. The letter it aligns with on the top is the decrypted letter.

For example, If you drag the gray bar so that "C" is under "A" and look at the letter that appears above "T" (the first encrypted letter), you get the decoded value of "R" (the first letter of the flag).
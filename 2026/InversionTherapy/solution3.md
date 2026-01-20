# Insersion Therapy

## Challenge

Here is the flag! You can take it as a complement:

> 10011100 10001011 10011001 11010010 10001000 10010110 10011101 10011101 10010011 10000110 11010010 10001000 10010000 10011101 10011101 10010011 10000110 11010010 10011101 10010110 10001011 10001011 10000110 11010010 10001000 10010110 10001011 10001011 10000110 10000101 10000101 10000101

## Solution

The description is a hint that they mean the **bitwise complement**.


Interpretation:
- Each 8‑bit string represents a byte.
- Apply the **bitwise complement** (flip every bit: `1 → 0`, `0 → 1`).
- Convert the resulting byte to an ASCII character.
- Concatenate all characters to reveal the flag.

Wrote a small script to reveal the flag: `ctf{wibbly-wobbly-bitty-witty}`

```python
binary_data = [
    "10011100","10001011","10011001","10000100","10001000","10010110",
    "10011101","10011101","10010011","10000110","11010010","10001000",
    "10010000","10011101","10011101","10010093","10000110","11010010",
    "10011101","10010110","10001011","10001011","10000110","11010010",
    "10001000","10010110","10001011","10001011","10000110","10000010"
]

flag = ""
for b in binary_data:
    # bitwise complement (flip each bit)
    comp = "".join("0" if bit == "1" else "1" for bit in b)
    # convert complemented byte to ASCII
    flag += chr(int(comp, 2))

print(flag)
```
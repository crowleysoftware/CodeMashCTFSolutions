# Inversion Therapy
Here is the flag! You can take it as a complement:

> 10011100 10001011 10011001 11010010 10001000 10010110 10011101 10011101 10010011 10000110 11010010 10001000 10010000 10011101 10011101 10010011 10000110 11010010 10011101 10010110 10001011 10001011 10000110 11010010 10001000 10010110 10001011 10001011 10000110 10000101 10000101 10000101

## Solution
To solve the "Inversion Therapy" challenge, follow these steps:
1. **Understand the Encoding**: The provided string is a series of 8-bit binary numbers separated by spaces. Each 8-bit segment represents a byte, which can be converted to its decimal equivalent and then to an ASCII character.
2. **Convert Binary to Decimal**: For each 8-bit binary number, convert it to its decimal equivalent. For example, the binary `10011100` converts to the decimal `156`.
3. **Find the Complement**: Since the challenge hints at taking the complement, you need to find the bitwise complement of each byte. The bitwise complement of a byte is obtained by flipping all bits (changing 0s to 1s and 1s to 0s). For example, the complement of `10011100` is `01100011`, which is `99` in decimal.
4. **Convert Decimal to ASCII**: After obtaining the decimal values of the complemented bytes, convert each decimal value to its corresponding ASCII character. Continuing the example, `99` corresponds to the character 'c'.
5. **Assemble the Flag**: Combine all the ASCII characters obtained from the previous step to form the final flag string.
Here is a Python script that performs these steps:

```python
binary_string = "10011100 10001011 10011001 11010010 10001000 10010110 10011101 10011101 10010011 10000110 11010010 10001000 10010000 10011101 10011101 10010011 10000110 11010010 10011101 10010110 10001011 10001011 10000110 11010010 10001000 10010110 10001011 10001011 10000110 10000101 10000101 10000101"   
flag = ""
for byte in binary_string.split():
    # Convert binary to decimal
    decimal_value = int(byte, 2)
    # Find the bitwise complement
    complement_value = 255 - decimal_value
    # Convert to ASCII character
    flag += chr(complement_value)
print(flag)
```

When you run this script, it will output the flag.
# Choose Wisely

## Challenge

Given a hash: `650e00a89da4bbc27f12148893517b0aa028efd1b5c1051dfbd5d3ddf50ad9ff`

And a long list of candidates:

```
ctf{sierra-moon-stone-echo}
ctf{quebec-purple-red-whiskey}
etc...
```

## Solution

This *is* the correct flag, but not in a submit‑ready format. Only one of the candidate flags hashes via SHA‑256 to the provided value.

I wrote a small script to loop through each each candidate:
 
- Compute its **SHA‑256** hash  
- Compare it to the given hash  
- When a match is found, that's the valid flag


```python
import hashlib

hash_to_match = "650e00a89da4bbc27f12148893517b0aa028efd1b5c1051dfbd5d3ddf50ad9ff"
candidates = [
        "ctf{sierra-moon-stone-echo}",
        "ctf{quebec-purple-red-whiskey}",
        "etc...",
]

for flag in candidates:
    h = hashlib.sha256(flag.encode()).hexdigest()
    if h == hash_to_match:
        print("Found the flag:", flag)
        break
```

Running the script produced the flag (replacing the starting and ending - with {}): `ctf{shadow-flame-gear-arc}`

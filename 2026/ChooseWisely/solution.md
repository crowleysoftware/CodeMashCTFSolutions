# Choose Wisely

### Challenge
  This is the flag, but you can't submit it looking like this:

  650e00a89da4bbc27f12148893517b0aa028efd1b5c1051dfbd5d3ddf50ad9ff

  You can also find the flag in this list. How much easier can it get?
  
  ````
  ctf-apple-rocket-silver-moon
  ctf-tiger-cloud-frost-lamp
  ctf-echo-spark-iron-leaf
  ctf-quantum-pixel-shadow-wave
  ctf-lunar-crystal-ember-hawk
  ctf-forest-omega-flame-gear
  ctf-ruby-phantom-ice-orbit
  ctf-vortex-sunrise-ghost-arc
  ctf-zenith-blade-mystic-fog
  ctf-ember-echo-void-star
  ctf-horizon-flux-rapid-stone
  etc..  
  etc..  
````

You need to figure out what relationship the seemingly random string has to the list of flags. 

Hopefully you will come to the conclusion that the value is a hash. But which type? If you recognize the values as hexadecimal you can determine this hash is 32 bytes. At 32 bytes you are almost certainly dealing with SHA256.

Going one-by-one you can hash each flag and see if it matches the challenge. The one that matches is the flag we are looking for. Better yet, write a utility to loop over each one. Here's a PowerShell script to get you started:

````
# Create SHA256 object
$hasher = [System.Security.Cryptography.HashAlgorithm]::Create("sha256")
$hashBytes = $hasher.ComputeHash([System.Text.Encoding]::UTF8.GetBytes("put the flag here"))

# Convert to hex string
($hashBytes | ForEach-Object { $_.ToString("x2") }) -join ''

````


Of course you can always brute force the system by trying to submit each flag until it works if it allows that many tries. This is a valid, if not tedious strategy and it demonstrates the importance of rate limits and retry restrictions.
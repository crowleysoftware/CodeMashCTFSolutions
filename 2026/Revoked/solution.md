# Revoked

The revoked token can be retrieved from `/jrl`.

In the signature part of the JWT, change the `-`'s to `+`'s. This remains a valid [Base64 encoding](https://en.wikipedia.org/wiki/Base64#Variants) while not matching the revoked token.

Set the modified JWT as a cookie in your request to `/flag`.

# Name That Animal

> Get the image: `docker pull crowcoder/codemash-ctf:namethatanimal`

### Challenge
**Its simple, just submit the name of the animal in the photo.**

The link shows you a picture of an elephant and there is a simple form where all you have to do is type in the name of the animal. If you submit the name of the animal, you get the flag.

![Name that animal](namethatanimal.png)

The problem is that the text box only accepts 5 characters. No matter what you try to type in, you get an error message:

> Incorrect. Try again!

You need to figure out a different way to submit the name. If you review the network traffic, you will see that the form is submitting a POST request to the server:

![POST](request.png)

 If you recreate this request with your favorite HTTP client, you can submit the name of the animal and get the flag. This is a classic case of trusting the front end to enforce security.

> cURL example:

```curl
curl -X POST --location "http://localhost:3000/api/submit" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "value=Elephant"
```

> .http client example:

```
### Get flag
POST http://localhost:3000/api/submit
Content-Type: application/x-www-form-urlencoded

value=Elephant
```

> Insomnia example:

![insomnia](insomnia.png)
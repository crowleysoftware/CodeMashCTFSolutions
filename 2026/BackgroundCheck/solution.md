# Background Check

> Get the image: `docker pull crowcoder/codemash-ctf:backgroundcheck`

## Challenge Description
You’ve stumbled onto a suspicious-looking web page filled with an overwhelming wall of text. At first glance, it looks like nothing but noise. But don’t be fooled—someone has gone to great lengths to conceal a secret here. Enter flag in lower case.
## Solution
To solve the "Background Check" challenge, follow these steps:
1. **Access the Web Page**: Open the provided URL in a web browser to view the suspicious-looking web page filled with text.
2. **Inspect the Page Source**: Use the browser's developer tools to inspect the HTML source code of the page.
3. **Notice the many occurrences of the style flag-frag**: As you scroll through the source code, you'll see that the style "flag-frag" appears repeatedly, often in a way that seems out of place. Maybe if you could view those spans in a different way...
4. **Use Browser Developer Tools**: In the developer tools, you can modify the CSS to make the "flag-frag" elements stand out. You can do this by editing the CSS rule:
   ```css
   .flag-frag {
       color: black;
   }
   ```
   et voila! The hidden message is revealed.
   ![Revealed Flag](bkgrnd_flag.png)
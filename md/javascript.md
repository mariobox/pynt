post
2019-07-12
# JavaScript: The Language of Web Browsers

You can run JavaScript in any modern browser console. JavaScript adds dynamism and interactivity to your web pages.

This is an example of JavaScript code:

<pre><code>
let gallery = "";

const fetchPhotos = async () => {
    const res = await fetch("/js/pix.json");
    const photos = await res.json();
    
}

fetchPhotos();
</code></pre>

[More Info](https://google.com/search?q=javascript)

&larr;[Back](index.html)
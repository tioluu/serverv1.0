(function(){
    const form = document.querySelector('form');
    const resultDiv = document.getElementById('result');

    function findUrl(obj){
        if (!obj) return null;
        if (typeof obj === 'string'){
            if (/^https?:\/\//i.test(obj)) return obj;
            return null;
        }
        if (Array.isArray(obj)){
            for (const v of obj){ const u = findUrl(v); if (u) return u; }
            return null;
        }
        if (typeof obj === 'object'){
            for (const k in obj){ const u = findUrl(obj[k]); if (u) return u; }
        }
        return null;
    }

    form.addEventListener('submit', async (e)=>{
        e.preventDefault();
        resultDiv.textContent = 'Shortening...';
        const url = form.url.value;
        const params = new URLSearchParams();
        params.append('url', url);
        try{
            const res = await fetch('/shorten', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: params.toString()
            });
            const data = await res.json();
            const shortUrl = data && (data.short_url || data.shortUrl || data.short_link || data.shortenedUrl);
            if (shortUrl){
                resultDiv.innerHTML = `<p>Short link: <a href="${shortUrl}" target="_blank" rel="noopener noreferrer">${shortUrl}</a></p>`;
            } else {
                resultDiv.textContent = 'Shortened URL not found in response.';
                console.log('Response JSON:', data);
            }
        }catch(err){
            resultDiv.textContent = 'Error creating short link.';
            console.error(err);
        }
    });
})();

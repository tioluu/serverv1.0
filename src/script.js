(function(){
    const form = document.querySelector('form');
    const resultDiv = document.getElementById('result');

    function isValidUrl(value){
        if (!value) return false;
        return /^https?:\/\//i.test(value.trim());
    }

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
        const url = form.url.value.trim();
        if (!isValidUrl(url)){
            resultDiv.textContent = 'Please enter a valid URL that starts with http:// or https://';
            return;
        }
        resultDiv.textContent = 'Shortening...';
        const params = new URLSearchParams();
        params.append('url', url);
        try{
            const res = await fetch('/shorten', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: params.toString()
            });
            let data = null;
            try{
                data = await res.json();
            } catch (_err){
                data = null;
            }
            if (!res.ok){
                const message = data && (data.message || data.error || data.detail);
                resultDiv.textContent = message || `Shortener request failed (HTTP ${res.status}).`;
                return;
            }
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

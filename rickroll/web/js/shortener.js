const getBaseUrl = () => {
    return `${window.location.protocol}//${window.location.host}`;
};

const API_BASE = "/api";

async function shortenLink() {
    const urlInput = document.getElementById('urlInput');
    const shortenBtn = document.getElementById('shortenBtn');
    const resultCard = document.getElementById('resultCard');
    
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Пожалуйста, введите URL');
        return;
    }
    
    if (!isValidUrl(url)) {
        showError('Пожалуйста, введите корректный URL (должен начинаться с http:// или https://)');
        return;
    }
    
    shortenBtn.classList.add('is-loading');
    hideError();
    
    try {
        const response = await axios.post(`${API_BASE}/links/shorten`, {
            url: url
        });
        
        const data = response.data;
        
        document.getElementById('shortUrl').value = `${getBaseUrl()}${data.short_url}`;
        document.getElementById('originalUrl').textContent = data.original_url;
        document.getElementById('shortCode').textContent = data.short_code;
        
        resultCard.style.display = 'block';
        resultCard.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error shortening link:', error);
        
        if (error.response && error.response.data && error.response.data.detail) {
            showError(`Ошибка: ${error.response.data.detail}`);
        } else {
            showError('Не удалось сократить ссылку. Пожалуйста, попробуйте снова.');
        }
    } finally {
        shortenBtn.classList.remove('is-loading');
    }
}

function copyToClipboard() {
    const shortUrlInput = document.getElementById('shortUrl');
    const copyBtn = document.getElementById('copyBtn');
    
    shortUrlInput.select();
    shortUrlInput.setSelectionRange(0, 99999);
    
    navigator.clipboard.writeText(shortUrlInput.value).then(() => {
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<span class="icon"><i class="fas fa-check"></i></span><span>Copied!</span>';
        copyBtn.classList.remove('is-info');
        copyBtn.classList.add('is-success');
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.classList.remove('is-success');
            copyBtn.classList.add('is-info');
        }, 2000);
    }).catch(() => {
        showError('Не удалось скопировать в буфер обмена');
    });
}

function isValidUrl(string) {
    try {
        new URL(string);
        return string.startsWith('http://') || string.startsWith('https://');
    } catch (_) {
        return false;
    }
}

function showError(message) {
    const errorNotification = document.getElementById('errorNotification');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    errorNotification.style.display = 'block';
    errorNotification.scrollIntoView({ behavior: 'smooth' });
}

function hideError() {
    const errorNotification = document.getElementById('errorNotification');
    errorNotification.style.display = 'none';
}

document.getElementById('urlInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        shortenLink();
    }
});

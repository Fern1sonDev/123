const getBaseUrl = () => {
    return `${window.location.protocol}//${window.location.host}`;
};

const API_BASE = "/api";
        
async function redirectToLink() {
    const pathParts = window.location.pathname.split('/');
    const shortCode = pathParts[pathParts.length - 1];
    
    if (!shortCode) {
        showError();
        return;
    }
    
    try {
        const response = await axios.get(`${API_BASE}/links/${shortCode}`);
        const data = response.data;
        
        window.location.href = data.url;
        
    } catch (error) {
        console.error('Error fetching link:', error);
        showError();
    }
}

function showError() {
    document.getElementById('loadingContent').style.display = 'none';
    document.getElementById('errorContent').style.display = 'block';
}

window.addEventListener('load', redirectToLink);
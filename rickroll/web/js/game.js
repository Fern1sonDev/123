const getBaseUrl = () => {
    return `${window.location.protocol}//${window.location.host}`;
};

const API_BASE = "/api";

let gameSession = null;
let currentGameData = null;

async function startGame() {
    showLoading();
    
    try {
        const response = await axios.post(`${API_BASE}/game/start`);
        gameSession = response.data;
        
        document.getElementById('startScreen').style.display = 'none';
        document.getElementById('gameScreen').style.display = 'block';
        
        await loadNextLink();
        
    } catch (error) {
        console.error('Error starting game:', error);
        showError('Не удалось начать игру. Пожалуйста, попробуйте снова.');
    } finally {
        hideLoading();
    }
}

async function loadNextLink() {
    if (!gameSession) return;
    
    showLoading();
    
    try {
        const response = await axios.get(`${API_BASE}/game/link/${gameSession.session_id}`);
        currentGameData = response.data;
        
        document.getElementById('currentLink').textContent = currentGameData.link_index + 1;
        document.getElementById('coinCount').textContent = currentGameData.coins;
        document.getElementById('currentLinkDisplay').textContent = `${getBaseUrl()}/s/${currentGameData.short_code}`;
        
        document.getElementById('notRickrollBtn').disabled = false;
        document.getElementById('continueBtn').disabled = false;
        
    } catch (error) {
        console.error('Error loading link:', error);
        if (error.response && error.response.status === 400) {
            showEndScreen(false, currentGameData ? currentGameData.coins : 0);
        } else {
            showError('Не удалось загрузить ссылку. Пожалуйста, попробуйте снова.');
        }
    } finally {
        hideLoading();
    }
}

async function makeGuess(guessType) {
    if (!gameSession || !currentGameData) return;
    
    document.getElementById('notRickrollBtn').disabled = true;
    document.getElementById('continueBtn').disabled = true;
    
    showLoading();
    
    try {
        const response = await axios.post(`${API_BASE}/game/guess`, {
            session_id: gameSession.session_id,
            link_index: currentGameData.link_index,
            guess: guessType
        });
        
        const result = response.data;
        
        document.getElementById('coinCount').textContent = result.coins;
        
        if (result.original_url) {
            openLinkInBackground(result.original_url);
        }
        
        if (result.game_over) {
            showEndScreen(result.won, result.coins, result.flag, result.is_rickrolled);
        } else {
            await loadNextLink();
        }
        
    } catch (error) {
        console.error('Error making guess:', error);
        showError('Не удалось отправить ответ. Пожалуйста, попробуйте снова.');
        
        document.getElementById('notRickrollBtn').disabled = false;
        document.getElementById('continueBtn').disabled = false;
    } finally {
        hideLoading();
    }
}

function openLinkInBackground(url) {
    if (url && url.trim() !== '') {
        window.open(url, '_blank');
    }
}

function showEndScreen(won, coins, flag = null, isRickrolled = false) {
    const gameScreen = document.getElementById('gameScreen');
    const endScreen = document.getElementById('endScreen');
    const finalScore = document.getElementById('finalScore');
    const winContent = document.getElementById('winContent');
    const loseContent = document.getElementById('loseContent');
    const flagDisplay = document.getElementById('flagDisplay');
    const endTitle = document.getElementById('endTitle');
    const loseReason = document.getElementById('loseReason');
    
    if (!gameScreen || !endScreen || !finalScore || !winContent || !loseContent || !endTitle || !loseReason) {
        console.error('Required DOM elements not found');
        return;
    }
    
    gameScreen.style.display = 'none';
    endScreen.style.display = 'block';
    
    finalScore.textContent = coins;
    
    if (won && flag) {
        winContent.style.display = 'block';
        loseContent.style.display = 'none';
        flagDisplay.textContent = flag;
        endTitle.innerHTML = '<i class="fas fa-trophy mr-2"></i>Victory!';
    } else {
        winContent.style.display = 'none';
        loseContent.style.display = 'block';
        
        if (isRickrolled) {
            loseReason.textContent = 'Вас зарикроллили!';
            endTitle.innerHTML = '<i class="fas fa-times-circle mr-2"></i>Игра окончена!';
        } else {
            loseReason.textContent = 'Вы завершили игру, но у вас недостаточно монет для победы!';
            endTitle.innerHTML = '<i class="fas fa-times-circle mr-2"></i>Игра окончена!';
        }
    }
}

function resetGame() {
    gameSession = null;
    currentGameData = null;
    
    document.getElementById('endScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'none';
    document.getElementById('startScreen').style.display = 'block';
    
    document.getElementById('coinCount').textContent = '0';
    document.getElementById('currentLink').textContent = '0';
    document.getElementById('currentLinkDisplay').textContent = 'Загрузка...';
    
    hideError();
}

function showLoading() {
    document.getElementById('loadingModal').classList.add('is-active');
}

function hideLoading() {
    document.getElementById('loadingModal').classList.remove('is-active');
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

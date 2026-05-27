let activeDeck = 'finalfantasy';
let progress = {};
let activeCards = [];
let currentIndex = 0;
let isFlipped = false;
let settings = { theme: 'dark', animate: true, sound: true };

// Object to store loaded deck arrays (avoids reloading)
const loadedDecks = {};

// Load settings on startup
function loadSettings() {
  const saved = localStorage.getItem('klepanka_settings');
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      settings = { ...settings, ...parsed };
    } catch(e) {}
  }
  applyTheme();
  applyAnimation();
  applySound();
}

function saveSettings() {
  localStorage.setItem('klepanka_settings', JSON.stringify(settings));
}

function applySound() {
  const btn = document.getElementById('soundIcon');
  if (!btn) return;
  if (settings.sound) {
    btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>`;
  } else {
    btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="23" y1="9" x2="17" y2="15"></line><line x1="17" y1="9" x2="23" y2="15"></line><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon></svg>`;
  }
}

function toggleSound() {
  settings.sound = !settings.sound;
  saveSettings();
  applySound();
}

function applyTheme() {
  if (settings.theme === 'light') {
    document.documentElement.classList.add('light-theme');
    document.getElementById('themeIcon').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
  } else {
    document.documentElement.classList.remove('light-theme');
    document.getElementById('themeIcon').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`;
  }
}

function toggleTheme() {
  settings.theme = settings.theme === 'light' ? 'dark' : 'light';
  saveSettings();
  applyTheme();
}

function applyAnimation() {
  const card = document.getElementById('flashcard');
  if (settings.animate) {
    card.style.transition = 'transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
    document.getElementById('animIcon').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="4" x2="18" y2="20"></line><line x1="6" y1="4" x2="6" y2="20"></line></svg>`;
  } else {
    card.style.transition = 'none';
    document.getElementById('animIcon').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
  }
}

function toggleAnimation() {
  settings.animate = !settings.animate;
  saveSettings();
  applyAnimation();
}

function getGlobalDeckVar(globalVarName) {
  try {
    return window[globalVarName];
  } catch(e) {
    return undefined;
  }
}

// Lazy loading function to download deck arrays on demand (works for both file:// and http://)
function loadDeckScript(deckName, callback) {
  let globalVarName = 'WORDS_' + deckName.toUpperCase();
  if (deckName === 'sevendays') {
    globalVarName = 'WORDS_7DAYS';
  }
  
  const existing = getGlobalDeckVar(globalVarName);
  if (existing) {
    loadedDecks[deckName] = existing;
    callback();
    return;
  }

  showToast("Wczytywanie talii...", false);
  const script = document.createElement('script');
  script.src = 'js/decks/' + deckName + '.js';
  script.onload = () => {
    const loaded = getGlobalDeckVar(globalVarName);
    if (loaded) {
      loadedDecks[deckName] = loaded;
      callback();
    } else {
      showToast("Błąd ładowania talii", true);
    }
  };
  script.onerror = () => {
    showToast("Błąd ładowania talii", true);
  };
  document.head.appendChild(script);
}

function getDeckWords(deckName) {
  return loadedDecks[deckName] || [];
}

function loadProgress() {
  const key = 'klepanka_progress_' + activeDeck;
  try {
    progress = JSON.parse(localStorage.getItem(key)) || {};
  } catch(e) {
    progress = {};
  }
}

function saveProgress() {
  const key = 'klepanka_progress_' + activeDeck;
  localStorage.setItem(key, JSON.stringify(progress));
}

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function applyFilter() {
  const deckWords = getDeckWords(activeDeck);
  // Filter out cards that are already mastered (progress >= 1)
  const cards = deckWords.filter(c => !(progress[c.en] >= 1));
  
  if (cards.length === 0) {
    activeCards = [];
  } else {
    activeCards = shuffle(cards);
  }
  currentIndex = 0;
  isFlipped = false;
}

function getCard() {
  return activeCards[currentIndex];
}

function renderCard() {
  const card = getCard();
  if (!card) {
    document.getElementById('wordFront').textContent = '🎉 Koniec!';
    document.getElementById('wordBack').textContent = 'Wszystkie fiszki opanowane!';
    document.getElementById('flashcard').classList.add('flipped');
    isFlipped = true;
    updateStats();
    
    document.getElementById('btnNope').disabled = true;
    document.getElementById('btnKnow').disabled = true;
    return;
  }
  
  document.getElementById('btnNope').disabled = false;
  document.getElementById('btnKnow').disabled = false;

  document.getElementById('wordFront').textContent = card.en;
  document.getElementById('wordBack').textContent = card.pl;

  document.getElementById('flashcard').classList.remove('flipped');
  isFlipped = false;
}

function updateStats() {
  const deckWords = getDeckWords(activeDeck);
  const total = deckWords.length;
  const known = deckWords.filter(c => (progress[c.en] || 0) >= 1).length;
  const left = total - known;
  const pct = total ? Math.round(known / total * 100) : 0;
  
  document.getElementById('statKnown').textContent = known;
  document.getElementById('statLeft').textContent = left;
  document.getElementById('statPct').textContent = pct + '%';
  document.getElementById('progressBar').style.width = pct + '%';
}

function speakWord(text) {
  if (!settings.sound) return;
  if ('speechSynthesis' in window) {
    // Cancel any active speech
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    
    // Select an English voice
    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(v => v.lang === 'en-US' && v.name.includes('Natural')) || 
                           voices.find(v => v.lang.startsWith('en-US')) || 
                           voices.find(v => v.lang.startsWith('en'));
    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }
    
    window.speechSynthesis.speak(utterance);
  }
}

// Warm up speech synthesis voices list
if ('speechSynthesis' in window) {
  window.speechSynthesis.getVoices();
}

function flipCard() {
  if (activeCards.length === 0) return;
  isFlipped = !isFlipped;
  document.getElementById('flashcard').classList.toggle('flipped', isFlipped);
  
  // Speak the English word on flip
  const card = getCard();
  if (card && card.en) {
    speakWord(card.en);
  }
}

function markKnown() {
  if (document.getElementById('btnKnow').disabled) return;
  const card = getCard();
  if (!card) return;
  
  progress[card.en] = (progress[card.en] || 0) + 1;
  saveProgress();
  
  spawnEmoji('✅');
  showToast(card.en + ' ✓');
  
  nextCard();
}

function markNope() {
  if (document.getElementById('btnNope').disabled) return;
  const card = getCard();
  if (!card) return;
  
  progress[card.en] = 0;
  saveProgress();
  
  spawnEmoji('❌');
  showToast('Do nauki: ' + card.en, true);
  
  nextCard();
}

function nextCard() {
  const card = getCard();
  if (card && progress[card.en] >= 1) {
    activeCards.splice(currentIndex, 1);
    if (activeCards.length === 0) {
      renderCard();
      updateStats();
      return;
    }
    if (currentIndex >= activeCards.length) {
      currentIndex = 0;
    }
  } else {
    if (currentIndex < activeCards.length - 1) {
      currentIndex++;
    } else {
      currentIndex = 0;
      activeCards = shuffle(activeCards);
    }
  }
  
  renderCard();
  updateStats();
}

function resetProgress() {
  if (confirm('Czy na pewno chcesz zresetować postęp w tej talii?')) {
    progress = {};
    saveProgress();
    applyFilter();
    renderCard();
    updateStats();
    showToast('Postęp zresetowany');
  }
}

function spawnEmoji(emoji) {
  const el = document.createElement('div');
  el.className = 'emoji-burst';
  el.textContent = emoji;
  el.style.setProperty('--tx', (Math.random()-0.5)*120+'px');
  el.style.setProperty('--ty', -(80+Math.random()*60)+'px');
  el.style.left = '50%';
  el.style.top = '40%';
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 800);
}

function exportProgress() {
  const data = {
    settings: settings,
    activeDeck: activeDeck,
    progress: {}
  };
  
  // Gather progress for ALL decks
  const decks = ['finalfantasy','baldursgate','fallout','witcher','cyberpunk','poe','oncehuman','sevendays','xanth','lotr','residentevil'];
  for (const d of decks) {
    const key = 'klepanka_progress_' + d;
    try {
      const p = JSON.parse(localStorage.getItem(key));
      if (p && Object.keys(p).length) data.progress[d] = p;
    } catch(e) {}
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'klepanka_save_' + new Date().toISOString().slice(0,10) + '.json';
  a.click();
  showToast('Postęp zapisany! ⬇');
}

function importProgress(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const data = JSON.parse(e.target.result);
      
      // Restore settings
      if (data.settings) {
        settings = { ...settings, ...data.settings };
        saveSettings();
        applyTheme();
        applyAnimation();
        applySound();
      }
      
      // Restore progress for all decks
      if (data.progress) {
        for (const [deck, prog] of Object.entries(data.progress)) {
          const key = 'klepanka_progress_' + deck;
          localStorage.setItem(key, JSON.stringify(prog));
        }
      }
      
      // Restore active deck
      if (data.activeDeck) {
        localStorage.setItem('klepanka_active_deck', data.activeDeck);
        document.getElementById('deckSelect').value = data.activeDeck;
      }
      
      showToast('Postęp wczytany! ⬆');
      
      // Reload current deck
      const d = localStorage.getItem('klepanka_active_deck') || 'finalfantasy';
      changeDeck(d);
    } catch(err) {
      showToast('Błąd pliku!', true);
    }
  };
  reader.readAsText(file);
  event.target.value = '';
}

function showToast(msg, isError = false) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.background = isError ? '#e74c3c' : '#2ecc71';
  t.style.boxShadow = isError ? '0 5px 15px rgba(231, 76, 60, 0.3)' : '0 5px 15px rgba(46, 204, 113, 0.3)';
  t.classList.add('show');
  clearTimeout(t._tid);
  t._tid = setTimeout(() => t.classList.remove('show'), 1500);
}

function initDeck() {
  const savedDeck = localStorage.getItem('klepanka_active_deck') || 'finalfantasy';
  document.getElementById('deckSelect').value = savedDeck;
  changeDeck(savedDeck);
}

function changeDeck(deckName) {
  loadDeckScript(deckName, () => {
    activeDeck = deckName;
    localStorage.setItem('klepanka_active_deck', deckName);
    
    // Toggle class for Path of Exile and 7 Days to Die visual design testing
    document.body.classList.toggle('poe-active', deckName === 'poe');
    document.body.classList.toggle('sevendays-active', deckName === 'sevendays');
    document.body.classList.toggle('oncehuman-active', deckName === 'oncehuman');
    document.body.classList.toggle('finalfantasy-active', deckName === 'finalfantasy');
    document.body.classList.toggle('baldursgate-active', deckName === 'baldursgate');
    document.body.classList.toggle('fallout-active', deckName === 'fallout');
    document.body.classList.toggle('cyberpunk-active', deckName === 'cyberpunk');
    document.body.classList.toggle('witcher-active', deckName === 'witcher');
    document.body.classList.toggle('xanth-active', deckName === 'xanth');
    document.body.classList.toggle('lotr-active', deckName === 'lotr');
    document.body.classList.toggle('residentevil-active', deckName === 'residentevil');
    
    loadProgress();
    applyFilter();
    renderCard();
    updateStats();
  });
}

// Keyboard hotkeys
window.addEventListener('keydown', function(e) {
  if (e.target.tagName === 'SELECT' || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  
  if (e.key === 'ArrowLeft') {
    e.preventDefault();
    markNope();
  } else if (e.key === 'ArrowRight') {
    e.preventDefault();
    markKnown();
  } else if (e.key === 'ArrowDown' || e.key === ' ') {
    e.preventDefault();
    flipCard();
  } else if (e.key === 'r' || e.key === 'R') {
    e.preventDefault();
    resetProgress();
  }
}, { passive: false });

// Init app
loadSettings();
initDeck();

document.addEventListener('DOMContentLoaded', () => {
    // Elementos da interface
    const passwordDisplay = document.getElementById('password-display');
    const lengthSlider = document.getElementById('password-length');
    const lengthDisplay = document.getElementById('length-display');
    const uppercaseCheck = document.getElementById('uppercase');
    const lowercaseCheck = document.getElementById('lowercase');
    const numbersCheck = document.getElementById('numbers');
    const specialCheck = document.getElementById('special');
    const excludeSimilarCheck = document.getElementById('exclude-similar');
    const excludeAmbiguousCheck = document.getElementById('exclude-ambiguous');
    const generateBtn = document.getElementById('generate-btn');
    const regenerateBtn = document.getElementById('regenerate-btn');
    const copyBtn = document.getElementById('copy-btn');
    const favoriteBtn = document.getElementById('favorite-btn');
    const feedbackMessage = document.getElementById('feedback-message');
    const strengthFill = document.getElementById('strength-fill');
    const strengthText = document.getElementById('strength-text');
    const timeEstimate = document.getElementById('time-estimate');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const patternButtons = document.querySelectorAll('.pattern-btn');
    const themeToggle = document.getElementById('theme-toggle-icon');
    const savedList = document.getElementById('saved-list');
    const tutorialModal = document.getElementById('tutorial-modal');
    const showTutorialBtn = document.getElementById('show-tutorial');
    const closeTutorialBtn = document.getElementById('tutorial-close');
    const closeModalBtn = document.querySelector('.close-modal');
    const dontShowTutorialCheck = document.getElementById('dont-show-tutorial');
    
    // Estado inicial
    let currentPassword = '';
    let savedPasswords = [];
    let darkMode = localStorage.getItem('darkMode') === 'true';
    
    // Inicialização
    loadSavedPasswords();
    initTheme();
    showInitialTutorial();
    generatePassword();
    
    // Event Listeners
    lengthSlider.addEventListener('input', updateLengthDisplay);
    generateBtn.addEventListener('click', generatePassword);
    regenerateBtn.addEventListener('click', generatePassword);
    copyBtn.addEventListener('click', copyPassword);
    favoriteBtn.addEventListener('click', savePassword);
    
    // Abas
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tab = button.dataset.tab;
            changeTab(tab);
        });
    });
    
    // Padrões de senha
    patternButtons.forEach(button => {
        button.addEventListener('click', () => {
            applyPasswordPattern(button.dataset.pattern);
        });
    });
    
    // Tema
    themeToggle.addEventListener('click', toggleTheme);
    
    // Tutorial
    showTutorialBtn.addEventListener('click', (e) => {
        e.preventDefault();
        showTutorial();
    });
    
    closeTutorialBtn.addEventListener('click', hideTutorial);
    closeModalBtn.addEventListener('click', hideTutorial);
    
    // Checagem de opções para prevenir que todas estejam desmarcadas
    [uppercaseCheck, lowercaseCheck, numbersCheck, specialCheck].forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const anyChecked = [uppercaseCheck, lowercaseCheck, numbersCheck, specialCheck]
                               .some(cb => cb.checked);
            
            if (!anyChecked) {
                checkbox.checked = true;
                showFeedback('Selecione pelo menos um tipo de caractere', 'error');
            }
            
            // Gerar nova senha ao mudar opções
            generatePassword();
        });
    });
    
    // Gerar nova senha ao mudar opções de exclusão
    [excludeSimilarCheck, excludeAmbiguousCheck].forEach(checkbox => {
        checkbox.addEventListener('change', generatePassword);
    });
    
    // Gerar nova senha ao mudar comprimento
    lengthSlider.addEventListener('change', generatePassword);
    
    // Atalhos de teclado
    document.addEventListener('keydown', (e) => {
        // Alt+G para gerar nova senha
        if (e.altKey && e.key === 'g') {
            e.preventDefault();
            generatePassword();
        }
        
        // Alt+C para copiar a senha
        if (e.altKey && e.key === 'c') {
            e.preventDefault();
            copyPassword();
        }
        
        // Alt+S para salvar a senha
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            savePassword();
        }
        
        // Escape para fechar modal
        if (e.key === 'Escape' && tutorialModal.classList.contains('show')) {
            hideTutorial();
        }
    });
    
    // Fechar modal ao clicar fora
    tutorialModal.addEventListener('click', (e) => {
        if (e.target === tutorialModal) {
            hideTutorial();
        }
    });
    
    /**
     * Carrega senhas salvas do localStorage
     */
    function loadSavedPasswords() {
        const saved = localStorage.getItem('savedPasswords');
        if (saved) {
            try {
                savedPasswords = JSON.parse(saved);
                updateSavedPasswordsList();
            } catch (e) {
                console.error('Erro ao carregar senhas salvas:', e);
                savedPasswords = [];
            }
        }
    }
    
    /**
     * Atualiza a lista de senhas salvas na interface
     */
    function updateSavedPasswordsList() {
        if (savedPasswords.length === 0) {
            savedList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-folder-open"></i>
                    <p>Nenhuma senha salva ainda. Clique na estrela para salvar senhas.</p>
                </div>
            `;
            return;
        }
        
        savedList.innerHTML = '';
        savedPasswords.forEach((password, index) => {
            const item = document.createElement('div');
            item.className = 'saved-item';
            
            // Mascarar a senha para exibição
            const maskedPassword = password.length > 10 
                ? password.substring(0, 3) + '•'.repeat(password.length - 6) + password.substring(password.length - 3)
                : '•'.repeat(password.length);
            
            item.innerHTML = `
                <div class="saved-password">${maskedPassword}</div>
                <div class="saved-actions">
                    <button class="copy-saved" data-index="${index}" aria-label="Copiar senha salva">
                        <i class="fas fa-copy"></i>
                    </button>
                    <button class="show-saved" data-index="${index}" aria-label="Mostrar/ocultar senha">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="delete-saved" data-index="${index}" aria-label="Excluir senha salva">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            `;
            
            savedList.appendChild(item);
        });
        
        // Adicionar event listeners aos botões
        document.querySelectorAll('.copy-saved').forEach(btn => {
            btn.addEventListener('click', () => {
                const index = parseInt(btn.dataset.index);
                copySavedPassword(index);
            });
        });
        
        document.querySelectorAll('.show-saved').forEach(btn => {
            btn.addEventListener('click', () => {
                const index = parseInt(btn.dataset.index);
                togglePasswordVisibility(btn, index);
            });
        });
        
        document.querySelectorAll('.delete-saved').forEach(btn => {
            btn.addEventListener('click', () => {
                const index = parseInt(btn.dataset.index);
                deleteSavedPassword(index);
            });
        });
    }
    
    /**
     * Copia uma senha salva para a área de transferência
     */
    function copySavedPassword(index) {
        const password = savedPasswords[index];
        navigator.clipboard.writeText(password)
            .then(() => {
                showFeedback('Senha copiada para a área de transferência!', 'success');
                
                // Limpar a área de transferência após um tempo (para segurança)
                setTimeout(() => {
                    navigator.clipboard.writeText('').catch(() => {});
                }, 60000); // 1 minuto
            })
            .catch(() => {
                showFeedback('Erro ao copiar senha', 'error');
            });
    }
    
    /**
     * Alterna a visibilidade de uma senha salva
     */
    function togglePasswordVisibility(button, index) {
        const passwordElement = button.closest('.saved-item').querySelector('.saved-password');
        const isHidden = button.querySelector('i').classList.contains('fa-eye');
        
        if (isHidden) {
            passwordElement.textContent = savedPasswords[index];
            button.querySelector('i').classList.replace('fa-eye', 'fa-eye-slash');
            
            // Ocultar depois de 5 segundos
            setTimeout(() => {
                const btn = document.querySelector(`.show-saved[data-index="${index}"]`);
                if (btn && btn.querySelector('i').classList.contains('fa-eye-slash')) {
                    const item = btn.closest('.saved-item');
                    if (item) {
                        const passwordEl = item.querySelector('.saved-password');
                        const pass = savedPasswords[index];
                        const maskedPassword = pass.length > 10 
                            ? pass.substring(0, 3) + '•'.repeat(pass.length - 6) + pass.substring(pass.length - 3)
                            : '•'.repeat(pass.length);
                            
                        passwordEl.textContent = maskedPassword;
                        btn.querySelector('i').classList.replace('fa-eye-slash', 'fa-eye');
                    }
                }
            }, 5000);
        } else {
            const pass = savedPasswords[index];
            const maskedPassword = pass.length > 10 
                ? pass.substring(0, 3) + '•'.repeat(pass.length - 6) + pass.substring(pass.length - 3)
                : '•'.repeat(pass.length);
                
            passwordElement.textContent = maskedPassword;
            button.querySelector('i').classList.replace('fa-eye-slash', 'fa-eye');
        }
    }
    
    /**
     * Exclui uma senha salva
     */
    function deleteSavedPassword(index) {
        savedPasswords.splice(index, 1);
        localStorage.setItem('savedPasswords', JSON.stringify(savedPasswords));
        updateSavedPasswordsList();
        showFeedback('Senha excluída com sucesso', 'success');
    }
    
    /**
     * Salva a senha atual
     */
    function savePassword() {
        if (!currentPassword) {
            showFeedback('Nenhuma senha para salvar', 'error');
            return;
        }
        
        if (savedPasswords.includes(currentPassword)) {
            showFeedback('Esta senha já está salva', 'warning');
            return;
        }
        
        savedPasswords.push(currentPassword);
        localStorage.setItem('savedPasswords', JSON.stringify(savedPasswords));
        updateSavedPasswordsList();
        
        // Feedback visual
        favoriteBtn.querySelector('i').classList.remove('far');
        favoriteBtn.querySelector('i').classList.add('fas');
        
        showFeedback('Senha salva com sucesso!', 'success');
        
        // Mostrar aba de senhas salvas
        changeTab('saved');
    }
    
    /**
     * Alterna entre temas claro e escuro
     */
    function toggleTheme() {
        darkMode = !darkMode;
        localStorage.setItem('darkMode', darkMode);
        document.body.classList.toggle('dark-theme', darkMode);
        
        themeToggle.className = darkMode ? 'fas fa-sun' : 'fas fa-moon';
    }
    
    /**
     * Inicializa o tema com base na preferência salva
     */
    function initTheme() {
        document.body.classList.toggle('dark-theme', darkMode);
        themeToggle.className = darkMode ? 'fas fa-sun' : 'fas fa-moon';
    }
    
    /**
     * Exibe o tutorial inicial se for a primeira visita
     */
    function showInitialTutorial() {
        if (localStorage.getItem('tutorialShown') !== 'true') {
            showTutorial();
        }
    }
    
    /**
     * Exibe o tutorial
     */
    function showTutorial() {
        tutorialModal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
    
    /**
     * Oculta o tutorial
     */
    function hideTutorial() {
        tutorialModal.classList.remove('show');
        document.body.style.overflow = '';
        
        if (dontShowTutorialCheck.checked) {
            localStorage.setItem('tutorialShown', 'true');
        }
    }
    
    /**
     * Alterna entre as abas
     */
    function changeTab(tabId) {
        // Desativar todas as abas
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabPanes.forEach(pane => pane.classList.remove('active'));
        
        // Ativar a aba selecionada
        document.querySelector(`.tab-btn[data-tab="${tabId}"]`).classList.add('active');
        document.getElementById(tabId).classList.add('active');
    }
    
    /**
     * Aplica um padrão predefinido de senha
     */
    function applyPasswordPattern(pattern) {
        // Resetar todos os botões de padrão
        patternButtons.forEach(btn => btn.classList.remove('active'));
        
        // Ativar o botão selecionado
        document.querySelector(`.pattern-btn[data-pattern="${pattern}"]`).classList.add('active');
        
        // Aplicar configurações com base no padrão
        switch(pattern) {
            case 'easy-to-say':
                uppercaseCheck.checked = true;
                lowercaseCheck.checked = true;
                numbersCheck.checked = false;
                specialCheck.checked = false;
                excludeSimilarCheck.checked = true;
                excludeAmbiguousCheck.checked = true;
                break;
                
            case 'easy-to-read':
                uppercaseCheck.checked = true;
                lowercaseCheck.checked = true;
                numbersCheck.checked = true;
                specialCheck.checked = false;
                excludeSimilarCheck.checked = true;
                excludeAmbiguousCheck.checked = true;
                break;
                
            case 'all-chars':
                uppercaseCheck.checked = true;
                lowercaseCheck.checked = true;
                numbersCheck.checked = true;
                specialCheck.checked = true;
                excludeSimilarCheck.checked = false;
                excludeAmbiguousCheck.checked = false;
                break;
                
            case 'pin':
                uppercaseCheck.checked = false;
                lowercaseCheck.checked = false;
                numbersCheck.checked = true;
                specialCheck.checked = false;
                excludeSimilarCheck.checked = false;
                excludeAmbiguousCheck.checked = false;
                lengthSlider.value = 8;
                updateLengthDisplay();
                break;
                
            case 'passphrase':
                lengthSlider.value = 32;
                uppercaseCheck.checked = true;
                lowercaseCheck.checked = true;
                numbersCheck.checked = true;
                specialCheck.checked = true;
                excludeSimilarCheck.checked = false;
                excludeAmbiguousCheck.checked = false;
                updateLengthDisplay();
                break;
        }
        
        // Gerar nova senha com as configurações aplicadas
        generatePassword();
    }
    
    /**
     * Atualiza o display do comprimento da senha
     */
    function updateLengthDisplay() {
        const length = lengthSlider.value;
        lengthDisplay.textContent = length;
        lengthSlider.setAttribute('aria-valuenow', length);
        lengthSlider.setAttribute('aria-valuetext', `${length} caracteres`);
    }
    
    /**
     * Gera uma nova senha com base nas opções selecionadas
     */
    function generatePassword() {
        // Validar as opções
        const options = {
            length: parseInt(lengthSlider.value, 10),
            uppercase: uppercaseCheck.checked,
            lowercase: lowercaseCheck.checked,
            numbers: numbersCheck.checked,
            special: specialCheck.checked,
            excludeSimilar: excludeSimilarCheck.checked,
            excludeAmbiguous: excludeAmbiguousCheck.checked
        };
        
        if (!validateOptions(options)) {
            return;
        }
        
        // Reset do botão de favoritos
        favoriteBtn.querySelector('i').classList.remove('fas');
        favoriteBtn.querySelector('i').classList.add('far');
        
        // Fazer a requisição para a API
        fetch('/generate-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Token CSRF poderia ser adicionado aqui
            },
            body: JSON.stringify(options)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Erro ao gerar senha');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.password) {
                currentPassword = data.password;
                displayPassword(currentPassword);
                
                // Limpar qualquer mensagem de erro anterior
                clearFeedback();
                
                // Anúncio para leitores de tela que uma nova senha foi gerada
                passwordDisplay.setAttribute('aria-label', 'Nova senha gerada');
                
                // Analisar e mostrar a força da senha
                analyzePasswordStrength(currentPassword);
                
                // Estimar o tempo para quebrar
                estimateCrackingTime(currentPassword);
            }
        })
        .catch(error => {
            showFeedback(error.message, 'error');
            console.error('Erro:', error);
        });
    }
    
    /**
     * Analisa a força da senha e atualiza o indicador visual
     */
    function analyzePasswordStrength(password) {
        let score = 0;
        const length = password.length;
        
        // Pontuação por comprimento
        if (length >= 8) score += 1;
        if (length >= 12) score += 1;
        if (length >= 16) score += 1;
        if (length >= 24) score += 1;
        if (length >= 32) score += 1;
        
        // Pontuação por tipos de caracteres
        if (/[A-Z]/.test(password)) score += 1;
        if (/[a-z]/.test(password)) score += 1;
        if (/[0-9]/.test(password)) score += 1;
        if (/[^A-Za-z0-9]/.test(password)) score += 1;
        
        // Pontuação por distribuição de caracteres
        const entropy = calculateEntropy(password);
        if (entropy > 60) score += 1;
        if (entropy > 80) score += 2;
        if (entropy > 100) score += 2;
        
        // Escala de 0 a 100
        const strengthPercent = Math.min(100, Math.round((score / 15) * 100));
        
        // Atualizar o indicador visual
        strengthFill.style.width = `${strengthPercent}%`;
        
        // Exibir texto descritivo da força
        let strengthLabel = '';
        if (strengthPercent < 20) {
            strengthLabel = 'Muito fraca';
        } else if (strengthPercent < 40) {
            strengthLabel = 'Fraca';
        } else if (strengthPercent < 60) {
            strengthLabel = 'Razoável';
        } else if (strengthPercent < 80) {
            strengthLabel = 'Forte';
        } else {
            strengthLabel = 'Muito forte';
        }
        
        strengthText.textContent = `Força da Senha: ${strengthLabel}`;
    }
    
    /**
     * Estima o tempo necessário para quebrar a senha por força bruta
     */
    function estimateCrackingTime(password) {
        const entropy = calculateEntropy(password);
        const possibleCombinations = Math.pow(2, entropy);
        
        // Assumindo 10 bilhões de tentativas por segundo (supercomputador)
        const secondsToBreak = possibleCombinations / (10 * Math.pow(10, 9));
        
        let timeString = '';
        
        if (secondsToBreak < 1) {
            timeString = 'Instantâneo';
        } else if (secondsToBreak < 60) {
            timeString = 'Menos de um minuto';
        } else if (secondsToBreak < 3600) {
            const minutes = Math.floor(secondsToBreak / 60);
            timeString = `${minutes} minuto${minutes !== 1 ? 's' : ''}`;
        } else if (secondsToBreak < 86400) {
            const hours = Math.floor(secondsToBreak / 3600);
            timeString = `${hours} hora${hours !== 1 ? 's' : ''}`;
        } else if (secondsToBreak < 31536000) {
            const days = Math.floor(secondsToBreak / 86400);
            timeString = `${days} dia${days !== 1 ? 's' : ''}`;
        } else if (secondsToBreak < 31536000 * 100) {
            const years = Math.floor(secondsToBreak / 31536000);
            timeString = `${years} ano${years !== 1 ? 's' : ''}`;
        } else if (secondsToBreak < 31536000 * 1000) {
            timeString = 'Centenas de anos';
        } else if (secondsToBreak < 31536000 * 1000000) {
            timeString = 'Milhares de anos';
        } else if (secondsToBreak < 31536000 * 1000000000) {
            timeString = 'Milhões de anos';
        } else {
            timeString = 'Bilhões de anos';
        }
        
        const securityLevel = secondsToBreak > 31536000 ? 'Segura' : 'Vulnerável';
        const timeValue = document.querySelector('.time-value');
        timeValue.textContent = timeString;
        timeValue.style.color = secondsToBreak > 31536000 ? 'var(--success-color)' : 'var(--warning-color)';
    }
    
    /**
     * Valida as opções selecionadas pelo usuário
     */
    function validateOptions(options) {
        // Verificar se pelo menos uma opção está selecionada
        if (!options.uppercase && !options.lowercase && !options.numbers && !options.special) {
            showFeedback('Selecione pelo menos um tipo de caractere', 'error');
            return false;
        }
        
        // Verificar se o comprimento está dentro dos limites permitidos
        if (options.length < 8 || options.length > 64) {
            showFeedback('Comprimento deve estar entre 8 e 64 caracteres', 'error');
            return false;
        }
        
        return true;
    }
    
    /**
     * Exibe a senha na interface
     */
    function displayPassword(password) {
        // Sanitizar a senha antes de exibi-la (proteger contra XSS)
        passwordDisplay.value = sanitizeInput(password);
    }
    
    /**
     * Sanitiza entradas para prevenir XSS
     */
    function sanitizeInput(input) {
        // Converter caracteres especiais em entidades HTML
        const div = document.createElement('div');
        div.textContent = input;
        return div.textContent;
    }
    
    /**
     * Copia a senha para a área de transferência
     */
    function copyPassword() {
        if (!currentPassword) {
            showFeedback('Nenhuma senha para copiar', 'error');
            return;
        }
        
        // Usar a moderna Clipboard API com fallback para o método mais antigo
        if (navigator.clipboard) {
            navigator.clipboard.writeText(currentPassword)
                .then(() => {
                    handleSuccessfulCopy();
                    
                    // Limpar a área de transferência após um tempo (para segurança)
                    setTimeout(() => {
                        navigator.clipboard.writeText('').catch(() => {});
                    }, 60000); // 1 minuto
                })
                .catch(() => {
                    fallbackCopyMethod();
                });
        } else {
            fallbackCopyMethod();
        }
    }
    
    /**
     * Método alternativo para copiar texto em navegadores mais antigos
     */
    function fallbackCopyMethod() {
        passwordDisplay.select();
        
        try {
            const successful = document.execCommand('copy');
            if (successful) {
                handleSuccessfulCopy();
            } else {
                showFeedback('Não foi possível copiar. Por favor, copie manualmente (Ctrl+C/Cmd+C)', 'error');
            }
        } catch (err) {
            showFeedback('Não foi possível copiar. Por favor, copie manualmente (Ctrl+C/Cmd+C)', 'error');
        }
        
        // Desselecionar o texto
        window.getSelection().removeAllRanges();
    }
    
    /**
     * Trata a cópia bem-sucedida
     */
    function handleSuccessfulCopy() {
        // Feedback visual
        copyBtn.querySelector('i').className = 'fas fa-check';
        
        showFeedback('Senha copiada para a área de transferência!', 'success');
        
        // Restaurar o botão após 2 segundos
        setTimeout(() => {
            copyBtn.querySelector('i').className = 'fas fa-copy';
        }, 2000);
    }
    
    /**
     * Exibe mensagens de feedback para o usuário
     */
    function showFeedback(message, type) {
        feedbackMessage.textContent = message;
        feedbackMessage.className = 'feedback-message';
        feedbackMessage.classList.add(type);
        feedbackMessage.classList.add('show');
        
        // Limpar a mensagem após 3 segundos
        setTimeout(clearFeedback, 3000);
    }
    
    /**
     * Limpa as mensagens de feedback
     */
    function clearFeedback() {
        feedbackMessage.textContent = '';
        feedbackMessage.className = 'feedback-message';
    }
    
    /**
     * Calcula a entropia da senha (medida de aleatoriedade)
     */
    function calculateEntropy(password) {
        // Se a senha estiver vazia, a entropia é zero
        if (!password || password.length === 0) return 0;
        
        // Determinar o conjunto de caracteres usado
        let charsetSize = 0;
        
        if (password.match(/[a-z]/)) charsetSize += 26;
        if (password.match(/[A-Z]/)) charsetSize += 26;
        if (password.match(/[0-9]/)) charsetSize += 10;
        if (password.match(/[^a-zA-Z0-9]/)) charsetSize += 33; // caracteres especiais comuns
        
        // Se não foi possível determinar o charset, use um valor padrão
        if (charsetSize === 0) charsetSize = 26;
        
        // Fórmula da entropia: log2(charsetSize^length)
        return Math.log2(Math.pow(charsetSize, password.length));
    }
});
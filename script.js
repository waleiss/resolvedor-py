let premiseCount = 1;
let solutionStepCount = 0;
let currentModal = null; // Para controlar qual modal está aberto

function showScreen(screen) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screen + '-screen').classList.add('active');
    
    // Atualizar botões de navegação
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    
    // Marcar como ativo o botão correspondente à tela atual
    if (screen === 'solution') {
        // Copiar premissas e conclusão para a tela de solução
        copyPremisesToSolution();
        copyConclusionToSolution();
        
        document.querySelectorAll('.nav-btn').forEach(btn => {
            if (btn.textContent.includes('Solução')) {
                btn.classList.add('active');
            }
        });
    } else if (screen === 'premises') {
        document.querySelectorAll('.nav-btn').forEach(btn => {
            if (btn.textContent.includes('Premissas')) {
                btn.classList.add('active');
            }
        });
    }
}

function copyPremisesToSolution() {
    const premisesList = document.getElementById('premises-list');
    const solutionPremisesList = document.getElementById('solution-premises-list');
    
    // Limpar lista de premissas na solução
    solutionPremisesList.innerHTML = '';
    
    // Copiar todas as premissas
    const premiseItems = premisesList.querySelectorAll('.premise-item');
    premiseItems.forEach(item => {
        const label = item.querySelector('.premise-label').textContent;
        const value = item.querySelector('.editable-premise').value;
        
        const newPremise = document.createElement('div');
        newPremise.className = 'premise-item';
        newPremise.innerHTML = `
            <span class="premise-label">${label}</span>
            <input type="text" class="editable-premise" value="${value}" placeholder="Digite a premissa ${label}">
        `;
        solutionPremisesList.appendChild(newPremise);
    });
}

function copyConclusionToSolution() {
    const conclusionInput = document.getElementById('conclusion-input');
    const solutionConclusionInput = document.getElementById('solution-conclusion-input');
    
    solutionConclusionInput.value = conclusionInput.value;
}

function addPremise() {
    currentModal = 'premise';
    document.getElementById('premise-modal').classList.add('active');
    document.getElementById('premise-input').focus();
}

function addPremiseInSolution() {
    currentModal = 'premise-solution';
    document.getElementById('premise-modal').classList.add('active');
    document.getElementById('premise-input').focus();
}

function closePremiseModal() {
    document.getElementById('premise-modal').classList.remove('active');
    document.getElementById('premise-input').value = '';
    currentModal = null;
}

function savePremise() {
    const formula = document.getElementById('premise-input').value.trim();
    if (formula) {
        premiseCount++;
        const newPremise = document.createElement('div');
        newPremise.className = 'premise-item';
        newPremise.innerHTML = `
            <span class="premise-label">P${premiseCount}:</span>
            <input type="text" class="editable-premise" value="${formula}" placeholder="Digite a premissa P${premiseCount}">
        `;
        
        if (currentModal === 'premise-solution') {
            // Adicionar na tela de solução
            const solutionPremisesList = document.getElementById('solution-premises-list');
            solutionPremisesList.appendChild(newPremise);
        } else {
            // Adicionar na tela de premissas
            const premisesList = document.getElementById('premises-list');
            premisesList.appendChild(newPremise);
        }
        
        closePremiseModal();
    }
}

function addSolutionStep() {
    document.getElementById('step-modal').classList.add('active');
    document.getElementById('step-formula-input').focus();
}

function closeStepModal() {
    document.getElementById('step-modal').classList.remove('active');
    document.getElementById('step-formula-input').value = '';
    document.getElementById('step-method-input').value = '';
    document.getElementById('step-premises-input').value = '';
}

function saveSolutionStep() {
    const formula = document.getElementById('step-formula-input').value.trim();
    const method = document.getElementById('step-method-input').value.trim();
    const premises = document.getElementById('step-premises-input').value.trim();
    
    if (formula && method && premises) {
        solutionStepCount++;
        const stepsList = document.getElementById('student-solution');
        const newStep = document.createElement('div');
        newStep.className = 'solution-item';
        newStep.innerHTML = `
            <div class="step-info">
                <span class="premise-label">S${solutionStepCount}:</span>
                <input type="text" class="editable-step step-formula" value="${formula}" placeholder="Fórmula">
                <input type="text" class="editable-step step-method" value="${method}" placeholder="Método">
                <input type="text" class="editable-step step-premises" value="${premises}" placeholder="Premissas">
            </div>
        `;
        stepsList.appendChild(newStep);
        closeStepModal();
    }
}

async function solveProblem() {
    showModal();
    
    try {
        // Coletar dados das premissas e conclusão
        const premises = [];
        document.querySelectorAll('#premises-list .editable-premise').forEach(el => {
            if (el.value.trim()) {
                premises.push(el.value.trim());
            }
        });
        
        const conclusion = document.getElementById('conclusion-input').value.trim();
        
        const data = {
            sentences: premises,
            conclusion: conclusion
        };
        
        // Simular chamada da API - substitua pela sua API real
        const response = await fetch('http://127.0.0.1:5000/solvejson', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            showAPIResponse(result.log.join('\n'));
            // Ir para tela de solução após um tempo
            setTimeout(() => {
                closeModal();
                showScreen('solution');
            }, 100000);
        } else {
            showAPIResponse(`Erro: ${result.error}`);
        }
    } catch (error) {
        showAPIResponse(`Erro: ${error.message}`);
    }
}

async function evaluateSolution() {
    showModal();
    
    try {
        // Coletar dados das premissas da tela de solução
        const premises = [];
        document.querySelectorAll('#solution-premises-list .editable-premise').forEach(el => {
            if (el.value.trim()) {
                premises.push(el.value.trim());
            }
        });
        
        // Coletar conclusão da tela de solução
        const conclusion = document.getElementById('solution-conclusion-input').value.trim();
        
        // Coletar dados da solução do aluno
        const inferences = [];
        document.querySelectorAll('#student-solution .solution-item').forEach(item => {
            const formula = item.querySelector('.step-formula').value.trim();
            const method = item.querySelector('.step-method').value.trim();
            const stepPremises = item.querySelector('.step-premises').value.trim();
            
            if (formula && method && stepPremises) {
                inferences.push(`${formula}  ${method}  ${stepPremises}`);
            }
        });
        
        const data = {
            premises: premises,
            conclusion: conclusion,
            inferences: inferences
        };
        
        // Chamada da API para avaliar
        const response = await fetch('http://127.0.0.1:5000/evaluatejson', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            let responseText = result.log.join('\n');
            if (result.feedback) {
                responseText += '\n\nFeedback:\n' + result.feedback;
            }
            showAPIResponse(responseText);
        } else {
            showAPIResponse(`Erro: ${result.error}`);
        }
    } catch (error) {
        showAPIResponse(`Erro: ${error.message}`);
    }
}

function showModal() {
    document.getElementById('api-modal').classList.add('active');
    document.getElementById('modal-body').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Processando...</p>
        </div>
    `;
}

function closeModal() {
    document.getElementById('api-modal').classList.remove('active');
}

function showAPIResponse(response) {
    document.getElementById('modal-body').innerHTML = `
        <div class="api-response">${response}</div>
    `;
}

// Fechar modais ao clicar fora
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.classList.remove('active');
            if (modal.id === 'premise-modal') {
                currentModal = null;
            }
        }
    });
}

// Permitir Enter para adicionar premissa e passos
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('premise-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            savePremise();
        }
    });
    
    document.getElementById('step-premises-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            saveSolutionStep();
        }
    });
});

// Variável para controlar o input ativo
let activeInput = null;

// Função para fazer o teclado lógico funcionar com qualquer input
function typeKey(operator) {
    // Se não há input ativo, tenta encontrar um input focado
    if (!activeInput) {
        activeInput = document.activeElement;
        // Verifica se o elemento focado é um input de texto
        if (!activeInput || activeInput.tagName !== 'INPUT' || activeInput.type !== 'text') {
            // Se não há input focado, não faz nada
            return;
        }
    }
    
    const cursorPos = activeInput.selectionStart;
    const textBefore = activeInput.value.substring(0, cursorPos);
    const textAfter = activeInput.value.substring(cursorPos);

    activeInput.value = textBefore + operator + textAfter;
    activeInput.focus();
    activeInput.setSelectionRange(cursorPos + operator.length, cursorPos + operator.length);
}

// Função para alternar minimizar/maximizar o teclado
function toggleKeyboard() {
    const keyboard = document.getElementById('logicalKeyboard');
    const toggleBtn = document.getElementById('toggleKeyboard');
    
    keyboard.classList.toggle('minimized');
    
    if (keyboard.classList.contains('minimized')) {
        toggleBtn.textContent = '+';
    } else {
        toggleBtn.textContent = '−';
    }
}

// Adiciona Event Listeners para rastrear input ativo
document.addEventListener('DOMContentLoaded', function() {
    // Rastreia quando um input recebe foco
    document.addEventListener('focusin', function(e) {
        if (e.target.tagName === 'INPUT' && e.target.type === 'text') {
            activeInput = e.target;
        }
    });
    
    // Limpa o input ativo quando perde o foco (opcional)
    document.addEventListener('focusout', function(e) {
        // Mantém o último input ativo para facilitar o uso
        // activeInput = null;
    });
    
    // Event Listeners para os botões do teclado lógico
    document.getElementById("btnAnd").addEventListener("click", () => typeKey("∧"));
    document.getElementById("btnOr").addEventListener("click", () => typeKey("∨"));
    document.getElementById("btnNot").addEventListener("click", () => typeKey("¬"));
    document.getElementById("btnImplies").addEventListener("click", () => typeKey("→"));
    document.getElementById("btnEquiv").addEventListener("click", () => typeKey("↔"));
    document.getElementById("btnOpenParen").addEventListener("click", () => typeKey("("));
    document.getElementById("btnCloseParen").addEventListener("click", () => typeKey(")"));
    
    // Event Listener para o botão de toggle
    document.getElementById("toggleKeyboard").addEventListener("click", toggleKeyboard);

    // Outros event listeners existentes
    document.getElementById('premise-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            savePremise();
        }
    });
    
    document.getElementById('step-premises-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            saveSolutionStep();
        }
    });
});
<script lang="ts">
import { onMount } from 'svelte';

const logicalSymbols = [
  { symbol: '¬', label: 'NOT', description: 'Negação (Ctrl+Alt+1)', color: 'btn-primary', shortcut: '1' },
  { symbol: '∧', label: 'AND', description: 'Conjunção (Ctrl+Alt+2)', color: 'btn-primary', shortcut: '2' },
  { symbol: '∨', label: 'OR', description: 'Disjunção (Ctrl+Alt+3)', color: 'btn-primary', shortcut: '3' },
  { symbol: '→', label: 'IMP', description: 'Implicação (Ctrl+Alt+4)', color: 'btn-secondary', shortcut: '4' },
  { symbol: '↔', label: 'BIIMP', description: 'Bi-implicação (Ctrl+Alt+5)', color: 'btn-secondary', shortcut: '5' },
  { symbol: '(', label: '(', description: 'Parêntese esquerdo', color: 'btn-secondary', shortcut: null },
  { symbol: ')', label: ')', description: 'Parêntese direito', color: 'btn-secondary', shortcut: null },
];

let lastActiveInput: HTMLInputElement | HTMLTextAreaElement | null = null;
let isVisible = $state(true);
let lastInsertedSymbol = $state<string | null>(null);
let showWarning = $state(false);

function insertSymbol(symbol: string, fromKeyboard: boolean = false) {
  // Try to use the last focused input or the current active element
  const activeElement = (lastActiveInput || document.activeElement) as HTMLInputElement | HTMLTextAreaElement;
  
  if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA')) {
    const start = activeElement.selectionStart ?? 0;
    const end = activeElement.selectionEnd ?? 0;
    const currentValue = activeElement.value;
    
    // Create new value with symbol inserted
    const newValue = currentValue.slice(0, start) + symbol + currentValue.slice(end);
    
    // Update the value
    activeElement.value = newValue;
    
    // Dispatch multiple events to ensure Svelte updates
    activeElement.dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));
    activeElement.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
    activeElement.dispatchEvent(new InputEvent('input', { 
      bubbles: true, 
      cancelable: true,
      data: symbol 
    }));
    
    // Set cursor position after the inserted symbol
    const newPosition = start + symbol.length;
    setTimeout(() => {
      activeElement.setSelectionRange(newPosition, newPosition);
      activeElement.focus();
    }, 0);
    
    // Visual feedback
    if (!fromKeyboard) {
      lastInsertedSymbol = symbol;
      setTimeout(() => {
        lastInsertedSymbol = null;
      }, 300);
    }
  } else {
    // Show a visual warning
    showWarning = true;
    setTimeout(() => {
      showWarning = false;
    }, 3000);
  }
}

// Track focused inputs and keyboard shortcuts
onMount(() => {
  const handleFocus = (e: FocusEvent) => {
    const target = e.target as HTMLElement;
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
      lastActiveInput = target as HTMLInputElement | HTMLTextAreaElement;
    }
  };
  
  const handleKeyboard = (e: KeyboardEvent) => {
    // Ctrl+Alt+Number shortcuts
    if (e.ctrlKey && e.altKey) {
      const symbol = logicalSymbols.find(s => s.shortcut === e.key);
      if (symbol) {
        e.preventDefault();
        insertSymbol(symbol.symbol, true);
      }
    }
    
    // Toggle visibility with Ctrl+Alt+K
    if (e.ctrlKey && e.altKey && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      toggleVisibility();
    }
  };
  
  document.addEventListener('focusin', handleFocus);
  document.addEventListener('keydown', handleKeyboard);
  
  return () => {
    document.removeEventListener('focusin', handleFocus);
    document.removeEventListener('keydown', handleKeyboard);
  };
});

function toggleVisibility() {
  isVisible = !isVisible;
}
</script>

<div class="fixed bottom-4 left-1/2 -translate-x-1/2 z-50">
  <!-- Warning Toast -->
  {#if showWarning}
    <div class="toast toast-top toast-center mb-4 animate-bounce">
      <div class="alert alert-warning shadow-lg">
        <span class="material-symbols-outlined">warning</span>
        <span>Clique em um campo de entrada primeiro!</span>
      </div>
    </div>
  {/if}
  
  <div class="card bg-base-300 shadow-2xl border border-primary/20 transition-transform duration-300"
       class:translate-y-0={!isVisible}>
    <div class="card-body p-3">
      <!-- Header with toggle -->
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs font-semibold text-primary flex items-center gap-2">
          <span class="material-symbols-outlined text-sm">keyboard</span>
          Símbolos Lógicos
        </span>
        <button
          class="btn btn-ghost btn-xs"
          onclick={toggleVisibility}
          type="button"
          title={isVisible ? 'Ocultar teclado' : 'Mostrar teclado'}
        >
          <span class="material-symbols-outlined text-base">
            {isVisible ? 'keyboard_hide' : 'keyboard'}
          </span>
        </button>
      </div>
      
      <!-- Keyboard buttons -->
      {#if isVisible}
        <div class="flex gap-2 items-center justify-center flex-wrap">
          {#each logicalSymbols as { symbol, label, description, color, shortcut }}
            <div class="tooltip tooltip-top" data-tip={description}>
              <button
                class="btn btn-sm {color} hover:scale-110 transition-all relative"
                class:ring-2={lastInsertedSymbol === symbol}
                class:ring-primary={lastInsertedSymbol === symbol}
                class:ring-offset-2={lastInsertedSymbol === symbol}
                class:ring-offset-base-300={lastInsertedSymbol === symbol}
                onclick={() => insertSymbol(symbol, false)}
                type="button"
              >
                <span class="text-xl font-bold">{symbol}</span>
                <span class="text-[10px] opacity-70 ml-1">{label}</span>
              </button>
            </div>
          {/each}
        </div>
        
        <!-- Helper text -->
        <div class="text-[10px] text-center text-base-content/50 mt-2 space-y-1">
          <div>Atalhos: <kbd class="kbd kbd-xs">Ctrl</kbd>+<kbd class="kbd kbd-xs">Alt</kbd>+<kbd class="kbd kbd-xs">1-5</kbd> | Toggle: <kbd class="kbd kbd-xs">Ctrl</kbd>+<kbd class="kbd kbd-xs">Alt</kbd>+<kbd class="kbd kbd-xs">K</kbd></div>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  .tooltip:before,
  .tooltip:after {
    bottom: 100%;
    margin-bottom: 0.5rem;
  }
  
  /* Animation for button press */
  .btn:active {
    transform: scale(0.95);
  }

</style>


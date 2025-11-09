<script lang="ts">
import type { Argument } from '../types';
import { submitToPipeline1, submitToPipeline2 } from './api';
import { onMount } from 'svelte';

let sentences = $state<string[]>(['']);
let conclusion = $state<string>('');
let loading = $state<boolean>(false);
let error = $state<string | null>(null);
let result = $state<any>(null);
let sentenceInputs: HTMLInputElement[] = [];
let conclusionInput: HTMLInputElement | null = null;

function addSentence() {
  sentences = [...sentences, ''];
  // Focus the new input after it's added
  setTimeout(() => {
    const newIndex = sentences.length - 1;
    sentenceInputs[newIndex]?.focus();
  }, 50);
}

function removeSentence(index: number) {
  if (sentences.length > 1) {
    sentences = sentences.filter((_, i) => i !== index);
    // Focus the previous or next input
    setTimeout(() => {
      const focusIndex = Math.min(index, sentences.length - 1);
      sentenceInputs[focusIndex]?.focus();
    }, 50);
  }
}

// Handle input events to ensure state updates
function handleSentenceInput(index: number, event: Event) {
  const target = event.target as HTMLInputElement;
  sentences[index] = target.value;
}

function handleConclusionInput(event: Event) {
  const target = event.target as HTMLInputElement;
  conclusion = target.value;
}

async function handleSubmit(pipeline: 1 | 2) {
  error = null;
  result = null;
  
  // Filter out empty sentences
  const filteredSentences = sentences.filter(s => s.trim() !== '');
  
  if (filteredSentences.length === 0) {
    error = 'Adicione pelo menos uma sentença';
    return;
  }
  
  if (conclusion.trim() === '') {
    error = 'Adicione uma conclusão';
    return;
  }
  
  const argument: Argument = {
    sentences: filteredSentences,
    conclusion: conclusion.trim()
  };
  
  loading = true;
  
  try {
    if (pipeline === 1) {
      result = await submitToPipeline1(argument);
    } else {
      result = await submitToPipeline2(argument);
    }
  } catch (e: any) {
    error = e.message || 'Erro ao enviar o problema';
  } finally {
    loading = false;
  }
}
</script>

<div class="card bg-base-200 shadow-xl">
  <div class="card-body">
    <h3 class="card-title">Problema de Lógica</h3>
    
    <div class="form-control gap-3">
      <!-- Sentences -->
      <div>
        <div class="label">
          <span class="label-text">Sentenças (premissas)</span>
        </div>
        {#each sentences as sentence, index (index)}
          <div class="flex gap-2 mb-2">
            <div class="relative flex-1">
              <input
                bind:this={sentenceInputs[index]}
                type="text"
                class="input input-bordered w-full pr-10"
                placeholder="Digite uma sentença (ex: p → q)"
                value={sentence}
                oninput={(e) => handleSentenceInput(index, e)}
              />
              <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-base-content/40">
                {index + 1}
              </span>
            </div>
            {#if sentences.length > 1}
              <button
                class="btn btn-error btn-square"
                onclick={() => removeSentence(index)}
                type="button"
                title="Remover sentença"
              >
                <span class="material-symbols-outlined">close</span>
              </button>
            {/if}
          </div>
        {/each}
        
        <button
          class="btn btn-outline btn-primary btn-sm mt-2 mb-5"
          onclick={addSentence}
          type="button"
        >
          <span class="material-symbols-outlined">add</span> 
          Adicionar Sentença
        </button>
      </div>
      
      <!-- Conclusion -->
      <div class="form-control">
        <div class="label">
          <span class="label-text font-semibold">Conclusão:</span>
        </div>
        <div class="relative">
          <input
            bind:this={conclusionInput}
            type="text"
            class="input input-bordered w-full pr-10"
            placeholder="Digite a conclusão (ex: r)"
            value={conclusion}
            oninput={handleConclusionInput}
          />
          <span class="absolute right-3 top-1/2 -translate-y-1/2 text-lg text-primary">
            ∴
          </span>
        </div>
      </div>
      
      <!-- Error message -->
      {#if error}
        <div class="alert alert-error my-5">
          <span>{error}</span>
        </div>
      {/if}
      
      <!-- Result -->
      {#if result}
        <div class="alert alert-success">
          <span>Problema enviado com sucesso!</span>
        </div>
        <div class="mockup-code">
          <pre><code>{JSON.stringify(result, null, 2)}</code></pre>
        </div>
      {/if}
      
      <!-- Submit buttons -->
      <div class="card-actions justify-end gap-2 mt-4">
        <button
          class="btn btn-primary"
          onclick={() => handleSubmit(1)}
          disabled={loading}
        >
          {#if loading}
            <span class="loading loading-spinner"></span>
          {:else}
            <span class="material-symbols-outlined">send</span>
          {/if}
          Pipeline 1
        </button>
        <button
          class="btn btn-secondary"
          onclick={() => handleSubmit(2)}
          disabled={loading}
        >
          {#if loading}
            <span class="loading loading-spinner"></span>
          {:else}
            <span class="material-symbols-outlined">rocket_launch</span>
          {/if}
          Pipeline 2
        </button>
      </div>
    </div>
  </div>
</div>

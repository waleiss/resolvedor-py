<script lang="ts">
import { onMount } from 'svelte';
import type { Argument } from '../types'
import { submitToPipeline1, submitToPipeline2 } from './api'
import ResultsBox from './ResultsBox.svelte'

let sentences = $state<string[]>(['']);
let conclusion = $state<string>('');
let loading = $state<boolean>(false);
let error = $state<string | null>(null);
let result = $state<any>(null);
let lastPipeline = $state<number | null>(null);
let sentenceInputs: HTMLInputElement[] = [];
let conclusionInput: HTMLInputElement | null = null;

onMount(() => {
  // Extrai query params da hash
  const hash = window.location.hash;
  const queryString = hash.split('?')[1];
  
  if (queryString) {
    const params = new URLSearchParams(queryString);
    const prefillSentences = params.get('sentences');
    const prefillConclusion = params.get('conclusion');
    
    if (prefillSentences && prefillConclusion) {
      try {
        sentences = JSON.parse(prefillSentences);
        conclusion = prefillConclusion;
      } catch (e) {
        console.error('Erro ao fazer parse dos parâmetros:', e);
      }
    }
  }
});


function addSentence() {
  sentences = [...sentences, ''];
  setTimeout(() => {
    const newIndex = sentences.length - 1;
    sentenceInputs[newIndex]?.focus();
  }, 50);
}

function removeSentence(index: number) {
  if (sentences.length > 1) {
    sentences = sentences.filter((_, i) => i !== index);
    setTimeout(() => {
      const focusIndex = Math.min(index, sentences.length - 1);
      sentenceInputs[focusIndex]?.focus();
    }, 50);
  }
}

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
      lastPipeline = 1;
    } else {
      result = await submitToPipeline2(argument);
      lastPipeline = 2;
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
    <h3 class="card-title mb-2">Problema de Lógica</h3>
    
    <div class="form-control gap-3">
      <!-- Sentences -->
      <div>
        <div class="label">
          <span class="label-text font-semibold mb-2">Sentenças (premissas)</span>
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
          <span class="label-text font-semibold mb-2">Conclusão:</span>
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
            <div class="flex items-center gap-1">
              <span class="font-bold text-lg">W</span>
              <span class="material-symbols-outlined">arrow_right_alt</span>
              <span class="material-symbols-outlined">smart_toy</span>
            </div>
            <span class="mt-1">Pipeline 1</span>
          {/if}
        </button>
        <button
          class="btn btn-secondary"
          onclick={() => handleSubmit(2)}
          disabled={loading}
        >
          {#if loading}
            <span class="loading loading-spinner"></span>
          {:else}
            <div class="flex items-center gap-1">
              <span class="material-symbols-outlined">smart_toy</span>
              <span class="material-symbols-outlined">arrow_right_alt</span>
              <span class="font-bold text-lg">W</span>
            </div>
            <span class="mt-1">Pipeline 2</span>
          {/if}
        </button>
      </div>
    </div>
  </div>
</div>

<ResultsBox bind:result bind:lastPipeline />
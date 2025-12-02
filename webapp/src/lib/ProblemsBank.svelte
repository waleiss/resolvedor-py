<script lang="ts">
  import { onMount } from 'svelte';
  import { submitToPipeline1, submitToPipeline2, getProblems } from './api';
  import ResultsBox from './ResultsBox.svelte';
  import type { SavedProblem } from '../types';
  
  let problems: SavedProblem[] = [];
  let selectedProblem: SavedProblem | null = null;
  let modalResult: any = null;
  let modalLoading = false;
  let lastPipeline: 1 | 2 | null = null;
  let loading = false;
  let error = '';
  
  onMount(async () => {
    await loadProblems();
  });
  
  async function loadProblems() {
    loading = true;
    error = '';
    try {
      problems = await getProblems();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Erro ao carregar problemas';
    } finally {
      loading = false;
    }
  }
  
  function editProblem(problem: SavedProblem) {
    // Usando window.location para navegação no Svelte vanilla
    const params = new URLSearchParams({
      sentences: JSON.stringify(problem.sentences),
      conclusion: problem.conclusion
    });
    window.location.href = `/#/?${params.toString()}`;
  }
  
  async function quickRun(pipeline: 1 | 2) {
    if (!selectedProblem) return;
    
    modalLoading = true;
    lastPipeline = pipeline;
    modalResult = null; // Limpa resultado anterior
    
    try {
      const argument = {
        sentences: selectedProblem.sentences,
        conclusion: selectedProblem.conclusion
      };
      
      const result = pipeline === 1 
        ? await submitToPipeline1(argument)
        : await submitToPipeline2(argument);
      
      modalResult = result;
    } catch (e) {
      error = e instanceof Error ? e.message : 'Erro ao executar pipeline';
    } finally {
      modalLoading = false;
    }
  }
  
  function closeModal() {
    selectedProblem = null;
    modalResult = null;
    lastPipeline = null;
    error = '';
  }
  
  function getDifficultyColor(difficulty: string): string {
    const colors: Record<string, string> = {
      'easy': 'badge-success',
      'medium': 'badge-warning',
      'hard': 'badge-error'
    };
    return colors[difficulty.toLowerCase()] || 'badge-neutral';
  }
</script>

<div class="container mx-auto p-4">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold flex items-center gap-2">
      <span class="material-symbols-outlined text-4xl">library_books</span>
      Banco de Problemas
    </h1>
    <button class="btn btn-primary" onclick={loadProblems} disabled={loading}>
      {#if loading}
        <span class="loading loading-spinner loading-sm"></span>
      {:else}
        <span class="material-symbols-outlined">refresh</span>
      {/if}
      Atualizar
    </button>
  </div>

  {#if error && !selectedProblem}
    <div role="alert" class="alert alert-error mb-4">
      <span class="material-symbols-outlined">error</span>
      <span>{error}</span>
    </div>
  {/if}

  {#if loading && problems.length === 0}
    <div class="flex justify-center items-center py-12">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {:else if problems.length === 0}
    <div class="alert alert-info">
      <span class="material-symbols-outlined">info</span>
      <span>Nenhum problema cadastrado no banco de dados.</span>
    </div>
  {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each problems as problem}
        <div class="card bg-base-200 shadow-xl hover:shadow-2xl transition-shadow">
          <div class="card-body">
            <div class="flex justify-between items-start mb-2">
              <h3 class="card-title text-sm flex-1">{problem.description}</h3>
              <div class="badge {getDifficultyColor(problem.difficulty)} badge-sm">
                {problem.difficulty}
              </div>
            </div>
            
            <div class="text-xs space-y-2">
              <div>
                <p class="font-semibold mb-1">Premissas:</p>
                <ul class="list-disc list-inside ml-2">
                  {#each problem.sentences as s}
                    <li class="font-mono">{s}</li>
                  {/each}
                </ul>
              </div>
              <div>
                <p class="font-semibold">Conclusão:</p>
                <code class="ml-2">{problem.conclusion}</code>
              </div>
            </div>
            
            <div class="card-actions justify-end mt-3 gap-2">
              <button 
                class="btn btn-sm btn-outline"
                onclick={() => editProblem(problem)}
              >
                <span class="material-symbols-outlined text-sm">edit</span>
                Editar
              </button>
              <button 
                class="btn btn-sm btn-outline btn-primary"
                onclick={() => selectedProblem = problem}
              >
                <span class="material-symbols-outlined text-sm">play_arrow</span>
                Executar
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<!-- Modal de Execução Rápida -->
{#if selectedProblem}
  <dialog class="modal modal-open">
    <div class="modal-box max-w-7xl w-full">
      <form method="dialog">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onclick={closeModal}>✕</button>
      </form>
      
      <h3 class="text-2xl font-bold mb-4 flex items-center gap-2">
        <span class="material-symbols-outlined">terminal</span>
        Executar Problema
      </h3>
      
      <!-- Problema (read-only) -->
      <div class="mb-6 text-center">
        <div class="bg-base-300 p-4 rounded-lg">
          <p class="font-mono text-lg mb-3">{selectedProblem.description}</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
            <div>
              <p class="font-semibold mb-2">Premissas:</p>
              <ul class="list-disc list-inside ml-4">
                {#each selectedProblem.sentences as sentence}
                  <li class="font-mono text-sm">{sentence}</li>
                {/each}
              </ul>
            </div>
            <div>
              <p class="font-semibold mb-2">Conclusão:</p>
              <code class="ml-4 text-sm">{selectedProblem.conclusion}</code>
            </div>
          </div>
        </div>
      </div>
      
      {#if !modalResult}
        <!-- Botões de Pipeline -->
        <div class="flex gap-4 justify-center">
          <button 
            class="btn btn-primary btn-lg flex-col h-auto py-3"
            onclick={() => quickRun(1)}
            disabled={modalLoading}
          >
            {#if modalLoading && lastPipeline === 1}
              <span class="loading loading-spinner"></span>
            {:else}
              <div class="flex items-center gap-1">
                <span class="font-bold">W</span>
                <span class="material-symbols-outlined">arrow_right_alt</span>
                <span class="material-symbols-outlined">smart_toy</span>
              </div>
              <span class="text-xs mt-1">Pipeline 1</span>
            {/if}
          </button>
          <button 
            class="btn btn-secondary btn-lg flex-col h-auto py-3"
            onclick={() => quickRun(2)}
            disabled={modalLoading}
          >
            {#if modalLoading && lastPipeline === 2}
              <span class="loading loading-spinner"></span>
            {:else}
              <div class="flex items-center gap-1">
                <span class="material-symbols-outlined">smart_toy</span>
                <span class="material-symbols-outlined">arrow_right_alt</span>
                <span class="font-bold">W</span>
              </div>
              <span class="text-xs mt-1">Pipeline 2</span>
            {/if}
          </button>
        </div>
      {:else}
        <!-- Reutiliza o componente ResultsBox -->
        <ResultsBox bind:result={modalResult} bind:lastPipeline />
      {/if}
    </div>
    <form method="dialog" class="modal-backdrop" onclick={closeModal}>
      <button>close</button>
    </form>
  </dialog>
{/if}

<style>
  .material-symbols-outlined {
    font-variation-settings:
      'FILL' 0,
      'wght' 400,
      'GRAD' 0,
      'opsz' 24;
    vertical-align: middle;
  }
</style>
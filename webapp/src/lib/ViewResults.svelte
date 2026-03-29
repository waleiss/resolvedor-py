<script lang="ts">
  import { onMount } from 'svelte';
  import { getExperiments, getExperiment } from './api';
  import type { ExperimentListItem, Experiment } from '../types';

  let experiments: ExperimentListItem[] = [];
  let selectedExperiment: Experiment | null = null;
  let loading = false;
  let error = '';
  let modalOpen = false;

  onMount(async () => {
    await loadExperiments();
  });

  async function loadExperiments() {
    loading = true;
    error = '';
    try {
      experiments = await getExperiments();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Erro ao carregar experimentos';
    } finally {
      loading = false;
    }
  }

  async function openExperiment(filename: string) {
    loading = true;
    error = '';
    try {
      selectedExperiment = await getExperiment(filename);
      modalOpen = true;
    } catch (e) {
      error = e instanceof Error ? e.message : 'Erro ao carregar experimento';
    } finally {
      loading = false;
    }
  }

  function closeModal() {
    modalOpen = false;
    selectedExperiment = null;
  }

  function formatDate(timestamp: string): string {
    return new Date(timestamp).toLocaleString('pt-BR');
  }

  function getPipelineName(pipeline: string): string {
    if (pipeline === 'solver_to_llm') {
      return 'W → LLM';
    } else if (pipeline === 'llm_to_evaluator') {
      return 'LLM → W';
    }
    return pipeline;
  }

  function getSolverTitle(experiment: Experiment): string {
    return experiment.solver.type === 'llm' ? 'Solução do LLM' : 'Resolvedor Agente W';
  }

  function getEvaluatorTitle(experiment: Experiment): string {
    return experiment.evaluator.type === 'llm' ? 'Avaliação do LLM' : 'Avaliador Agente W';
  }

  function getSolverBoxClasses(experiment: Experiment): string {
    const isLLM = experiment.solver.type === 'llm';
    return `p-4 rounded-lg border-2 ${isLLM ? 'bg-secondary-content/10 border-secondary' : 'bg-primary-content/10 border-primary'}`;
  }

  function getEvaluatorBoxClasses(experiment: Experiment): string {
    const isLLM = experiment.evaluator.type === 'llm';
    return `p-4 rounded-lg border-2 ${isLLM ? 'bg-secondary-content/10 border-secondary' : 'bg-primary-content/10 border-primary'}`;
  }
</script>

<div class="container mx-auto p-4">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold">Experimentos Realizados</h1>
    <button class="btn btn-primary" onclick={loadExperiments} disabled={loading}>
      {#if loading}
        <span class="loading loading-spinner loading-sm"></span>
      {:else}
        <span class="material-symbols-outlined">refresh</span>
      {/if}
      Atualizar
    </button>
  </div>

  {#if error}
    <div role="alert" class="alert alert-error mb-4">
      <span class="material-symbols-outlined">error</span>
      <span>{error}</span>
    </div>
  {/if}

  {#if loading && experiments.length === 0}
    <div class="flex justify-center items-center py-12">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {:else if experiments.length === 0}
    <div class="alert alert-info">
      <span class="material-symbols-outlined">info</span>
      <span>Nenhum experimento encontrado. Execute um pipeline para criar experimentos.</span>
    </div>
  {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each experiments as experiment}
        <div class="card bg-base-200 shadow-xl hover:shadow-2xl transition-shadow cursor-pointer border-neutral hover:border-primary" role="button" tabindex="0" onclick={() => openExperiment(experiment.filename)} onkeydown={(e) => e.key === 'Enter' || e.key === ' ' ? openExperiment(experiment.filename) : null}>
          <div class="card-body">
            <div class="badge badge-outline badge-accent mb-2">{getPipelineName(experiment.pipeline)}</div>
            <h2 class="card-title text-sm">{experiment.problem}</h2>
            <p class="text-xs opacity-70">
              <span class="material-symbols-outlined text-sm">schedule</span>
              {formatDate(experiment.timestamp)}
            </p>
            <div class="card-actions justify-end mt-2">
              <button class="btn btn-outline btn-sm btn-neutral">
                Ver Detalhes
                <span class="material-symbols-outlined">arrow_forward</span>
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<!-- Modal -->
{#if modalOpen && selectedExperiment}
  <dialog class="modal modal-open">
    <div class="modal-box max-w-7xl w-full">
      <form method="dialog">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onclick={closeModal}>✕</button>
      </form>
      
      <!-- Informações do Problema -->
      <div class="mb-6 text-center">
        <div class="badge badge-lg badge-accent mb-2">
          {getPipelineName(selectedExperiment.metadata.pipeline)}
        </div>
        <h3 class="text-2xl font-bold mb-2">{selectedExperiment.problem.description}</h3>
        <p class="text-sm opacity-70">
          <span class="material-symbols-outlined text-sm">schedule</span>
          {formatDate(selectedExperiment.metadata.timestamp)}
        </p>
        
        <!-- Premissas e Conclusão -->
        <div class="mt-4 text-left bg-base-300 p-4 rounded-lg">
          <div class="mb-2">
            <span class="font-semibold">Premissas:</span>
            <ul class="list-disc list-inside ml-4">
              {#each selectedExperiment.problem.sentences as sentence}
                <li class="font-mono">{sentence}</li>
              {/each}
            </ul>
          </div>
          <div>
            <span class="font-semibold">Conclusão:</span>
            <span class="font-mono ml-2">{selectedExperiment.problem.conclusion}</span>
          </div>
        </div>
      </div>

      <!-- Duas Caixas Lado a Lado -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div class={getSolverBoxClasses(selectedExperiment)}>
          <h4 class="text-xl font-bold mb-3 flex items-center gap-2">
            <span class="material-symbols-outlined">build</span>
            {getSolverTitle(selectedExperiment)}
          </h4>
          <div class="overflow-y-auto max-h-96">
            <p class="text-sm mb-2"><strong>Modelo:</strong> {selectedExperiment.solver.model}</p>

            {#if !selectedExperiment.solver_output.success}
              <div class="badge badge-error mb-2">Erro</div>
            {/if}

            {#if selectedExperiment.solver_output.steps_raw.length > 0}
              <div>
                <p class="font-semibold mb-1">Passos:</p>
                <ul class="list-disc list-inside ml-2">
                  {#each selectedExperiment.solver_output.steps_raw as step}
                    <li class="font-mono text-sm">{step}</li>
                  {/each}
                </ul>
              </div>
            {/if}
          </div>
        </div>

        <div class={getEvaluatorBoxClasses(selectedExperiment)}>
          <h4 class="text-xl font-bold mb-3 flex items-center gap-2">
            <span class="material-symbols-outlined">fact_check</span>
            {getEvaluatorTitle(selectedExperiment)}
          </h4>
          <div class="overflow-y-auto max-h-96">
            <p class="text-sm mb-2"><strong>Modelo:</strong> {selectedExperiment.evaluator.model}</p>

            {#if !selectedExperiment.evaluation_output.success}
              <div class="badge badge-error mb-2">Erro</div>
              {#if selectedExperiment.evaluation_output.error}
                <p class="text-sm text-error">{selectedExperiment.evaluation_output.error}</p>
              {/if}
            {/if}

            {#if selectedExperiment.evaluation_output.raw_text}
              <div class="whitespace-pre-wrap text-sm mb-3">{selectedExperiment.evaluation_output.raw_text}</div>
            {/if}

            {#if selectedExperiment.evaluation_output.log && selectedExperiment.evaluation_output.log.length > 0}
              <div>
                <p class="font-semibold mb-1">Log do avaliador:</p>
                {#each selectedExperiment.evaluation_output.log as step}
                  <p class="font-mono text-sm mb-1 whitespace-pre-wrap">{step}</p>
                {/each}
              </div>
            {/if}
          </div>
        </div>
      </div>

      <div class="modal-action">
        <button class="btn" onclick={closeModal}>Fechar</button>
      </div>
    </div>
    <button type="button" class="modal-backdrop" onclick={closeModal} aria-label="Fechar modal">
    </button>
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
<script lang="ts">
  import { onMount } from 'svelte';
  import { getExperimentsSample, saveQualitativeEvaluation } from './api';
  import type { Experiment } from '../types';

  let experiments: Experiment[] = [];
  let selectedExperiment: Experiment | null = null;
  let loading = false;
  let error = '';
  let modalOpen = false;

  // Drawer states
  let drawerOpen = false;
  let activeEvaluator: 'evaluator_1' | 'evaluator_2' | null = null;
  let evalForm = { clareza: 0, justificativa: 0, consistencia: 0 };
  let saveLoading = false;
  let saveMessage = '';

  onMount(async () => {
    await loadExperiments();
  });

  async function loadExperiments() {
    loading = true;
    error = '';
    try {
      experiments = await getExperimentsSample();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Erro';
    } finally {
      loading = false;
    }
  }

  function openExperiment(experiment: Experiment) {
    selectedExperiment = experiment;
    modalOpen = true;
    drawerOpen = false;
  }

  function closeModal() {
    modalOpen = false;
    selectedExperiment = null;
    drawerOpen = false;
  }

  function openDrawer(evaluator: 'evaluator_1' | 'evaluator_2') {
    activeEvaluator = evaluator;
    if (selectedExperiment?.qualitative_eval?.[evaluator]) {
        evalForm = { ...selectedExperiment.qualitative_eval[evaluator] };
    } else {
        evalForm = { clareza: 0, justificativa: 0, consistencia: 0 };
    }
    saveMessage = '';
    drawerOpen = true;
  }

  function closeDrawer() {
    drawerOpen = false;
  }

  async function submitEvaluation() {
    if (!selectedExperiment || !activeEvaluator) return;
    saveLoading = true;
    saveMessage = '';
    try {
      await saveQualitativeEvaluation(selectedExperiment.metadata.filename, activeEvaluator, evalForm);
      if (!selectedExperiment.qualitative_eval) {
          selectedExperiment.qualitative_eval = {};
      }
      selectedExperiment.qualitative_eval[activeEvaluator] = { ...evalForm };
      
      // Update in the list
      const idx = experiments.findIndex(e => e.metadata.filename === selectedExperiment!.metadata.filename);
      if (idx !== -1) {
          experiments[idx] = selectedExperiment;
      }
      
      saveMessage = 'Salvo com sucesso!';
      setTimeout(() => { if (drawerOpen) closeDrawer(); }, 1500);
    } catch (e) {
      saveMessage = 'Erro ao salvar!';
    } finally {
      saveLoading = false;
    }
  }

  function getSolverBoxClasses() {
    return 'p-4 rounded-lg border-2 bg-primary-content/10 border-primary';
  }
  function getEvaluatorBoxClasses() {
    return 'p-4 rounded-lg border-2 bg-secondary-content/10 border-secondary relative';
  }
</script>

<div class="container mx-auto p-4">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold">Amostra para Avaliação (20)</h1>
    <button class="btn btn-primary" onclick={loadExperiments} disabled={loading}>
      {#if loading}
        <span class="loading loading-spinner loading-sm"></span>
      {:else}
        <span class="material-symbols-outlined">refresh</span>
      {/if}
      Recarregar
    </button>
  </div>

  {#if error}
    <div role="alert" class="alert alert-error mb-4"><span>{error}</span></div>
  {/if}

  {#if experiments.length === 0 && !loading}
    <div class="alert alert-info">Nenhum experimento encontrado.</div>
  {/if}

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {#each experiments as experiment}
      <!-- svelte-ignore a11y_interactive_supports_focus -->
      <div class="card bg-base-200 shadow-xl hover:shadow-2xl cursor-pointer border-neutral hover:border-primary" role="button" onkeydown={(e) => e.key==='Enter' && openExperiment(experiment)} onclick={() => openExperiment(experiment)}>
        <div class="card-body">
          <div class="badge badge-outline badge-accent mb-2">{experiment.metadata.pipeline}</div>
          <h2 class="card-title text-sm">{experiment.problem.description}</h2>
          <div class="mt-2 text-xs flex gap-2">
            <span class={`badge ${experiment.qualitative_eval?.evaluator_1 ? 'badge-success' : 'badge-ghost'}`}>E1</span>
            <span class={`badge ${experiment.qualitative_eval?.evaluator_2 ? 'badge-success' : 'badge-ghost'}`}>E2</span>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>

{#if modalOpen && selectedExperiment}
  <dialog class="modal modal-open">
    <div class="modal-box max-w-7xl w-full h-[90vh] flex flex-col relative overflow-hidden p-0">
      <div class="p-6 overflow-y-auto flex-1 transition-all duration-300" style={drawerOpen ? "margin-right: 20rem;" : ""}>
          <button class="btn btn-sm btn-circle btn-ghost absolute top-2 z-50 transition-all duration-300" style={drawerOpen ? "right: 20.5rem;" : "right: 0.5rem;"} onclick={closeModal}>✕</button>
          
          <div class="mb-6 text-center">
            <h3 class="text-2xl font-bold mb-2">{selectedExperiment.problem.description}</h3>
            
            <div class="mt-4 text-left bg-base-300 p-4 rounded-lg">
              <div class="mb-2"><span class="font-semibold">Premissas:</span>
                <ul class="list-disc list-inside ml-4">
                  {#each selectedExperiment.problem.sentences as sentence}
                    <li class="font-mono">{sentence}</li>
                  {/each}
                </ul>
              </div>
              <div><span class="font-semibold">Conclusão:</span> <span class="font-mono ml-2">{selectedExperiment.problem.conclusion}</span></div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 relative">
            <div class={getSolverBoxClasses()}>
              <h4 class="text-xl font-bold mb-3">Resolvedor</h4>
              <div class="overflow-y-auto max-h-screen">
                {#if selectedExperiment.solver_output.steps_raw.length > 0}
                  <ul class="list-disc list-inside ml-2">
                    {#each selectedExperiment.solver_output.steps_raw as step}
                      <li class="font-mono text-sm">{step}</li>
                    {/each}
                  </ul>
                {/if}
              </div>
            </div>

            <div class={getEvaluatorBoxClasses()}>
              <div class="flex justify-between items-center mb-3">
                <h4 class="text-xl font-bold">Avaliador (LLM)</h4>
                <div class="join">
                    <button class="btn btn-sm btn-secondary join-item" onclick={() => openDrawer('evaluator_1')}>Av. 1</button>
                    <button class="btn btn-sm btn-primary join-item" onclick={() => openDrawer('evaluator_2')}>Av. 2</button>
                </div>
              </div>
              <div class="overflow-y-auto" style="max-h: 60vh;">
                  {#if !selectedExperiment.evaluation_output.success}
                      <div class="badge badge-error mb-2">Erro</div>
                  {/if}
                  {#if selectedExperiment.evaluation_output.log}
                    {#each selectedExperiment.evaluation_output.log as line}
                      <p class="font-mono text-sm mb-1 whitespace-pre-wrap">{line}</p>
                    {/each}
                  {/if}
              </div>
            </div>
          </div>
      </div>

      <!-- Drawer -->
      <div class={`absolute top-0 right-0 w-80 h-full bg-base-100 shadow-[0_0_15px_rgba(0,0,0,0.5)] transform transition-transform duration-300 z-50 flex flex-col ${drawerOpen ? 'translate-x-0' : 'translate-x-full'}`}>
        <div class="p-4 border-b border-base-300 flex justify-between items-center bg-base-200">
            <h3 class="font-bold text-lg">{activeEvaluator === 'evaluator_1' ? 'Especialista 1' : 'Especialista 2'}</h3>
            <button class="btn btn-sm btn-circle btn-ghost" onclick={closeDrawer}>✕</button>
        </div>
        <div class="p-6 flex-1 overflow-y-auto space-y-6">
            <!-- Clareza -->
            <div class="form-control">
                <div class="mb-2"><span class="label-text font-bold">Clareza</span></div>
                <label class="label cursor-pointer justify-start gap-4">
                    <input type="radio" name="clareza" class="radio radio-primary radio-sm" value={1} bind:group={evalForm.clareza} />
                    <span class="label-text">( 1 ) Insatisfatório</span>
                </label>
                <label class="label cursor-pointer justify-start gap-4">
                    <input type="radio" name="clareza" class="radio radio-primary radio-sm" value={2} bind:group={evalForm.clareza} />
                    <span class="label-text">( 2 ) Parcialmente</span>
                </label>
                <label class="label cursor-pointer justify-start gap-4">
                    <input type="radio" name="clareza" class="radio radio-primary radio-sm" value={3} bind:group={evalForm.clareza} />
                    <span class="label-text">( 3 ) Totalmente</span>
                </label>
            </div>

            <!-- Justificativa -->
            <div class="form-control">
                <div class="mb-2"><span class="label-text font-bold">Justificativa</span></div>
                <label class="label cursor-pointer justify-start gap-4">
                    <input type="radio" name="justificativa" class="radio radio-primary radio-sm" value={1} bind:group={evalForm.justificativa} />
                    <span class="label-text">( 1 ) Insatisfatória</span>
                </label>
                <label class="label cursor-pointer justify-start gap-4">
                    <input type="radio" name="justificativa" class="radio radio-primary radio-sm" value={2} bind:group={evalForm.justificativa} />
                    <span class="label-text">( 2 ) Parcialmente</span>
                </label>
                <label class="label cursor-pointer justify-start gap-4">
                    <input type="radio" name="justificativa" class="radio radio-primary radio-sm" value={3} bind:group={evalForm.justificativa} />
                    <span class="label-text">( 3 ) Totalmente</span>
                </label>
            </div>

            <!-- Consistência -->
            <div class="form-control">
                <div class="mb-2"><span class="label-text font-bold">Consistência</span></div>
                <label class="label cursor-pointer justify-start gap-4">
                    <input type="radio" name="consistencia" class="radio radio-primary radio-sm" value={1} bind:group={evalForm.consistencia} />
                    <span class="label-text">( 1 ) Insatisfatória</span>
                </label>
                <label class="label cursor-pointer justify-start gap-4">
                    <input type="radio" name="consistencia" class="radio radio-primary radio-sm" value={2} bind:group={evalForm.consistencia} />
                    <span class="label-text">( 2 ) Parcialmente</span>
                </label>
                <label class="label cursor-pointer justify-start gap-4">
                    <input type="radio" name="consistencia" class="radio radio-primary radio-sm" value={3} bind:group={evalForm.consistencia} />
                    <span class="label-text">( 3 ) Totalmente</span>
                </label>
            </div>
        </div>
        <div class="p-4 border-t border-base-300 bg-base-200">
            <button class="btn btn-primary w-full" onclick={submitEvaluation} disabled={saveLoading || !evalForm.clareza || !evalForm.justificativa || !evalForm.consistencia}>
                {#if saveLoading}<span class="loading loading-spinner loading-sm"></span>{/if}
                Salvar Avaliação
            </button>
            {#if saveMessage}
                <div class="text-center mt-2 text-sm text-success">{saveMessage}</div>
            {/if}
        </div>
      </div>

    </div>
    <button type="button" class="modal-backdrop" onclick={closeModal} aria-label="Fechar"></button>
  </dialog>
{/if}

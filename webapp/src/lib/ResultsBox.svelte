<script lang="ts">
  // Recebe as props do componente pai
  let { result = $bindable(null), lastPipeline = $bindable(null) } = $props();

  function getPipelineName(pipeline: number): string {
    return pipeline === 1 ? 'W → LLM' : 'LLM → W';
  }

  function getExperimentData() {
    return result?.experiment ?? null;
  }

  function getSolverTitle(experiment: any): string {
    return experiment?.solver?.type === 'llm' ? 'Solução do LLM' : 'Resolvedor Agente W';
  }

  function getEvaluatorTitle(experiment: any): string {
    return experiment?.evaluator?.type === 'llm' ? 'Avaliação do LLM' : 'Avaliador Agente W';
  }

  function getSolverBoxClasses(experiment: any): string {
    const isLLM = experiment?.solver?.type === 'llm';
    return `p-4 rounded-lg border-2 ${isLLM ? 'bg-secondary-content/10 border-secondary' : 'bg-primary-content/10 border-primary'}`;
  }

  function getEvaluatorBoxClasses(experiment: any): string {
    const isLLM = experiment?.evaluator?.type === 'llm';
    return `p-4 rounded-lg border-2 ${isLLM ? 'bg-secondary-content/10 border-secondary' : 'bg-primary-content/10 border-primary'}`;
  }
</script>

<!-- Result -->
{#if result && (getExperimentData() || lastPipeline)}
  {@const experiment = getExperimentData()}
  <div class="mt-6">
    <div class="alert alert-success mb-4">
      <span class="material-symbols-outlined">check_circle</span>
      <span>Problema processado com sucesso!</span>
      <div class="badge badge-accent-content ml-auto">
        {#if experiment}
          {experiment.metadata.pipeline === 'solver_to_llm' ? 'W → LLM' : 'LLM → W'}
        {:else}
          {getPipelineName(lastPipeline)}
        {/if}
      </div>
    </div>

    <!-- Resultado organizado -->
    <div class="space-y-4">
      {#if experiment}
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div class={getSolverBoxClasses(experiment)}>
            <h4 class="text-lg font-bold mb-3 flex items-center gap-2">
              <span class="material-symbols-outlined">build</span>
              {getSolverTitle(experiment)}
            </h4>
            <div class="bg-base-300 p-3 rounded-lg overflow-y-auto max-h-128">
              <p class="text-sm mb-2"><strong>Modelo:</strong> {experiment.solver.model}</p>

              {#if experiment.solver_output.steps_raw?.length > 0}
                <div>
                  <p class="font-semibold mb-1">Passos:</p>
                  <ul class="list-disc list-inside ml-2">
                    {#each experiment.solver_output.steps_raw as step}
                      <li class="font-mono text-sm">{step}</li>
                    {/each}
                  </ul>
                </div>
              {/if}
            </div>
          </div>

          <div class={getEvaluatorBoxClasses(experiment)}>
            <h4 class="text-lg font-bold mb-3 flex items-center gap-2">
              <span class="material-symbols-outlined">fact_check</span>
              {getEvaluatorTitle(experiment)}
            </h4>
            <div class="bg-base-300 p-3 rounded-lg overflow-y-auto max-h-128">
              <p class="text-sm mb-2"><strong>Modelo:</strong> {experiment.evaluator.model}</p>

              {#if !experiment.evaluation_output.success}
                <div class="badge badge-error mb-2">Erro</div>
                {#if experiment.evaluation_output.error}
                  <p class="text-sm text-error">{experiment.evaluation_output.error}</p>
                {/if}
              {/if}

              {#if experiment.evaluation_output.raw_text}
                <div class="whitespace-pre-wrap text-sm mb-3">{experiment.evaluation_output.raw_text}</div>
              {/if}

              {#if experiment.evaluation_output.log?.length > 0}
                {#each experiment.evaluation_output.log as step}
                  <p class="font-mono text-sm mb-1 whitespace-pre-wrap">{step}</p>
                {/each}
              {/if}
            </div>
          </div>
        </div>
      {/if}

      <!-- Informações adicionais -->
      {#if result.saved_to}
        <div class="alert alert-info">
          <span class="material-symbols-outlined">save</span>
          <div class="flex-1">
            <span class="font-semibold">Experimento salvo:</span>
            <code class="ml-2 text-xs">{result.saved_to}</code>
          </div>
        </div>
      {/if}
    </div>
  </div>
{/if}
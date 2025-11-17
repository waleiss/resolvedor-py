<!-- Result -->
      {#if result && lastPipeline}
        <div class="mt-6">
          <div class="alert alert-success mb-4">
            <span class="material-symbols-outlined">check_circle</span>
            <span>Problema processado com sucesso!</span>
            <div class="badge badge-outline badge-accent ml-auto">{getPipelineName(lastPipeline)}</div>
          </div>

          <!-- Resultado organizado -->
          <div class="space-y-4">
            {#if lastPipeline === 1}
              <!-- Pipeline 1: Solver → LLM -->
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <!-- Solver Result -->
                <div class="bg-primary/5 p-4 rounded-lg border-2 border-primary">
                  <h4 class="text-lg font-bold mb-3 flex items-center gap-2">
                    <span class="material-symbols-outlined">build</span>
                    Resolvedor Agente W
                  </h4>
                  <div class="bg-base-300 p-3 rounded-lg overflow-y-auto max-h-64">
                    {#each result.solver_log as step}
                      <p class="font-mono text-sm mb-1 whitespace-pre-wrap">{step}</p>
                    {/each}
                  </div>
                </div>

                <!-- Gemini Evaluation -->
                <div class="bg-secondary/5 p-4 rounded-lg border-2 border-secondary">
                  <h4 class="text-lg font-bold mb-3 flex items-center gap-2">
                    <span class="material-symbols-outlined">smart_toy</span>
                    Avaliação do LLM
                  </h4>
                  <div class="bg-base-300 p-3 rounded-lg overflow-y-auto max-h-64">
                    {#if result.gemini_evaluation.success}
                      <p class="text-sm mb-2"><strong>Modelo:</strong> {result.gemini_evaluation.model}</p>
                      <div class="whitespace-pre-wrap text-sm">{result.gemini_evaluation.evaluation}</div>
                    {:else}
                      <div class="badge badge-error mb-2">Erro</div>
                      <p class="text-sm text-error">{result.gemini_evaluation.error}</p>
                    {/if}
                  </div>
                </div>
              </div>
            {:else}
              <!-- Pipeline 2: LLM → Evaluator -->
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <!-- Gemini Solution -->
                <div class="bg-secondary/5 p-4 rounded-lg border-2 border-secondary">
                  <h4 class="text-lg font-bold mb-3 flex items-center gap-2">
                    <span class="material-symbols-outlined">smart_toy</span>
                    Solução do LLM
                  </h4>
                  <div class="bg-base-300 p-3 rounded-lg overflow-y-auto max-h-64">
                    {#if result.gemini_solution.success}
                      <p class="text-sm mb-2"><strong>Modelo:</strong> {result.gemini_solution.model}</p>
                      <div class="mb-3">
                        <p class="font-semibold mb-1">Solução:</p>
                        <div class="whitespace-pre-wrap text-sm bg-base-200 p-2 rounded">{result.gemini_solution.solution}</div>
                      </div>
                      <div>
                        <p class="font-semibold mb-1">Inferências extraídas:</p>
                        <ul class="list-disc list-inside ml-2">
                          {#each result.gemini_solution.inferences as inference}
                            <li class="font-mono text-sm">{inference}</li>
                          {/each}
                        </ul>
                      </div>
                    {:else}
                      <div class="badge badge-error mb-2">Erro</div>
                      <p class="text-sm text-error">{result.gemini_solution.error}</p>
                    {/if}
                  </div>
                </div>

                <!-- Evaluator Result -->
                <div class="bg-accent/5 p-4 rounded-lg border-2 border-primary">
                  <h4 class="text-lg font-bold mb-3 flex items-center gap-2">
                    <span class="material-symbols-outlined">fact_check</span>
                    Avaliador Agente W
                  </h4>
                  <div class="bg-base-300 p-3 rounded-lg overflow-y-auto max-h-64">
                    {#each result.evaluator_log as step}
                      <p class="font-mono text-sm mb-1 whitespace-pre-wrap">{step}</p>
                    {/each}
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
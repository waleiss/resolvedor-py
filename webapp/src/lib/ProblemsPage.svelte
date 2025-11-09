<script lang="ts">
import type { Argument } from '../types';

// Mock data - in a real app, this would come from an API
let problems = $state<Array<Argument & { id: number; date: string }>>([
  {
    id: 1,
    sentences: ['p → q', 'p'],
    conclusion: 'q',
    date: '2025-11-09'
  },
  {
    id: 2,
    sentences: ['p ∨ q', '¬p'],
    conclusion: 'q',
    date: '2025-11-08'
  },
  {
    id: 3,
    sentences: ['p ∧ q', 'p → r', 'q → s'],
    conclusion: 'r ∧ s',
    date: '2025-11-07'
  }
]);
</script>

<div class="container mx-auto p-4">
  <div class="flex justify-between items-center mb-6">
    <h2 class="text-3xl font-bold">Problemas Armazenados</h2>
    <a href="#/" class="btn btn-primary">
      ➕ Novo Problema
    </a>
  </div>
  
  <div class="grid gap-4">
    {#if problems.length === 0}
      <div class="alert">
        <span>Nenhum problema armazenado ainda.</span>
      </div>
    {:else}
      {#each problems as problem}
        <div class="card bg-base-200 shadow-xl">
          <div class="card-body">
            <div class="flex justify-between items-start">
              <h3 class="card-title">Problema #{problem.id}</h3>
              <span class="badge badge-primary">{problem.date}</span>
            </div>
            
            <div class="divider"></div>
            
            <div class="space-y-2">
              <div>
                <p class="text-sm font-semibold text-base-content/70">Premissas:</p>
                <ul class="list-disc list-inside space-y-1 ml-2">
                  {#each problem.sentences as sentence}
                    <li class="font-mono text-lg">{sentence}</li>
                  {/each}
                </ul>
              </div>
              
              <div>
                <p class="text-sm font-semibold text-base-content/70">Conclusão:</p>
                <p class="font-mono text-lg ml-2">∴ {problem.conclusion}</p>
              </div>
            </div>
            
            <div class="card-actions justify-end mt-4">
              <button class="btn btn-sm btn-outline btn-primary">
                Ver Solução
              </button>
              <button class="btn btn-sm btn-outline btn-error">
                Excluir
              </button>
            </div>
          </div>
        </div>
      {/each}
    {/if}
  </div>
</div>

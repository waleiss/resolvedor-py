<script lang="ts">
  import { onMount } from 'svelte';
  import { getExperimentsWithAnalysis } from './api';
  import type { Experiment, AnalysisErrorType } from '../types';

  type TeamKey = 'agent_w' | 'gemini';
  type DifficultyKey = 'easy' | 'medium' | 'hard' | 'unknown';
  type StructureKey =
    | 'Muitos Modus Ponens'
    | 'Muitas negações'
    | 'De Morgan'
    | 'Disjunção'
    | 'Mista / Outros';

  interface BucketStats {
    total: number;
    analyzed: number;
    success: number;
    fullyCorrect: number;
    conclusionCorrect: number;
    validRatioSum: number;
    stepsSum: number;
  }

  interface TeamStats extends BucketStats {
    difficulties: Record<string, BucketStats>;
    structures: Record<string, BucketStats>;
    errors: Record<string, number>;
  }

  interface MetricsState {
    agent_w: TeamStats;
    gemini: TeamStats;
  }

  const overallRows = [
    { key: 'success', label: 'Taxa de sucesso' },
    { key: 'fullyCorrect', label: 'Taxa de correção completa' },
    { key: 'conclusionCorrect', label: 'Taxa de conclusão correta' },
    { key: 'validSteps', label: 'Percentual de passos válidos' },
    { key: 'avgSteps', label: 'Número médio de passos' },
  ] as const;

  const difficultyRows: DifficultyKey[] = ['easy', 'medium', 'hard'];
  const difficultyLabels: Record<DifficultyKey, string> = {
    easy: 'Fácil',
    medium: 'Médio',
    hard: 'Difícil',
    unknown: 'Sem classificação',
  };
  const structureRows: StructureKey[] = [
    'Muitos Modus Ponens',
    'Muitas negações',
    'De Morgan',
    'Disjunção',
    'Mista / Outros',
  ];
  const errorRows: AnalysisErrorType[] = [
    'aplicação inválida de regra',
    'regra inexistente',
    'conclusão não alcançada',
    'uso incorreto de referência a linhas anteriores',
  ];

  const teamLabels: Record<TeamKey, string> = {
    agent_w: 'Agente W',
    gemini: 'Gemini',
  };

  let loading = true;
  let error = '';
  let experiments: Experiment[] = [];
  let metrics: MetricsState = createEmptyMetricsState();

  onMount(async () => {
    await loadMetrics();
  });

  async function loadMetrics() {
    loading = true;
    error = '';

    try {
      experiments = await getExperimentsWithAnalysis();
      metrics = buildMetrics(experiments);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Erro ao carregar métricas';
    } finally {
      loading = false;
    }
  }

  function createEmptyBucket(): BucketStats {
    return {
      total: 0,
      analyzed: 0,
      success: 0,
      fullyCorrect: 0,
      conclusionCorrect: 0,
      validRatioSum: 0,
      stepsSum: 0,
    };
  }

  function createEmptyTeamStats(): TeamStats {
    return {
      ...createEmptyBucket(),
      difficulties: {},
      structures: {},
      errors: {},
    };
  }

  function createEmptyMetricsState(): MetricsState {
    return {
      agent_w: createEmptyTeamStats(),
      gemini: createEmptyTeamStats(),
    };
  }

  function getTeamKey(experiment: Experiment): TeamKey {
    return experiment.solver?.type === 'llm' ? 'gemini' : 'agent_w';
  }

  function normalizeDifficulty(value?: string): DifficultyKey {
    const normalized = value?.toLowerCase?.() ?? '';

    if (normalized === 'easy' || normalized === 'medium' || normalized === 'hard') {
      return normalized;
    }

    return 'unknown';
  }

  function getStructureKey(experiment: Experiment): StructureKey {
    const text = [
      experiment.problem?.description ?? '',
      ...(experiment.problem?.sentences ?? []),
      experiment.problem?.conclusion ?? '',
    ].join(' ');

    const implicationCount = (text.match(/→/g) ?? []).length;
    const negationCount = (text.match(/¬/g) ?? []).length;
    const disjunctionCount = (text.match(/∨/g) ?? []).length;
    const conjunctionCount = (text.match(/∧/g) ?? []).length;

    const hasDeMorganPattern = /¬\s*\([^)]*[∧∨][^)]*\)/.test(text) || (negationCount >= 1 && conjunctionCount + disjunctionCount >= 1);

    if (hasDeMorganPattern) {
      return 'De Morgan';
    }

    if (negationCount >= 3) {
      return 'Muitas negações';
    }

    if (disjunctionCount >= 2) {
      return 'Disjunção';
    }

    if (implicationCount >= 2) {
      return 'Muitos Modus Ponens';
    }

    return 'Mista / Outros';
  }

  function ensureBucket(container: Record<string, BucketStats>, key: string): BucketStats {
    if (!container[key]) {
      container[key] = createEmptyBucket();
    }

    return container[key];
  }

  function accumulateBucket(bucket: BucketStats, experiment: Experiment) {
    bucket.total += 1;

    if (experiment.solver_output?.success) {
      bucket.success += 1;
    }

    if (!experiment.analysis) {
      return;
    }

    bucket.analyzed += 1;

    if (experiment.analysis.is_fully_correct) {
      bucket.fullyCorrect += 1;
    }

    if (experiment.analysis.reaches_target_conclusion) {
      bucket.conclusionCorrect += 1;
    }

    const steps = experiment.analysis.num_steps;
    const validSteps = experiment.analysis.num_valid_steps;

    if (steps > 0) {
      bucket.validRatioSum += validSteps / steps;
    }

    bucket.stepsSum += steps;
  }

  function buildMetrics(source: Experiment[]): MetricsState {
    const state = createEmptyMetricsState();

    for (const experiment of source) {
      const teamKey = getTeamKey(experiment);
      const team = state[teamKey];

      team.total += 1;

      if (experiment.solver_output?.success) {
        team.success += 1;
      }

      if (experiment.analysis) {
        team.analyzed += 1;

        if (experiment.analysis.is_fully_correct) {
          team.fullyCorrect += 1;
        }

        if (experiment.analysis.reaches_target_conclusion) {
          team.conclusionCorrect += 1;
        }

        const steps = experiment.analysis.num_steps;
        const validSteps = experiment.analysis.num_valid_steps;

        if (steps > 0) {
          team.validRatioSum += validSteps / steps;
        }

        team.stepsSum += steps;
      }

      const difficultyBucket = ensureBucket(team.difficulties, normalizeDifficulty(experiment.problem?.difficulty));
      accumulateBucket(difficultyBucket, experiment);

      const structureBucket = ensureBucket(team.structures, getStructureKey(experiment));
      accumulateBucket(structureBucket, experiment);

      if (experiment.analysis?.error_type) {
        const errorKey = experiment.analysis.error_type;
        team.errors[errorKey] = (team.errors[errorKey] ?? 0) + 1;
      }
    }

    return state;
  }

  function formatPercent(value: number, total: number): string {
    if (!total) {
      return '—';
    }

    return `${((value / total) * 100).toFixed(1)}%`;
  }

  function formatAverage(value: number, total: number): string {
    if (!total) {
      return '—';
    }

    return (value / total).toFixed(2);
  }

  function getMetricValue(stats: TeamStats, metric: string): string {
    switch (metric) {
      case 'success':
        return formatPercent(stats.success, stats.total);
      case 'fullyCorrect':
        return formatPercent(stats.fullyCorrect, stats.analyzed);
      case 'conclusionCorrect':
        return formatPercent(stats.conclusionCorrect, stats.analyzed);
      case 'validSteps':
        return formatPercent(stats.validRatioSum, stats.analyzed);
      case 'avgSteps':
        return formatAverage(stats.stepsSum, stats.analyzed);
      default:
        return '—';
    }
  }

  function getBucketSummary(bucket: BucketStats): string {
    return [
      `Sucesso: ${formatPercent(bucket.success, bucket.total)}`,
      `Correção: ${formatPercent(bucket.fullyCorrect, bucket.analyzed)}`,
      `Conclusão: ${formatPercent(bucket.conclusionCorrect, bucket.analyzed)}`,
      `Passos válidos: ${formatPercent(bucket.validRatioSum, bucket.analyzed)}`,
      `Média de passos: ${formatAverage(bucket.stepsSum, bucket.analyzed)}`,
    ].join('\n');
  }

  function getErrorRowsTotal(stats: TeamStats): number {
    return Object.values(stats.errors).reduce((sum, value) => sum + value, 0);
  }

  function getBucket(stats: TeamStats, category: string, bucketMap: 'difficulties' | 'structures'): BucketStats {
    return stats[bucketMap][category] ?? createEmptyBucket();
  }

  function formatErrorCell(stats: TeamStats, errorType: AnalysisErrorType): string {
    const totalErrors = getErrorRowsTotal(stats);
    const count = stats.errors[errorType] ?? 0;

    if (!totalErrors) {
      return '—';
    }

    return `${count} (${formatPercent(count, totalErrors)})`;
  }
</script>

<div class="container mx-auto p-4 space-y-6">
  <div class="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
    <div>
      <h1 class="text-3xl font-bold">Metrics</h1>
      <p class="opacity-70">Resumo comparativo entre Agente W e Gemini usando o campo analysis dos experimentos.</p>
    </div>

    <button class="btn btn-primary" on:click={loadMetrics} disabled={loading}>
      {#if loading}
        <span class="loading loading-spinner loading-sm"></span>
      {:else}
        <span class="material-symbols-outlined">refresh</span>
      {/if}
      Atualizar
    </button>
  </div>

  {#if error}
    <div role="alert" class="alert alert-error">
      <span class="material-symbols-outlined">error</span>
      <span>{error}</span>
    </div>
  {/if}

  {#if loading && experiments.length === 0}
    <div class="flex justify-center items-center py-16">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {:else}
    {@const agentStats = metrics.agent_w}
    {@const geminiStats = metrics.gemini}

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div class="card bg-base-200 shadow-xl border border-base-300">
        <div class="card-body">
          <h2 class="card-title">
            <span class="px-3 py-1 rounded-md border border-primary">Agente W</span>
          </h2>
          <p class="text-sm opacity-70">{agentStats.total} experimentos, {agentStats.analyzed} com analysis disponível</p>
          <div class="overflow-x-auto mt-2">
            <table class="table table-zebra">
              <tbody>
                {#each overallRows as row}
                  <tr>
                    <td class="font-medium">{row.label}</td>
                    <td class="text-right font-mono">{getMetricValue(agentStats, row.key)}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="card bg-base-200 shadow-xl border border-base-300">
        <div class="card-body">
          <h2 class="card-title">
            <span class="px-3 py-1 rounded-md border border-secondary">Gemini</span>
          </h2>
          <p class="text-sm opacity-70">{geminiStats.total} experimentos, {geminiStats.analyzed} com analysis disponível</p>
          <div class="overflow-x-auto mt-2">
            <table class="table table-zebra">
              <tbody>
                {#each overallRows as row}
                  <tr>
                    <td class="font-medium">{row.label}</td>
                    <td class="text-right font-mono">{getMetricValue(geminiStats, row.key)}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div class="card bg-base-200 shadow-xl border border-base-300">
      <div class="card-body">
        <div class="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
          <div>
            <h2 class="card-title">Taxas por dificuldade</h2>
            <p class="text-sm opacity-70">Desempenho agregado por nível de dificuldade.</p>
          </div>
        </div>

        <div class="overflow-x-auto mt-2">
          <table class="table table-zebra">
            <thead>
              <tr>
                <th>Dificuldade</th>
                <th>
                  <span class="inline-block px-2 py-1 rounded-md border border-primary">{teamLabels.agent_w}</span>
                </th>
                <th>
                  <span class="inline-block px-2 py-1 rounded-md border border-secondary">{teamLabels.gemini}</span>
                </th>
              </tr>
            </thead>
            <tbody>
              {#each difficultyRows as difficulty}
                <tr>
                  <td class="font-medium">{difficultyLabels[difficulty]}</td>
                  <td>
                    <pre class="whitespace-pre-wrap font-mono text-xs leading-5">{getBucketSummary(getBucket(agentStats, difficulty, 'difficulties'))}</pre>
                  </td>
                  <td>
                    <pre class="whitespace-pre-wrap font-mono text-xs leading-5">{getBucketSummary(getBucket(geminiStats, difficulty, 'difficulties'))}</pre>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="card bg-base-200 shadow-xl border border-base-300">
      <div class="card-body">
        <div class="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
          <div>
            <h2 class="card-title">Taxas por tipo de estrutura lógica</h2>
            <p class="text-sm opacity-70">Classificação heurística com base nas fórmulas do problema.</p>
          </div>
        </div>

        <div class="overflow-x-auto mt-2">
          <table class="table table-zebra">
            <thead>
              <tr>
                <th>Estrutura</th>
                <th>
                  <span class="inline-block px-2 py-1 rounded-md border border-primary">{teamLabels.agent_w}</span>
                </th>
                <th>
                  <span class="inline-block px-2 py-1 rounded-md border border-secondary">{teamLabels.gemini}</span>
                </th>
              </tr>
            </thead>
            <tbody>
              {#each structureRows as structure}
                <tr>
                  <td class="font-medium">{structure}</td>
                  <td>
                    <pre class="whitespace-pre-wrap font-mono text-xs leading-5">{getBucketSummary(getBucket(agentStats, structure, 'structures'))}</pre>
                  </td>
                  <td>
                    <pre class="whitespace-pre-wrap font-mono text-xs leading-5">{getBucketSummary(getBucket(geminiStats, structure, 'structures'))}</pre>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="card bg-base-200 shadow-xl border border-base-300">
      <div class="card-body">
        <div>
          <h2 class="card-title">Frequência de erros por tipo</h2>
          <p class="text-sm opacity-70">Distribuição dos principais erros detectados pelo analysis estruturado.</p>
        </div>

        <div class="overflow-x-auto mt-2">
          <table class="table table-zebra">
            <thead>
              <tr>
                <th>Erro</th>
                <th>
                  <span class="inline-block px-2 py-1 rounded-md border border-primary">{teamLabels.agent_w}</span>
                </th>
                <th>
                  <span class="inline-block px-2 py-1 rounded-md border border-secondary">{teamLabels.gemini}</span>
                </th>
              </tr>
            </thead>
            <tbody>
              {#each errorRows as errorType}
                <tr>
                  <td class="font-medium">{errorType}</td>
                  <td class="font-mono text-sm">{formatErrorCell(agentStats, errorType)}</td>
                  <td class="font-mono text-sm">{formatErrorCell(geminiStats, errorType)}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="alert alert-info">
      <span class="material-symbols-outlined">info</span>
      <span>Métricas calculadas a partir dos experimentos salvos com analysis disponível.</span>
    </div>
  {/if}
</div>
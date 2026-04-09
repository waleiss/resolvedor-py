<script lang="ts">
import Router from 'svelte-spa-router'
import Home from './lib/Home.svelte'
import Navbar from "./lib/Navbar.svelte"
import ViewResults from './lib/ViewResults.svelte'
import Metrics from './lib/Metrics.svelte'
import ProblemsBank from './lib/ProblemsBank.svelte'
import Evaluate from './lib/Evaluate.svelte'

const routes = {
  '/': Home,
  '/resultados': ViewResults,
  '/metricas': Metrics,
  '/problemas': ProblemsBank,
  '/avaliar': Evaluate
};
</script>

<div class="min-h-screen flex flex-col">
  <Navbar />
  <main class="flex flex-col flex-1">
    <Router {routes} />
  </main>
</div>

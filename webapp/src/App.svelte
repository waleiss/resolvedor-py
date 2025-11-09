<script lang="ts">
import Router from 'svelte-spa-router'
import Navbar from "./lib/Navbar.svelte"
import ProblemsPage from './lib/ProblemsPage.svelte'
import Home from './lib/Home.svelte'

const routes = {
  '/': Home,
  '/problemas': ProblemsPage,
};
</script>

<div class="min-h-screen flex flex-col">
  <Navbar />
  <main class="flex flex-col flex-1">
    <Router {routes} />
  </main>
</div>

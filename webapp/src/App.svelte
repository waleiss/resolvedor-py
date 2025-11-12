<script lang="ts">
import Router from 'svelte-spa-router'
import Home from './lib/Home.svelte'
import Navbar from "./lib/Navbar.svelte"
import ViewResults from './lib/ViewResults.svelte'

const routes = {
  '/': Home,
  '/problemas': ViewResults,
};
</script>

<div class="min-h-screen flex flex-col">
  <Navbar />
  <main class="flex flex-col flex-1">
    <Router {routes} />
  </main>
</div>

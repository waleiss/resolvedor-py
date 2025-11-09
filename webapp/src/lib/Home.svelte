<script lang="ts">
import ProblemForm from './ProblemForm.svelte'
import LogicalKeyboard from './LogicalKeyboard.svelte';
</script>

<div class="flex flex-col gap-2 mx-2 lg:container lg:mx-auto flex-1 py-6">
  <h2 class="text-3xl font-bold text-left mb-4">Insira um problema</h2>
  <ProblemForm />
  <LogicalKeyboard />
</div>

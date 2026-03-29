<div class="navbar bg-base-300 shadow-lg sticky top-0 z-40 px-2">
  <div class="flex-1 min-w-0">
    <a
      href="#/"
      class="btn btn-ghost normal-case text-base sm:text-xl ml-0 sm:ml-2 px-2 sm:px-3 min-w-0"
    >
      <span class="text-primary flex items-center gap-2 min-w-0">
        <span class="material-symbols-outlined shrink-0">cognition</span>
        <span class="truncate">Ambiente de Lógica</span>
      </span>
    </a>
  </div>

  <div class="flex-none">
    <!-- Mobile -->
    <div class="dropdown dropdown-end md:hidden">
      <button tabindex="0" class="btn btn-ghost btn-circle" aria-label="Abrir menu">
        <span class="material-symbols-outlined">menu</span>
      </button>
      <ul
        class="menu dropdown-content mt-3 z-60 p-2 shadow bg-base-200 rounded-box w-52"
      >
        <li>
          <a href="#/" class="flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px]">home</span>
            Home
          </a>
        </li>
        <li>
          <a href="#/problemas" class="flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px]">quiz</span>
            Problemas
          </a>
        </li>
        <li>
          <a href="#/resultados" class="flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px]">description</span>
            Resultados
          </a>
        </li>
      </ul>
    </div>

    <!-- Desktop -->
    <ul class="menu menu-horizontal px-1 hidden md:flex">
      <li>
        <a href="#/" class="hover:text-primary flex items-center gap-1">
          <span class="material-symbols-outlined text-[20px]">home</span>
          Home
        </a>
      </li>
      <li>
        <a href="#/problemas" class="hover:text-primary flex items-center gap-1">
          <span class="material-symbols-outlined text-[20px]">quiz</span>
          Problemas
        </a>
      </li>
      <li>
        <a href="#/resultados" class="hover:text-primary flex items-center gap-1">
          <span class="material-symbols-outlined text-[20px]">description</span>
          Resultados
        </a>
      </li>
    </ul>
  </div>
</div>
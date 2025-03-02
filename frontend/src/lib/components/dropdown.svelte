<script>
  export let buttontext = "Edit";
  export let style = "";
  export let isOpen = false; // State to control dropdown visibility

  // Toggliranje vidljivosti dropdown menija
  function toggleDropdown() {
    isOpen = !isOpen;
  }
</script>

<!-- Dropdown kontejner sa relativnim pozicioniranjem -->
<div class="relative inline-block">
  {#if style != 'nothing'}
    <!-- Gumb za otvaranje dropdown menija sa dinamičkim klasama -->
    <button class={style} on:click={toggleDropdown}>{buttontext}</button>
  {/if}
  
  {#if isOpen}
    <!-- Dropdown meni sa Tailwind CSS klasama za pozicioniranje, visinu, širinu i stilove -->
    <ul class="absolute top-full left-0 bg-black border border-gray-300 shadow-md z-[1000] max-h-[200px] overflow-y-auto w-[200px] min-h-[50px] p-0 m-0 list-none">
      <!-- Slot za dinamične stavke unutar menija -->
      <slot></slot>
    </ul>
  {/if}
</div>

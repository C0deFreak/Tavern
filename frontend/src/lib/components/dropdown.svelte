<script>
  export let buttontext = "Edit";
  let isOpen = false; // State to control dropdown visibility

  function toggleDropdown() {
    isOpen = !isOpen;
  }
</script>

<div class="dropdown">
  <button on:click={toggleDropdown}>{buttontext}</button>
  {#if isOpen}
    <ul class="dropdown-menu">
      <slot></slot>
    </ul>
  {/if}
</div>

<style>
  .dropdown {
    position: relative;
    display: inline-block;
  }

  .dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    background: white;
    border: 1px solid #ccc;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    max-height: 200px; /* Set the maximum height */
    overflow-y: auto; /* Enable scrolling when content exceeds max height */
    width: 200px; /* Optional: set a fixed width */
    min-height: 50px;
    padding: 0;
    margin: 0;
    list-style: none;
  }

</style>

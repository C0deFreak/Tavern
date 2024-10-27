<!-- src/lib/Modal.svelte -->
<script>
    export let show = false;
</script>

{#if show}
    <div class="modal-backdrop"></div>
    <div class="modal">
        <div class="modal-content">
            <slot></slot>
        </div>
        <button class="close-button" on:click={() => show = !show}>Close</button>
    </div>
{/if}

<style>
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 10;
    }
    .modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        z-index: 11;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .close-button {
        background: none;
        border: none;
        cursor: pointer;
        margin-top: 10px;
        color: #333;
    }
</style>

<script lang="ts">
    import { onMount,useData, goto, getUser } from '$lib/libraries'
  
    let code = '';
  
    // Funkcija koja se poziva prilikom učitavanja komponente
    onMount(async() => {
      await getUser(true);  // Dobavljanje podataka o korisniku
    });
  
    // Funkcija koja preusmjerava korisnika na chat s odgovarajućim kodom
    async function redirectToRoom() {
      goto('/chat/' + code);
    }
  
    // Funkcija koja kreira novu chat sobu
    async function makeRoom() {
      const response = await useData('/chat/create', 'POST');
      if (response.ok) {
        const code = await response.json();  // Dohvaćanje koda nove sobe
        goto('/chat/' + code.code);  // Preusmjeravanje na novu chat sobu
      }
    }
  </script>
  
  <div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, darkolivegreen, #171717);">
    <!-- Polje za unos chat koda -->
    <input class="bg-neutral-600 rounded py-2 px-2" type="text" placeholder="Chat Code" bind:value={code}>
    
    <!-- Dugme za prijavu u chat s unesenim kodom -->
    <button class="px-4 py-2 bg-lime-700 text-xs rounded" on:click={redirectToRoom}>Submit</button>
  
    <!-- Dugme za kreiranje nove chat sobe -->
    <button class="px-4 py-2 bg-green-500 text-xs rounded" on:click={makeRoom}>Make room</button>
  </div>
  
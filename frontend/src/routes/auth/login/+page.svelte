<script>
  import { goto, hostStore } from '$lib/libraries'

  let email = '';
  let password = '';

  async function login() {
    const response = await fetch($hostStore + '/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      goto('/')
    } else {
      goto('/auth/login');
    }
  }

</script>

<div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, darkolivegreen, #171717);">
  <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="email" placeholder="E-Mail" bind:value={email}>
  <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="password" placeholder="Password" bind:value={password}>
  <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={login}>Log In</button>
</div>
<script>
    import { goto, hostStore } from '$lib/libraries'
  
    let name = 'user' + Math.floor(Math.random() * 10000);  // Generiranje nasumičnog korisničkog imena
    let email = '';
    let password = '';
    let password1 = '';
    let specialChars = /[`!#$%^&*()\+=\[\]{};':"\\|,<>\/?~ ]/  // RegEx za specijalne znakove
  
    // Funkcija za registraciju korisnika
    async function signup() {
  
      // Provjera da li se lozinke podudaraju
      if (password != password1) {
        alert('Passwords not matching');
      } 
      // Provjera duljine lozinke (mora biti između 8 i 30 znakova)
      else if (password.length < 8 || password.length > 30) {
        alert('Password is too long or short');
      } 
      // Provjera duljine korisničkog imena (mora biti između 4 i 50 znakova)
      else if (name.length < 4 || name.length > 50) {
        alert('Username is too long or short');
      } 
      // Provjera specijalnih znakova u korisničkom imenu
      else if (specialChars.test(name)) {
        alert('Username can not contain special characters');
      } 
      // Provjera ispravnosti emaila
      else if (email.length < 6 || !/@/.test(email) || !/./.test(email) || specialChars.test(email) || email.length > 50) {
        alert('E-Mail formatting is wrong');
      } 
      else {
        // Slanje podataka na server za kreiranje korisnika
        const response = await fetch($hostStore + '/auth/signup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',  // Čuvanje kolačića za autentifikaciju
          body: JSON.stringify({ email, name, password }),
        });
  
        // Ako je registracija uspješna, preusmjeravanje na početnu stranicu
        if (response.ok) {
          goto('/');
        } else {
          // Ako je registracija neuspješna, vraćamo korisnika na stranicu za registraciju
          alert('A problem occured while signing up');
        }
      }
    }
  </script>
  
  <div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, darkolivegreen, #171717);">
    <!-- Polje za unos E-Mail adrese -->
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="email" bind:value={email} placeholder="Email">
    
    <!-- Polje za unos korisničkog imena -->
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" bind:value={name} placeholder="Username">
    
    <!-- Polje za unos lozinke -->
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="password" bind:value={password} placeholder="Password">
    
    <!-- Polje za ponovno unos lozinke -->
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="password" bind:value={password1} placeholder="Retype password">
    
    <!-- Dugme za registraciju -->
    <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={signup}>Sign Up</button>
  </div>
  
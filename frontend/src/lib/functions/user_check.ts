import { goto, hostStore } from "$lib/libraries";

// Funkcija za dohvat informacija o korisniku
export async function getUser(redirect: boolean = false, adminCanEdit: boolean = false) {
    let host;
    
    // Pretplata na host promjenu
    hostStore.subscribe(value => {
        host = value;
    })();

    // Slanje zahtjeva za provjeru korisnika
    const user_info = await fetch(host + '/auth/user_check', {
        method: 'GET',
        credentials: 'include' // Uključuje kolačiće za autentifikaciju
    });

    // Ako je odgovor uspješan
    if (user_info.ok) {
        const data = await user_info.json();

        // Ako je korisnik administrator i može uređivati, vraća -1
        if (adminCanEdit && data.admin) {
            return -1;
        }

        // Ako je postavljen redirect, vraća ime korisnika, inače ID
        if (redirect) {
            return data.name;
        } else {
            return data.id;
        }
        
    } else {
        // Ako korisnik nije prijavljen, preusmjeri ga na login stranicu
        if (redirect) {
            goto('/auth/login');
        }     
        return null; // Ako nije uspješno, vraća null
    }
}

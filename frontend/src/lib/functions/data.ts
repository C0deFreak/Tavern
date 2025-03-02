import { hostStore } from "$lib/libraries";

// Funkcija koja koristi podatke sa servera
export function useData(url: string, data_method: string, body_data: any = null) {
    let host;
    
    // Pretplata na promjenu hosta u store-u
    hostStore.subscribe(value => {
        host = value;
    })();

    // Slanje zahtjeva na server s priloženim podacima
    return fetch(host + url, {
        method: data_method, // HTTP metoda (GET, POST, PUT, DELETE)
        body: body_data,     // Podaci tijela zahtjeva (ako postoje)
        credentials: 'include', // Uključivanje kolačića za autentifikaciju
    });
}

import { useData, goto } from "$lib/libraries";

// Tip podataka za informacije o audio sadržaju
export type AudioInfo = {
    id: number;
    name: string;
    author: string;
    genre: string;
    description: string;
    is_private: boolean;
    listens: number;
    user_id: number;
}

// Funkcija za učitavanje informacija o audio sadržaju prema ID-u
export async function loadInfo(id: string, name: string, check: string) {
    // Slanje zahtjeva za informacijama o audio sadržaju
    const response = await useData(check + id, 'GET');

    // Ako je odgovor sa servera uspješan
    if (response.ok) {
        const info = await response.json();

        // Ako je ime neprepoznatljivo, provjerava se ako odgovara očekivanom formatu
        if (name != '_ignorename' && name != info.name.replace(/\s+/g, '-')) {
            // Ako ime ne odgovara, preusmjeri na početnu stranicu
            goto('/');
        }
        return info;
    } else {
        // Ako nije pronađen odgovor, a ime nije '_ignorename', preusmjeri na početnu stranicu
        if (name == '_ignorename') {
            return null;
        } else {
            goto('/');
        }
    }
}

// Funkcija koja izvlači ime i ID iz URL putanje
export function extractNameAndIdFromPath(path: string, check: string) {
    // Prilagodba regularnog izraza za prepoznavanje imena i ID-a iz URL-a
    const match = path.match(new RegExp(`(.+)_${check}_(\\d+)$`));
    if (match) {
        return {
            name: match[1].slice(1), // Uklanja prvi znak (pretpostavlja da je to nepotreban prefiks)
            id: match[2]
        };
    }
    // Ako nije pronađen odgovarajući format, vraća 'Not Found'
    return { name: 'Not Found', id: 'Not Found' };
}

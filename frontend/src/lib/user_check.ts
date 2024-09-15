import { goto } from "$app/navigation";
import { hostStore } from "./stores";

export async function getUser() {
    let host;
    
    hostStore.subscribe(value => {
        host = value;
    })();

    const user_info = await fetch(host + '/auth/user', {
        method: 'GET',
        credentials: 'include'
    });

    if (user_info.ok) {
        const data = await user_info.json();
        return data.username;
    } else {
        goto('/auth/login');
        return null;
    }
}
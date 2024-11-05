import { goto } from "$app/navigation";
import { hostStore } from "$lib/stores/stores";

export async function getUser(redirect: boolean = false) {
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
        if (redirect) {
            return data.username;
        } else {
            return data.id;
        }
        
    } else {
        if (redirect) {
            goto('/auth/login');
        }     
        return null;
    }
}
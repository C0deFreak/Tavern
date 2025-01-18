import { goto, hostStore } from "$lib/libraries";

export async function getUser(redirect: boolean = false, adminCanEdit: boolean = false) {
    let host;
    
    hostStore.subscribe(value => {
        host = value;
    })();

    const user_info = await fetch(host + '/auth/user_check', {
        method: 'GET',
        credentials: 'include'
    });

    if (user_info.ok) {
        const data = await user_info.json();
        if (adminCanEdit && data.admin) {
            return -1
        }

        if (redirect) {
            return data.name;
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
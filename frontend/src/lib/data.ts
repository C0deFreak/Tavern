import { hostStore } from "./stores";
export function useData(url: string, data_method: string, body_data: any = null) {
    let host;
    
    hostStore.subscribe(value => {
        host = value;
    })();

    return fetch(host + url, {
        method: data_method,
        body: body_data,
        credentials: 'include',
    });
}

import { useData, goto } from "$lib/libraries";

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

export async function loadInfo(id: string, name: string, check: string) {
    const response = await useData(check + id, 'GET')

    if (response.ok) {
        const info = await response.json();
        // When checking and there is no name available so '_ignorename' is used as a default pass
        if (name != '_ignorename' && name != info.name.replace(/\s+/g, '-')) {
            goto('/');
        }
        return info;
    } else {
        if (name == '_ignorename') {
            return null;
        } else {
            goto('/');
        }   
    }
    
} 

export function extractNameAndIdFromPath(path: string, check: string) {
    // Adjust the regex to capture the name and ID from the URL
    const match = path.match(new RegExp(`(.+)_${check}_(\\d+)$`));
    if (match) {
        return {
            name: match[1].slice(1),
            id: match[2]
        };
    }
    return { name: 'Not Found', id: 'Not Found' };
}
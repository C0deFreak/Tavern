import { useData } from "./data";
import { goto } from "$app/navigation";

export type AudioInfo = {
    id: number;
    name: string;
    author: string;
    genre: string;
    description: string;

}

export async function loadInfo(id: string, name: string, check: string) {
    const response = await useData(check + id, 'GET')

    if (response.ok) {
        const info = await response.json();
        // When checking in playlists there is no name available so '_playlist' is used as a default pass
        if (name != '_playlist' && name != info.name.replace(/\s+/g, '-')) {
            goto('/');
        }
        return info;
    } else {
        if (name == '_playlist') {
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
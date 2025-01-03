<script lang="ts">
    import type { AudioInfo } from '$lib/functions/player';
    import { page, onMount, extractNameAndIdFromPath, loadInfo, getUser, useData } from '$lib/libraries'

    $: ({ name, id } = extractNameAndIdFromPath($page.url.pathname, "userid"));

    interface GetUser {
        id: number;
        name: string;
        audios: number[];
        playlists: number[];
        followed: number[];
        listens: number;
    }

    interface GetItem {
        id: number;
        name: string;
    }

    let userInfo: GetUser;
    let audioInfos: GetItem[] = [];
    let playlistInfos: GetItem[] = [];
    let followedInfos: GetItem[] = [];
    let currentUserId: number;

    async function loadAllInfo(ids: number[], type: string) {
        let infos;
        infos = await Promise.all(ids.map(id => loadInfo(id.toString(), '_ignorename', '/' + type + '/info/')));
        infos.sort((a, b) => parseFloat(a.id.toString()) - parseFloat(b.id.toString()));
        return infos
    }

    onMount(async() => {
        userInfo = await loadInfo(id, name, '/auth/info/');
        audioInfos = await loadAllInfo(userInfo.audios, 'audio');
        playlistInfos = await loadAllInfo(userInfo.playlists, 'playlist');
        followedInfos = await loadAllInfo(userInfo.followed, 'auth');
        currentUserId = await getUser();     
    });





</script>

{#if userInfo}
    <h1>{userInfo.name}</h1>
    <h4>Listens: {userInfo.listens} </h4>
    {#if currentUserId && currentUserId != userInfo.id}
        <button on:click={async () => await useData('/auth/follow/' + userInfo.id, 'POST')}>Follow</button>
    {/if}

    {#if audioInfos}
        <h2>Audios:</h2>
        {#each audioInfos as audio}
            <a href={`/${audio.name.replace(/\s+/g, '-')}_audioid_${audio.id}`}>
                <h3>{audio.name}</h3>
            </a>
        {/each}
    {/if}

    {#if playlistInfos}
        <h2>Playlists:</h2>
        {#each playlistInfos as playlist}
            <a href={`/${playlist.name.replace(/\s+/g, '-')}_playlistid_${playlist.id}`}>
                <h3>{playlist.name}</h3>
            </a>
        {/each}
    {/if}

    {#if followedInfos}
        <h2>Followed creators:</h2>
        {#each followedInfos as followed}
            <a href={`/${followed.name.replace(/\s+/g, '-')}_userid_${followed.id}`}>
                <h3>{followed.name}</h3>
            </a>
        {/each}
    {/if}
{/if}


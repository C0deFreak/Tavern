<script lang="ts">
    import { page, onMount, extractNameAndIdFromPath, loadInfo, getUser, useData } from '$lib/libraries'

    $: ({ name, id } = extractNameAndIdFromPath($page.url.pathname, "userid"));

    interface GetUser {
        id: number;
        name: string;
        audios: number[];
        playlists: number[];
        followed: number[];
        listens: number;
        followers: number;
        is_following: boolean;
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
    let randomColor = '';

    let followtext = 'Follow'

    async function loadAllInfo(ids: number[], type: string) {
        let infos;
        infos = await Promise.all(ids.map(id => loadInfo(id.toString(), '_ignorename', '/' + type + '/info/')));
        infos.sort((a, b) => parseFloat(a.id.toString()) - parseFloat(b.id.toString()));
        return infos
    }

    async function changeFollowState() {
        await useData('/auth/follow/' + userInfo.id, 'POST')
        location.reload()
    }

    onMount(async() => {
        userInfo = await loadInfo(id, name, '/auth/info/');
        audioInfos = await loadAllInfo(userInfo.audios, 'audio');
        playlistInfos = await loadAllInfo(userInfo.playlists, 'playlist');
        followedInfos = await loadAllInfo(userInfo.followed, 'auth');
        currentUserId = await getUser();
        if (userInfo.is_following) {
            followtext = 'Unfollow'
        }

        const allowedColors = [
        "red", "orange", "gold", "green",
        "teal", "blue", "indigo", "purple", "pink"
        ];

        // Pick a random color
        randomColor = allowedColors[Math.floor(Math.random() * allowedColors.length)];
    });


</script>

{#if userInfo}
    <div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, {randomColor}, #171717);">
        <h1 class=" text-8xl font-extrabold">{userInfo.name}</h1>
        <h4 class=" text-1xl font-normal">{userInfo.listens} listens ⦁ {userInfo.followers} followers</h4>
        {#if currentUserId && currentUserId != userInfo.id}
            <button class=" px-4 py-2 bg-green-500 rounded-2xl text-xs z-40" on:click={changeFollowState}>{followtext}</button>
        {/if}

        <br>
        <br>
        {#if audioInfos}
            <h2 class=" text-2xl">Audios:</h2>
            {#each audioInfos as audio}
                <a href={`/${audio.name.replace(/\s+/g, '-')}_audioid_${audio.id}`}>
                    <button class=" bg-neutral-700 py-1 px-2 border border-neutral-300 text-s mb-2">{audio.name}</button>
                </a>
            {/each}
        {/if}
        
        <br>
        <br>
        {#if playlistInfos}
            <h2 class=" text-2xl">Playlists:</h2>
            {#each playlistInfos as playlist}
                <a href={`/${playlist.name.replace(/\s+/g, '-')}_playlistid_${playlist.id}`}>
                    <button class=" bg-neutral-700 py-1 px-2 border border-neutral-300 text-s mb-2">{playlist.name}</button>
                </a>
            {/each}
        {/if}
        
        <br>
        <br>
        {#if followedInfos}
            <h2 class=" text-2xl">Followed creators:</h2>
            {#each followedInfos as followed}
                <a href={`/${followed.name.replace(/\s+/g, '-')}_userid_${followed.id}`}>
                    <button class=" bg-neutral-700 py-1 px-2 border border-neutral-300 text-s mb-2">{followed.name}</button>
                </a>
            {/each}
        {/if}
    </div>
{/if}


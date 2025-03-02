<script lang="ts">
    import { page, onMount, extractNameAndIdFromPath, loadInfo, getUser, useData } from '$lib/libraries'

    // Dohvaćanje imena i ID korisnika sa URL-a
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

    // Funkcija za učitavanje svih informacija (audio, playlisti, praćeni korisnici)
    async function loadAllInfo(ids: number[], type: string) {
        let infos;
        infos = await Promise.all(ids.map(id => loadInfo(id.toString(), '_ignorename', '/' + type + '/info/')));
        infos.sort((a, b) => parseFloat(a.id.toString()) - parseFloat(b.id.toString()));
        return infos
    }

    // Funkcija za promjenu statusa praćenja korisnika
    async function changeFollowState() {
        await useData('/auth/follow/' + userInfo.id, 'POST')
        location.reload() // Ponovno učitavanje stranice nakon promjene statusa
    }

    // Funkcija koja se poziva prilikom montiranja komponente
    onMount(async() => {
        userInfo = await loadInfo(id, name, '/auth/info/');
        audioInfos = await loadAllInfo(userInfo.audios, 'audio');
        playlistInfos = await loadAllInfo(userInfo.playlists, 'playlist');
        followedInfos = await loadAllInfo(userInfo.followed, 'auth');
        currentUserId = await getUser();
        if (userInfo.is_following) {
            followtext = 'Unfollow'
        }

        // Definiramo moguće boje koje će biti korištene u pozadini
        const allowedColors = [
        "red", "orange", "gold", "green",
        "teal", "blue", "indigo", "purple", "pink"
        ];

        // Odabiremo nasumičnu boju
        randomColor = allowedColors[Math.floor(Math.random() * allowedColors.length)];
    });
</script>

{#if userInfo}
    <div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, {randomColor}, #171717);">
        <!-- Prikaz imena korisnika -->
        <h1 class="text-8xl font-extrabold truncate w-400">{userInfo.name}</h1>
        <!-- Prikaz broja slušanja i broja pratitelja -->
        <h4 class="text-1xl font-normal">{userInfo.listens} listens ⦁ {userInfo.followers} followers</h4>
        
        <!-- Ako trenutni korisnik nije isti kao korisnik na profilu, omogućavamo praćenje/odpraćivanje -->
        {#if currentUserId && currentUserId != userInfo.id}
            <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs z-40" on:click={changeFollowState}>{followtext}</button>
        {/if}

        <br>
        <br>
        
        <!-- Prikaz audio fajlova korisnika -->
        {#if audioInfos}
            <h2 class="text-2xl">Audios:</h2>
            <div class="grid grid-cols-3 gap-2 max-h-60 overflow-y-auto w-150 py-3">
                {#each audioInfos as audio}
                    <div class="relative w-40 h-15 border border-neutral-300 bg-neutral-700 flex items-center justify-center rounded">
                        <!-- Cijeli pravokutnik je klikabilan -->
                        <a href={`/${audio.name.replace(/\s+/g, '-')}_audioid_${audio.id}`} class="absolute inset-0 z-0 flex items-center justify-center text-center">
                            <div class="z-10 text-white text-center px-1 truncate">{audio.name}</div>
                        </a>
                    </div>
                {/each}
            </div>
        {/if}
        
        <br>
        <br>
        
        <!-- Prikaz playlista korisnika -->
        {#if playlistInfos}
            <h2 class="text-2xl">Playlists:</h2>
            <div class="grid grid-cols-3 gap-2 max-h-60 overflow-y-auto w-150 py-3">  
                {#each playlistInfos as playlist}
                    <div class="relative w-40 h-15 border border-neutral-300 bg-neutral-700 flex items-center justify-center rounded">
                        <!-- Cijeli pravokutnik je klikabilan -->
                        <a href={`/${playlist.name.replace(/\s+/g, '-')}_playlistid_${playlist.id}`} class="absolute inset-0 z-0 flex items-center justify-center text-center">
                            <div class="z-10 text-white text-center px-1 truncate">{playlist.name}</div>
                        </a>
                    </div>
                {/each}
            </div>
        {/if}
        
        <br>
        <br>
        
        <!-- Prikaz korisnika koje prati -->
        {#if followedInfos}
            <h2 class="text-2xl">Followed creators:</h2>
            <div class="grid grid-cols-3 gap-2 max-h-60 overflow-y-auto w-150 py-3">               
                {#each followedInfos as followed}
                    <div class="relative w-40 h-15 border border-neutral-300 bg-neutral-700 flex items-center justify-center rounded">
                        <!-- Cijeli pravokutnik je klikabilan -->
                        <a href={`/${followed.name.replace(/\s+/g, '-')}_userid_${followed.id}`} class="absolute inset-0 z-0 flex items-center justify-center text-center">
                            <div class="z-10 text-white text-center px-1 truncate">{followed.name}</div>
                        </a>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
{/if}

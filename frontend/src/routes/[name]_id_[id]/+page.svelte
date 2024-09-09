<script>
    import { page } from '$app/stores';

    $: id = extractIdFromPath($page.url.pathname);

    function extractIdFromPath(path) {
        const match = path.match(/.*_id_(\d+)$/);
        return match ? match[1] : 'Not Found';
    }
</script>

<p>Current URL: {$page.url.pathname}</p>
<p>Extracted ID: {id}</p>


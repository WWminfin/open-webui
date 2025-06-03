<script lang="ts">
    import { toast } from 'svelte-sonner';
    import { onMount, getContext, createEventDispatcher } from 'svelte';

    import { getAzureStorageConfig, setAzureStorageConfig } from '$lib/apis/configs';
    import SensitiveInput from '$lib/components/common/SensitiveInput.svelte';
    const dispatch = createEventDispatcher();

    const i18n = getContext('i18n');

    let AzureStorageEndpoint = '';
    let AzureStorageContainer = '';
    let AzureStorageKey = '';

    const submitHandler = async () => {
        await setAzureStorageConfig(localStorage.token, {
            AZURE_STORAGE_ENDPOINT: AzureStorageEndpoint,
            AZURE_STORAGE_CONTAINER_NAME: AzureStorageContainer,
            AZURE_STORAGE_KEY: AzureStorageKey
        }).catch((err) => {
            toast.error(`${err}`);
        });

        dispatch('save');
    };

    onMount(async () => {
        const storageConfig = await getAzureStorageConfig(localStorage.token).catch((err) => {
            toast.error(`${err}`);
            return null;
        });
        if (storageConfig) {
            AzureStorageEndpoint = storageConfig.AZURE_STORAGE_ENDPOINT;
            AzureStorageContainer = storageConfig.AZURE_STORAGE_CONTAINER_NAME;
            AzureStorageKey = storageConfig.AZURE_STORAGE_KEY;
        }
    });
</script>

<form class="flex flex-col h-full justify-between space-y-3 text-sm" on:submit|preventDefault={() => submitHandler()}>
    <div class="space-y-2.5 overflow-y-scroll scrollbar-hidden h-full pr-1.5">
        <div class="mb-3">
            <div class="mb-2.5 text-base font-medium">{$i18n.t('Azure Storage')}</div>
            <hr class="border-gray-100 dark:border-gray-850 my-2" />
            <div class="mb-2.5 flex w-full justify-between">
                <div class="self-center text-xs font-medium">{$i18n.t('Azure Blob Endpoint')}</div>
                <div class="flex items-center relative">
                    <input
                        class="flex-1 w-full text-sm bg-transparent outline-hidden"
                        placeholder={$i18n.t('https://account.blob.core.windows.net')}
                        bind:value={AzureStorageEndpoint}
                        autocomplete="off"
                    />
                </div>
            </div>
            <div class="mb-2.5 flex w-full justify-between">
                <div class="self-center text-xs font-medium">{$i18n.t('Azure Blob Container')}</div>
                <div class="flex items-center relative">
                    <input
                        class="flex-1 w-full text-sm bg-transparent outline-hidden"
                        bind:value={AzureStorageContainer}
                        autocomplete="off"
                    />
                </div>
            </div>
            <div class="mb-2.5 flex w-full justify-between">
                <div class="self-center text-xs font-medium">{$i18n.t('Azure Blob Key')}</div>
                <div class="flex items-center relative">
                    <SensitiveInput
                        placeholder={$i18n.t('Shared Access Key')}
                        bind:value={AzureStorageKey}
                        required={false}
                    />
                </div>
            </div>
        </div>
    </div>
    <div class="flex justify-end pt-3 text-sm font-medium">
        <button class="px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full" type="submit">
            {$i18n.t('Save')}
        </button>
    </div>
</form>

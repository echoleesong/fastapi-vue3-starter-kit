import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/user'

export const useAppStore = defineStore('app', () => {
    // State
    const loading = ref(false)
    const sidebarCollapse = ref(false)

    // Getters
    const isLoading = computed(() => loading.value)
    const isSidebarCollapsed = computed(() => sidebarCollapse.value)

    // Actions
    function setLoading(value: boolean) {
        loading.value = value
    }

    function toggleSidebar() {
        sidebarCollapse.value = !sidebarCollapse.value
    }

    return {
        loading,
        sidebarCollapse,
        isLoading,
        isSidebarCollapsed,
        setLoading,
        toggleSidebar,
    }
})

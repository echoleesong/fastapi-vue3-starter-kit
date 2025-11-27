import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/user'
import { getUsers, createUser, updateUser, deleteUser } from '@/api/user'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', () => {
    // State
    const users = ref<User[]>([])
    const currentUser = ref<User | null>(null)
    const loading = ref(false)

    // Getters
    const userList = computed(() => users.value)
    const isLoading = computed(() => loading.value)

    // Actions
    async function fetchUsers(params?: { skip?: number; limit?: number }) {
        loading.value = true
        try {
            const data = await getUsers(params)
            users.value = data
        } catch (error) {
            console.error('Failed to fetch users:', error)
            ElMessage.error('获取用户列表失败')
        } finally {
            loading.value = false
        }
    }

    async function addUser(userData: { email: string; username: string; password: string; full_name?: string }) {
        loading.value = true
        try {
            const newUser = await createUser(userData)
            users.value.push(newUser)
            ElMessage.success('用户创建成功')
            return newUser
        } catch (error) {
            console.error('Failed to create user:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    async function modifyUser(id: number, userData: Partial<User>) {
        loading.value = true
        try {
            const updatedUser = await updateUser(id, userData)
            const index = users.value.findIndex((u) => u.id === id)
            if (index !== -1) {
                users.value[index] = updatedUser
            }
            ElMessage.success('用户更新成功')
            return updatedUser
        } catch (error) {
            console.error('Failed to update user:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    async function removeUser(id: number) {
        loading.value = true
        try {
            await deleteUser(id)
            users.value = users.value.filter((u) => u.id !== id)
            ElMessage.success('用户删除成功')
        } catch (error) {
            console.error('Failed to delete user:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    return {
        users,
        currentUser,
        loading,
        userList,
        isLoading,
        fetchUsers,
        addUser,
        modifyUser,
        removeUser,
    }
})

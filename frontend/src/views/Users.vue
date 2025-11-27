<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">用户管理</h1>
          <p class="text-gray-600 mt-2">管理系统用户信息</p>
        </div>
        <el-button type="primary" size="large" @click="showCreateDialog">
          <span class="mr-2">+</span> 创建用户
        </el-button>
      </div>

      <!-- Users Table -->
      <el-card shadow="never">
        <el-table 
          :data="userStore.userList" 
          :loading="userStore.isLoading"
          stripe
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="username" label="用户名" min-width="120" />
          <el-table-column prop="email" label="邮箱" min-width="200" />
          <el-table-column prop="full_name" label="全名" min-width="120">
            <template #default="{ row }">
              {{ row.full_name || '-' }}
            </template>
          </el-table-column>
          <el-table-column prop="is_active" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
                {{ row.is_active ? '激活' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="is_superuser" label="超级用户" width="100">
            <template #default="{ row }">
              <el-tag :type="row.is_superuser ? 'warning' : 'info'" size="small">
                {{ row.is_superuser ? '是' : '否' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column fixed="right" label="操作" width="150">
            <template #default="{ row }">
              <el-button link type="primary" size="small" @click="handleEdit(row)">
                编辑
              </el-button>
              <el-button link type="danger" size="small" @click="handleDelete(row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- Create/Edit Dialog -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="500px"
        @close="resetForm"
      >
        <el-form
          ref="formRef"
          :model="formData"
          :rules="formRules"
          label-width="100px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="formData.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="formData.email" placeholder="请输入邮箱" type="email" />
          </el-form-item>
          <el-form-item label="全名" prop="full_name">
            <el-input v-model="formData.full_name" placeholder="请输入全名（可选）" />
          </el-form-item>
          <el-form-item v-if="!editMode" label="密码" prop="password">
            <el-input
              v-model="formData.password"
              type="password"
              placeholder="请输入密码"
              show-password
            />
          </el-form-item>
          <el-form-item v-if="editMode" label="新密码" prop="password">
            <el-input
              v-model="formData.password"
              type="password"
              placeholder="不修改请留空"
              show-password
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="userStore.isLoading">
            {{ editMode ? '更新' : '创建' }}
          </el-button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'
import type { User } from '@/types/user'

const userStore = useUserStore()

// Dialog state
const dialogVisible = ref(false)
const editMode = ref(false)
const currentEditId = ref<number | null>(null)

// Form
const formRef = ref<FormInstance>()
const formData = reactive({
  username: '',
  email: '',
  full_name: '',
  password: '',
})

const formRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在 3 到 50 个字符', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
  ],
  password: [
    {
      validator: (rule, value, callback) => {
        if (!editMode.value && !value) {
          callback(new Error('请输入密码'))
        } else if (value && value.length < 8) {
          callback(new Error('密码长度至少 8 个字符'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

const dialogTitle = ref('创建用户')

// Methods
const showCreateDialog = () => {
  editMode.value = false
  dialogTitle.value = '创建用户'
  dialogVisible.value = true
}

const handleEdit = (row: User) => {
  editMode.value = true
  currentEditId.value = row.id
  dialogTitle.value = '编辑用户'

  formData.username = row.username
  formData.email = row.email
  formData.full_name = row.full_name || ''
  formData.password = ''

  dialogVisible.value = true
}

const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${row.username}" 吗？此操作不可恢复。`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    await userStore.removeUser(row.id)
  } catch (error) {
    // User cancelled or error occurred
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      if (editMode.value && currentEditId.value) {
        // Update user
        const updateData: any = {
          username: formData.username,
          email: formData.email,
          full_name: formData.full_name || null,
        }
        if (formData.password) {
          updateData.password = formData.password
        }
        await userStore.modifyUser(currentEditId.value, updateData)
      } else {
        // Create user
        await userStore.addUser({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          full_name: formData.full_name || undefined,
        })
      }
      dialogVisible.value = false
      resetForm()
    } catch (error) {
      // Error handled in store
    }
  })
}

const resetForm = () => {
  formData.username = ''
  formData.email = ''
  formData.full_name = ''
  formData.password = ''
  currentEditId.value = null
  formRef.value?.resetFields()
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

// Load users on mount
onMounted(() => {
  userStore.fetchUsers()
})
</script>

<style scoped>
.el-table {
  border-radius: 8px;
}
</style>

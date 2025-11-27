import request from './request'
import type { User, UserCreate, UserUpdate } from '@/types/user'

/**
 * 获取用户列表
 */
export function getUsers(params?: { skip?: number; limit?: number }): Promise<User[]> {
    return request({
        url: '/api/v1/users',
        method: 'get',
        params,
    })
}

/**
 * 获取用户详情
 */
export function getUser(id: number): Promise<User> {
    return request({
        url: `/api/v1/users/${id}`,
        method: 'get',
    })
}

/**
 * 创建用户
 */
export function createUser(data: UserCreate): Promise<User> {
    return request({
        url: '/api/v1/users',
        method: 'post',
        data,
    })
}

/**
 * 更新用户
 */
export function updateUser(id: number, data: UserUpdate): Promise<User> {
    return request({
        url: `/api/v1/users/${id}`,
        method: 'put',
        data,
    })
}

/**
 * 删除用户
 */
export function deleteUser(id: number): Promise<void> {
    return request({
        url: `/api/v1/users/${id}`,
        method: 'delete',
    })
}

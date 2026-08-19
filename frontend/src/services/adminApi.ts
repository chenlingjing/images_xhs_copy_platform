import type { AdminOverview, User, AdminGenerationRecord, DailyStats } from '@/types'

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

const MOCK_USERS: User[] = [
  {
    id: 'user-1',
    username: '小鹿种草',
    email: 'xiaolu@example.com',
    role: 'user',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=xiaolu',
    createdAt: '2026-07-15T08:30:00.000Z',
    lastActiveAt: '2026-08-10T09:12:00.000Z'
  },
  {
    id: 'user-2',
    username: '美妆阿姐',
    email: 'meizhuang@example.com',
    role: 'user',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=meizhuang',
    createdAt: '2026-07-18T14:22:00.000Z',
    lastActiveAt: '2026-08-09T21:45:00.000Z'
  },
  {
    id: 'user-3',
    username: '数码评测君',
    email: 'digital@example.com',
    role: 'user',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=digital',
    createdAt: '2026-07-20T11:05:00.000Z',
    lastActiveAt: '2026-08-10T07:30:00.000Z'
  },
  {
    id: 'user-4',
    username: '旅行日记',
    email: 'travel@example.com',
    role: 'user',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=travel',
    createdAt: '2026-07-22T16:40:00.000Z',
    lastActiveAt: '2026-08-08T19:20:00.000Z'
  },
  {
    id: 'admin-1',
    username: 'admin',
    email: 'admin@example.com',
    role: 'admin',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=admin',
    createdAt: '2026-01-01T00:00:00.000Z',
    lastActiveAt: '2026-08-10T10:00:00.000Z'
  }
]

const MOCK_GENERATIONS: AdminGenerationRecord[] = [
  {
    id: 'gen-101',
    imageUrl: 'https://images.unsplash.com/photo-1541658016709-82535e94bc69?w=400&h=400&fit=crop',
    params: {
      imageUrl: 'https://images.unsplash.com/photo-1541658016709-82535e94bc69?w=400&h=400&fit=crop',
      productName: '丝绒奶茶',
      toneStyle: '活泼'
    },
    result: {
      id: 'gen-101',
      title: '✨ 这杯奶茶也太治愈了吧！下午茶首选就是它',
      content: '姐妹们！今天挖到一家宝藏奶茶店...',
      tags: ['#奶茶推荐', '#下午茶', '#治愈系']
    },
    status: 'success',
    createdAt: '2026-08-10T09:30:00.000Z',
    user: { id: 'user-1', username: '小鹿种草', avatar: MOCK_USERS[0].avatar }
  },
  {
    id: 'gen-102',
    imageUrl: 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop',
    params: {
      imageUrl: 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop',
      productName: '口红礼盒',
      toneStyle: '温柔'
    },
    result: {
      id: 'gen-102',
      title: '🌸 这支口红涂上去就是温柔本人',
      content: '今天试了一支新口红，质地丝滑不拔干...',
      tags: ['#口红试色', '#温柔妆', '#美妆']
    },
    status: 'success',
    createdAt: '2026-08-10T08:45:00.000Z',
    user: { id: 'user-2', username: '美妆阿姐', avatar: MOCK_USERS[1].avatar }
  },
  {
    id: 'gen-103',
    imageUrl: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop',
    params: {
      imageUrl: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop',
      productName: '无线耳机',
      toneStyle: '专业'
    },
    result: null,
    status: 'failed',
    errorMessage: '模型调用超时，请稍后重试',
    createdAt: '2026-08-09T22:10:00.000Z',
    user: { id: 'user-3', username: '数码评测君', avatar: MOCK_USERS[2].avatar }
  },
  {
    id: 'gen-104',
    imageUrl: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=400&fit=crop',
    params: {
      imageUrl: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=400&fit=crop',
      targetAudience: '旅行爱好者',
      toneStyle: '治愈'
    },
    result: {
      id: 'gen-104',
      title: '🍃 海边的风，把烦恼都吹走了',
      content: '周末去了一趟海边，阳光、沙滩、浪花...',
      tags: ['#海边', '#旅行', '#治愈']
    },
    status: 'success',
    createdAt: '2026-08-09T18:20:00.000Z',
    user: { id: 'user-4', username: '旅行日记', avatar: MOCK_USERS[3].avatar }
  }
]

function generateDailyStats(days: number): DailyStats[] {
  const stats: DailyStats[] = []
  const today = new Date()
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)
    const total = Math.floor(Math.random() * 80) + 20
    const failed = Math.floor(Math.random() * 5)
    stats.push({
      date: date.toISOString().slice(0, 10),
      totalGenerations: total,
      successCount: total - failed,
      failedCount: failed,
      uniqueUsers: Math.floor(Math.random() * 10) + 1
    })
  }
  return stats
}

export async function getAdminOverview(): Promise<AdminOverview> {
  await sleep(600)
  const dailyStats = generateDailyStats(14)
  const totalGenerations = dailyStats.reduce((sum, d) => sum + d.totalGenerations, 0)
  const successCount = dailyStats.reduce((sum, d) => sum + d.successCount, 0)

  return {
    totalUsers: MOCK_USERS.filter(u => u.role === 'user').length,
    totalGenerations,
    todayGenerations: dailyStats[dailyStats.length - 1].totalGenerations,
    successRate: totalGenerations > 0 ? Math.round((successCount / totalGenerations) * 100) : 0,
    avgGenerationTimeMs: 3200 + Math.floor(Math.random() * 800),
    dailyStats
  }
}

export async function getUsers(): Promise<User[]> {
  await sleep(500)
  return [...MOCK_USERS].sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
}

export async function getGenerations(): Promise<AdminGenerationRecord[]> {
  await sleep(500)
  return [...MOCK_GENERATIONS].sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
}

export async function deleteGeneration(id: string): Promise<void> {
  await sleep(400)
  const index = MOCK_GENERATIONS.findIndex(g => g.id === id)
  if (index !== -1) {
    MOCK_GENERATIONS.splice(index, 1)
  }
}

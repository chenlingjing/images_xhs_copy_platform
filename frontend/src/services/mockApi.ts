import type { GenerationParams, GenerationResult, MockUploadResponse } from '@/types'

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

const MOCK_RESULTS: Record<string, GenerationResult> = {
  default: {
    id: 'mock-1',
    title: '✨ 这杯奶茶也太治愈了吧！下午茶首选就是它',
    content: `姐妹们！今天挖到一家宝藏奶茶店，颜值和口感都戳中我的心巴 💗\n\n一拿到手就被这杯分层美到了，奶盖厚厚的像云朵一样，底下茶底清清爽爽。第一口先喝到绵密奶盖，然后是茶香和奶香交织，完全不会腻～\n\n我最喜欢的是它的甜度刚刚好，少糖党也能放心冲！下午三点来一杯，打工人的疲惫瞬间被治愈了 ☁️\n\n拍照也超出片，随手一拍就是小红书爆款感。建议姐妹们选窗边位置，自然光下颜色更通透！`,
    tags: ['#奶茶推荐', '#下午茶', '#治愈系', '#探店', '#生活方式']
  },
  温柔: {
    id: 'mock-2',
    title: '🌸 午后的温柔，藏在这一杯里',
    content: `阳光洒进窗边的午后，最适合来一杯这样温柔的奶茶。\n\n奶盖像初雪一样轻盈，茶底带着淡淡的花香，每一口都像在亲吻春天。没有过分的甜，只剩下恰到好处的回甘，让人忍不住想闭上眼睛慢慢品味。\n\n如果你也喜欢慢节奏的生活，不妨给自己这样一个小小仪式感。生活再忙，也要记得温柔以待自己呀 🕯️`,
    tags: ['#温柔日常', '#奶茶', '#治愈', '#慢生活', '#下午茶']
  },
  专业: {
    id: 'mock-3',
    title: '成分党看过来｜这杯奶茶为什么值得喝',
    content: `作为一个严格控糖又爱喝奶茶的人，这杯真的让我愿意写测评。\n\n茶底选用的是原叶茶而非茶粉，奶盖用的是动物奶油，入口能明显感受到质地差异：奶盖绵密厚重，茶底干净不涩，整体风味层次分明。甜度方面，少糖版本对胰岛素敏感度友好。\n\n从拍摄角度看，分层结构在侧光下非常明显，适合俯拍或45度角拍摄。综合口感、原料和出片率，推荐指数 4.5/5。`,
    tags: ['#奶茶测评', '#成分党', '#健康饮食', '#探店', '#理性种草']
  },
  搞笑: {
    id: 'mock-4',
    title: '喝了一口，我的打工魂原地复活',
    content: `救命！这杯奶茶是来给打工人续命的吧？\n\n我原本困得像被吸干了阳气，结果一口下去，奶盖糊嘴的瞬间我仿佛听见了天堂的钟声 🔥 甜而不腻，茶不苦涩，连吸管都吸得格外顺畅，简直是打工生涯的高光时刻！\n\n老板：你下午怎么笑得这么开心？\n我：没什么，只是和我的续命水双向奔赴了。`,
    tags: ['#打工人日常', '#奶茶续命', '#搞笑', '#办公室', '#快乐水']
  },
  治愈: {
    id: 'mock-5',
    title: '🍃 把坏心情泡进这杯茶里，就化了',
    content: `今天有点累，所以决定奖励自己一杯奶茶。\n\n拿到它的时候，刚好外面在下小雨，店里放着轻音乐，奶盖在杯壁上慢慢滑落，像时间也跟着慢了下来。喝一口，温热的茶从喉咙滑到胃里，整个人都松了下来。\n\n其实幸福有时候真的很简单，一杯喜欢的饮料，一个安静的角落，就足以把坏情绪慢慢融化。希望你也有这样的时刻 🌿`,
    tags: ['#治愈系', '#奶茶', '#情绪价值', '#独处时光', '#温暖']
  }
}

export async function uploadImage(file: File): Promise<MockUploadResponse> {
  await sleep(1200)

  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    throw new Error('图片格式不支持，请上传 jpg / png / webp / gif 格式的图片')
  }

  if (file.size > 10 * 1024 * 1024) {
    throw new Error('图片大小超过 10MB，请压缩后重试')
  }

  return {
    url: URL.createObjectURL(file)
  }
}

export async function uploadImageFromUrl(url: string): Promise<MockUploadResponse> {
  await sleep(800)

  if (!url.trim()) {
    throw new Error('请输入图片链接')
  }

  if (!/^https?:\/\/.+\.(jpg|jpeg|png|webp|gif)(\?.*)?$/i.test(url) && !url.includes('unsplash')) {
    // 宽松处理：允许任意 http 链接，但给出提示风险
    console.warn('URL 可能不是标准图片地址，将尝试加载')
  }

  return { url: url.trim() }
}

export async function generateCopy(params: GenerationParams): Promise<GenerationResult> {
  await sleep(2500)

  // 模拟随机失败（5% 概率）
  if (Math.random() < 0.05) {
    throw new Error('模型调用超时，请稍后重试')
  }

  const tone = params.toneStyle || 'default'
  const base = MOCK_RESULTS[tone] || MOCK_RESULTS.default

  return {
    ...base,
    id: `gen-${Date.now()}`,
    title: params.productName ? `${base.title} · ${params.productName}` : base.title
  }
}

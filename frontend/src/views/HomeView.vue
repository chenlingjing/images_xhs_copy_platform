<template>
  <AppLayout>
    <!-- Hero -->
    <section class="relative bg-white overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 sm:pt-16 lg:pt-20 pb-16 sm:pb-20 lg:pb-28">
        <div class="text-center max-w-4xl mx-auto">
          <!-- Announcement banner -->
          <RouterLink
            to="/workspace/history"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-red-50 border border-red-100 text-xhs-red text-sm font-medium mb-8 hover:bg-red-100 transition-colors"
          >
            <span class="px-2 py-0.5 rounded-full bg-xhs-red text-white text-xs">新功能</span>
            <span>历史记录已上线，随时回溯你的生成内容</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </RouterLink>

          <h1 class="text-4xl sm:text-5xl lg:text-7xl font-serif font-medium text-gray-900 leading-[1.1] mb-6 tracking-tight">
            让 AI 为你的小红书<br class="hidden sm:block">写出爆款种草文案
          </h1>
          <p class="text-lg sm:text-xl text-gray-500 mb-10 max-w-2xl mx-auto leading-relaxed">
            上传任意图片，AI 自动识别场景、产品与氛围，一键生成符合小红书风格的标题、正文与话题标签。从灵感到发布，只需几分钟。
          </p>

          <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
            <RouterLink
              to="/register"
              class="btn-primary text-lg px-8 py-4 rounded-2xl shadow-lg shadow-red-200"
            >
              免费开始使用
              <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </RouterLink>
            <a
              href="#example"
              class="inline-flex items-center justify-center px-8 py-4 rounded-2xl text-lg font-medium text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 hover:text-gray-900 transition-colors"
            >
              查看效果示例
            </a>
          </div>

          <p class="text-sm text-gray-400">无需信用卡 · 支持 jpg / png / webp</p>
        </div>
      </div>

      <!-- Hero visual -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16 sm:pb-20">
        <HeroVisual
          :image-url="exampleImage"
          :result="exampleResult"
        />
      </div>
    </section>

    <!-- Trust strip -->
    <section class="bg-xhs-bg border-y border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div>
            <p class="text-3xl font-bold text-gray-900">10,000+</p>
            <p class="text-sm text-gray-500 mt-1">文案已生成</p>
          </div>
          <div>
            <p class="text-3xl font-bold text-gray-900">3 分钟</p>
            <p class="text-sm text-gray-500 mt-1">平均产出时间</p>
          </div>
          <div>
            <p class="text-3xl font-bold text-gray-900">98%</p>
            <p class="text-sm text-gray-500 mt-1">生成成功率</p>
          </div>
          <div>
            <p class="text-3xl font-bold text-gray-900">5+</p>
            <p class="text-sm text-gray-500 mt-1">语气风格可选</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section
      id="features"
      class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28 scroll-mt-24"
    >
      <div class="text-center max-w-2xl mx-auto mb-14">
        <p class="text-sm font-semibold text-xhs-red uppercase tracking-wider mb-3">功能亮点</p>
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">从图片到发布，一步到位</h2>
        <p class="text-gray-500">无需学习复杂提示词，像发小红书一样简单</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
        <FeatureCard
          v-for="feature in features"
          :key="feature.title"
          :icon="feature.icon"
          :title="feature.title"
          :description="feature.description"
        />
      </div>
    </section>

    <!-- Example -->
    <section
      id="example"
      class="bg-white py-20 lg:py-28 border-y border-gray-100 scroll-mt-24"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          <div>
            <p class="text-sm font-semibold text-xhs-red uppercase tracking-wider mb-3">效果示例</p>
            <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-6">生成的文案，<br>就像你亲手写的一样</h2>
            <p class="text-gray-500 mb-8 leading-relaxed text-lg">
              结果以原生小红书笔记卡片呈现，标题、正文、话题标签分区清晰。你可以一键复制全文，或单独复制标题、正文、标签，直接发布到小红书。
            </p>
            <ul class="space-y-4 mb-8">
              <li class="flex items-start gap-3">
                <div class="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <span class="text-gray-700">20 字以内爆款标题，自动匹配 emoji</span>
              </li>
              <li class="flex items-start gap-3">
                <div class="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <span class="text-gray-700">200-400 字种草正文，分段清晰自然</span>
              </li>
              <li class="flex items-start gap-3">
                <div class="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <span class="text-gray-700">3-5 个精准话题标签，提升曝光</span>
              </li>
            </ul>
            <RouterLink
              to="/workspace"
              class="btn-primary px-6 py-3"
            >
              立即体验
            </RouterLink>
          </div>
          <div class="lg:pl-8">
            <XhsCard :result="exampleResult" />
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section
      id="faq"
      class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28 scroll-mt-24"
    >
      <div class="text-center mb-12">
        <p class="text-sm font-semibold text-xhs-red uppercase tracking-wider mb-3">常见问题</p>
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">还有疑问？</h2>
        <p class="text-gray-500">关于使用、数据与安全的常见疑问</p>
      </div>
      <div class="space-y-4">
        <FaqItem
          v-for="(item, index) in faqs"
          :key="index"
          :question="item.question"
          :answer="item.answer"
        />
      </div>
    </section>

    <!-- CTA -->
    <section class="bg-xhs-red py-16 lg:py-24">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">准备好提升你的创作效率了吗？</h2>
        <p class="text-red-100 mb-8 text-lg">现在上传图片，3 分钟内获得第一篇小红书文案。</p>
        <RouterLink
          to="/register"
          class="inline-flex items-center justify-center px-8 py-4 rounded-2xl bg-white text-xhs-red font-bold text-lg shadow-lg hover:bg-red-50 transition-colors"
        >
          免费创建账号
          <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </RouterLink>
      </div>
    </section>
  </AppLayout>
</template>

<script setup lang="ts">
import AppLayout from '@/components/AppLayout.vue'
import HeroVisual from '@/components/HeroVisual.vue'
import XhsCard from '@/components/XhsCard.vue'
import FeatureCard from '@/components/FeatureCard.vue'
import FaqItem from '@/components/FaqItem.vue'

const exampleImage = 'https://images.unsplash.com/photo-1541658016709-82535e94bc69?w=600&h=600&fit=crop'

const exampleResult = {
  id: 'example-1',
  title: '✨ 这杯奶茶也太治愈了吧！下午茶首选就是它',
  content: `姐妹们！今天挖到一家宝藏奶茶店，颜值和口感都戳中我的心巴 💗\n\n一拿到手就被这杯分层美到了，奶盖厚厚的像云朵一样，底下茶底清清爽爽。第一口先喝到绵密奶盖，然后是茶香和奶香交织，完全不会腻～\n\n我最喜欢的是它的甜度刚刚好，少糖党也能放心冲！下午三点来一杯，打工人的疲惫瞬间被治愈了 ☁️\n\n拍照也超出片，随手一拍就是小红书爆款感。建议姐妹们选窗边位置，自然光下颜色更通透！`,
  tags: ['#奶茶推荐', '#下午茶', '#治愈系', '#探店', '#生活方式']
}

const features = [
  {
    icon: 'upload',
    title: '图片一键上传',
    description: '支持本地上传拖拽或图片 URL，自动校验格式与大小，秒级预览。'
  },
  {
    icon: 'sparkles',
    title: 'AI 智能识别',
    description: '多模态模型识别图片主体、场景、氛围与卖点，为文案生成提供上下文。'
  },
  {
    icon: 'copy',
    title: '即生即用',
    description: '生成结果以小红书笔记卡片呈现，支持一键复制全文或单独复制标题、正文、标签。'
  }
]

const faqs = [
  {
    question: '这个平台需要付费吗？',
    answer: '当前版本为学习交流用途，不接入支付与订阅功能，所有功能均可免费体验。'
  },
  {
    question: '生成的文案可以直接发布到小红书吗？',
    answer: '可以。生成的文案已按照小红书风格排版，你可以一键复制后粘贴到小红书发布。建议根据实际情况微调。'
  },
  {
    question: '支持哪些图片格式？',
    answer: '目前支持 jpg、png、webp、gif 格式，单张图片大小不超过 10MB。'
  },
  {
    question: '我的图片和数据会被保存吗？',
    answer: '当前为前端演示版本，图片仅在本地预览，不会上传到服务器。历史记录保存在浏览器本地存储中，仅供当前账号查看。'
  }
]
</script>

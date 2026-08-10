export async function copyText(text: string): Promise<void> {
  if (!text) return

  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text)
    return
  }

  // Fallback for older browsers / non-secure contexts
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.style.position = 'fixed'
  textarea.style.left = '-9999px'
  textarea.style.top = '-9999px'
  document.body.appendChild(textarea)
  textarea.focus()
  textarea.select()

  try {
    const successful = document.execCommand('copy')
    if (!successful) {
      throw new Error('Copy command failed')
    }
  } finally {
    textarea.remove()
  }
}

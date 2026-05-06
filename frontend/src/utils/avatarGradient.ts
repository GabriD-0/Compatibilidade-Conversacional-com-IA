const AVATAR_GRADIENTS = [
  'linear-gradient(135deg, #5adb94, #0ba18c)',
  'linear-gradient(135deg, #c0345e, #6d0080)',
  'linear-gradient(135deg, #7c3aed, #4f46e5)',
  'linear-gradient(135deg, #0ea5e9, #0891b2)',
  'linear-gradient(135deg, #f59e0b, #ef4444)',
  'linear-gradient(135deg, #ec4899, #8b5cf6)',
]

export function avatarGradient(name: string): string {
  return AVATAR_GRADIENTS[name.charCodeAt(0) % AVATAR_GRADIENTS.length]!
}

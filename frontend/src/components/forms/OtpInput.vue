<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'

const props = withDefaults(
  defineProps<{
    modelValue?: string
    digits?: number
    disabled?: boolean
  }>(),
  {
    modelValue: '',
    digits: 6,
    disabled: false
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'complete', value: string): void
}>()

const otpDigits = ref<string[]>(Array(props.digits).fill(''))
const inputRefs = ref<HTMLInputElement[]>([])

// Sync props.modelValue to otpDigits
watch(
  () => props.modelValue,
  (val) => {
    const chars = (val || '').slice(0, props.digits).split('')
    otpDigits.value = Array.from({ length: props.digits }, (_, i) => chars[i] || '')
  },
  { immediate: true }
)

const handleInput = (index: number, event: Event) => {
  const input = event.target as HTMLInputElement
  let val = input.value

  // Keep only numbers
  val = val.replace(/\D/g, '')

  if (val.length > 1) {
    val = val.charAt(val.length - 1)
  }

  otpDigits.value[index] = val
  emitValue()

  if (val && index < props.digits - 1) {
    nextTick(() => {
      inputRefs.value[index + 1]?.focus()
    })
  }
}

const handleKeyDown = (index: number, event: KeyboardEvent) => {
  if (event.key === 'Backspace') {
    if (!otpDigits.value[index] && index > 0) {
      // Focus previous input on backspace if current field is empty
      inputRefs.value[index - 1]?.focus()
    }
  } else if (event.key === 'ArrowLeft' && index > 0) {
    inputRefs.value[index - 1]?.focus()
  } else if (event.key === 'ArrowRight' && index < props.digits - 1) {
    inputRefs.value[index + 1]?.focus()
  }
}

const handlePaste = (event: ClipboardEvent) => {
  event.preventDefault()
  const pastedData = event.clipboardData?.getData('text') || ''
  const cleanNumbers = pastedData.replace(/\D/g, '').slice(0, props.digits)

  if (cleanNumbers.length > 0) {
    const chars = cleanNumbers.split('')
    otpDigits.value = Array.from({ length: props.digits }, (_, i) => chars[i] || '')
    emitValue()

    const lastFilledIndex = Math.min(cleanNumbers.length, props.digits) - 1
    nextTick(() => {
      inputRefs.value[Math.max(0, lastFilledIndex)]?.focus()
    })
  }
}

const emitValue = () => {
  const result = otpDigits.value.join('')
  emit('update:modelValue', result)
  if (result.length === props.digits) {
    emit('complete', result)
  }
}
</script>

<template>
  <div class="otp-container" @paste="handlePaste">
    <div class="otp-input-wrapper">
      <div
        v-for="(_, index) in digits"
        :key="index"
        class="otp-box-slot"
        :class="{ 'has-value': !!otpDigits[index] }"
      >
        <input
          :ref="(el) => (inputRefs[index] = el as HTMLInputElement)"
          type="text"
          inputmode="numeric"
          pattern="[0-9]*"
          maxlength="1"
          :value="otpDigits[index]"
          :disabled="disabled"
          placeholder="0"
          class="otp-digit-input"
          @input="handleInput(index, $event)"
          @keydown="handleKeyDown(index, $event)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.otp-container {
  width: 100%;
}

.otp-input-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 12px;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  transition: all 0.2s ease;
}

.otp-input-wrapper:focus-within {
  border-color: #0d9488;
  background-color: #ffffff;
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.12);
}

.otp-box-slot {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.otp-digit-input {
  width: 100%;
  max-width: 44px;
  height: 48px;
  text-align: center;
  font-family: var(--font-family);
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
  background: transparent;
  border: none;
  outline: none;
  caret-color: #0d9488;
  transition: all 0.15s ease;
}

.otp-digit-input::placeholder {
  color: #cbd5e1;
  font-weight: 400;
}

.otp-digit-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>

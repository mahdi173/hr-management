<template>
  <div class="app-logo" :style="{ gap: `${gap}px` }">
    <!-- Icon mark -->
    <svg
      :width="iconSize"
      :height="iconSize"
      viewBox="0 0 44 44"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      class="app-logo__icon"
    >
      <defs>
        <linearGradient id="logoGradA" x1="0" y1="0" x2="44" y2="44" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#4F46E5"/>
          <stop offset="100%" stop-color="#7C3AED"/>
        </linearGradient>
        <filter id="logoShadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#4F46E5" flood-opacity="0.35"/>
        </filter>
      </defs>

      <!-- Background rounded square -->
      <rect width="44" height="44" rx="12" fill="url(#logoGradA)" filter="url(#logoShadow)"/>

      <!-- Outer ring (clock) -->
      <circle cx="22" cy="22" r="12" stroke="rgba(255,255,255,0.25)" stroke-width="1.5" fill="none"/>

      <!-- Inner filled arc – progress ring (270°) -->
      <path
        d="M22 10 A12 12 0 1 1 10 22"
        stroke="rgba(255,255,255,0.5)"
        stroke-width="1.5"
        stroke-linecap="round"
        fill="none"
      />

      <!-- Hour hand – pointing to 10 -->
      <line
        x1="22" y1="22"
        x2="16.2" y2="16.2"
        stroke="white"
        stroke-width="2.2"
        stroke-linecap="round"
      />

      <!-- Minute hand – pointing to 2 (slightly right of 12) -->
      <line
        x1="22" y1="22"
        x2="27" y2="14.5"
        stroke="white"
        stroke-width="1.6"
        stroke-linecap="round"
      />

      <!-- Center dot -->
      <circle cx="22" cy="22" r="2" fill="white"/>

      <!-- Small tick at 12 o'clock -->
      <line x1="22" y1="11" x2="22" y2="14" stroke="white" stroke-width="1.8" stroke-linecap="round" opacity="0.8"/>

      <!-- Checkmark badge (bottom-right) -->
      <circle cx="33" cy="33" r="7" fill="#10B981"/>
      <path
        d="M30 33.2 L32.2 35.5 L36.2 30.8"
        stroke="white"
        stroke-width="1.8"
        stroke-linecap="round"
        stroke-linejoin="round"
        fill="none"
      />
    </svg>

    <!-- Wordmark -->
    <span v-if="showText" class="app-logo__text" :style="{ fontSize: `${fontSize}px`, color: textColor }">
      <span class="app-logo__time">Time</span><span class="app-logo__app">App</span>
    </span>
  </div>
</template>

<script setup>
defineProps({
  iconSize: { type: Number, default: 36 },
  fontSize: { type: Number, default: 20 },
  gap: { type: Number, default: 10 },
  showText: { type: Boolean, default: true },
  textColor: { type: String, default: '#09090B' },
})
</script>

<style scoped>
.app-logo {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  flex-shrink: 0;
}
.app-logo__icon {
  flex-shrink: 0;
  transition: transform 0.3s ease;
}
.app-logo:hover .app-logo__icon {
  transform: rotate(-8deg) scale(1.05);
}
.app-logo__text {
  font-family: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1;
  white-space: nowrap;
}
.app-logo__time {
  color: inherit;
}
.app-logo__app {
  color: #4F46E5;
}
</style>

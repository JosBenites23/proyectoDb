import animations from '@midudev/tailwind-animations'

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{astro,html,js,jsx,ts,tsx}', 
    './public/**/*.html'
  ],
  theme: {
    extend: {
      animation: animations.animation,
      keyframes: animations.keyframes
    }
  },
  plugins: [],
}


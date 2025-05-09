import animations from '@midudev/tailwind-animations';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./dist/**/*.{astro,html,js,jsx,ts,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [animations],
}


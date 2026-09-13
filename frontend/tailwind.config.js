/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        navy: {
          50:  '#e8eef5',
          100: '#c5d3e6',
          200: '#9fb5d4',
          300: '#6d8eb8',
          400: '#3d6497',
          500: '#0C2340',
          600: '#0a1e38',
          700: '#081830',
          800: '#061228',
          900: '#040c1c',
        },
        usred: {
          50:  '#fdeaed',
          100: '#f9c4cb',
          200: '#f49aa7',
          300: '#ee6d7d',
          400: '#e84357',
          500: '#D8273F',
          600: '#b31f35',
          700: '#8c182a',
          800: '#651120',
          900: '#3e0a14',
        },
      },
      animation: {
        'fade-in':    'fadeIn 0.4s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          from: { opacity: '0', transform: 'translateY(8px)' },
          to:   { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          from: { maxHeight: '0', opacity: '0' },
          to:   { maxHeight: '9999px', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}

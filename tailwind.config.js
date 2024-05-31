/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html'
  ],
  theme: {

    extend: {
      colors: {
        'border-light': '#e6e6e680',
        'brand': '#2563eb',
        'brand-hover': '#1d4ed8',
        // 'brand': '#9333ea',
        // 'brand-hover': '#7e22ce',
        // 'brand': colors.blue,
      },

      fontFamily: {
        'poppins': ['Poppins'],
        'handlee': ['Handlee'],
        'pangolin': ['Pangolin'],
     }
    },
  },
  plugins: [],
}


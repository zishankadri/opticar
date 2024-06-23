/** @type {import('tailwindcss').Config} */
module.exports = {
  // darkMode: 'media',
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html',
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {

    extend: {
      colors: {
        'border-light': '#e6e6e680',
        'brand': '#2563eb',
        'brand-light': '#60a5fa',
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
  plugins: [
    require('flowbite/plugin')
]
}


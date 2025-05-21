// theme/static_src/tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../../blog/templates//*.html',
    '../../../templates//*.html',
    '../..//*.py',
    '../static_src/src//*.js',
    '../static_src/src//*.css',
  ],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
}
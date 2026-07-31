/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        soc: {
          bg: '#0B1220',
          card: '#131D2E',
          card2: '#0F1828',
          border: '#1E2A40',
          primary: '#2563EB',
          accent: '#06B6D4',
          danger: '#EF4444',
          warning: '#F59E0B',
          success: '#22C55E',
        },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
      boxShadow: {
        glow: '0 0 20px rgba(37, 99, 235, 0.35)',
        'glow-cyan': '0 0 24px rgba(6, 182, 212, 0.4)',
        'glow-danger': '0 0 24px rgba(239, 68, 68, 0.45)',
        card: '0 8px 30px rgba(0, 0, 0, 0.35)',
      },
      keyframes: {
        'spin-slow': { to: { transform: 'rotate(360deg)' } },
        'spin-rev': { to: { transform: 'rotate(-360deg)' } },
        pulse2: { '0%,100%': { opacity: '0.5' }, '50%': { opacity: '1' } },
        float: { '0%,100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-8px)' } },
        dash: { to: { 'stroke-dashoffset': '0' } },
        shimmer: { '100%': { transform: 'translateX(100%)' } },
        scan: { '0%': { transform: 'translateY(-100%)' }, '100%': { transform: 'translateY(100%)' } },
      },
      animation: {
        'spin-slow': 'spin-slow 12s linear infinite',
        'spin-rev': 'spin-rev 16s linear infinite',
        pulse2: 'pulse2 2.4s ease-in-out infinite',
        float: 'float 6s ease-in-out infinite',
        shimmer: 'shimmer 1.6s infinite',
        scan: 'scan 3s linear infinite',
      },
    },
  },
  plugins: [],
};

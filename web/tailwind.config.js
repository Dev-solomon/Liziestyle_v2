/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./*.html', './src/**/*.js'],
	theme: {
		extend: {
			colors: {
				primary: {
					DEFAULT: '#F5FDFF',
					100: '#C5F0FD',
					200: '#98E2F9',
					300: '#70D4F2',
					400: '#50C6E9',
					500: '#38B7DD',
					600: '#27A6CD',
					700: '#1B93B8',
					800: '#137FA0',
					900: '#0E6B87',
				},
				secondary: {
					DEFAULT: '#F5FAFF',
					100: '#E8F1FB',
					200: '#D8E6F3',
					300: '#C7D7E7',
					400: '#B3C4D5',
					500: '#9BACBD',
					600: '#7F8E9D',
					700: '#5E6A75',
					800: '#384047',
					900: '#121517',
				},
			},
		},
	},
	plugins: [],
	
}

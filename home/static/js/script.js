(() => {
	const shell = document.querySelector('.theme-shell');
	const toggle = document.querySelector('[data-theme-toggle]');
	const icon = document.querySelector('[data-theme-icon]');

	if (!shell || !toggle) {
		return;
	}

	const setTheme = (theme) => {
		const isDark = theme === 'dark';
		shell.classList.toggle('dark-theme', isDark);
		document.documentElement.dataset.theme = theme;
		icon.textContent = isDark ? '☀' : '☾';
		toggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
		toggle.setAttribute('title', isDark ? 'Switch to light mode' : 'Switch to dark mode');
	};

	const savedTheme = localStorage.getItem('arkan-theme');
	setTheme(savedTheme === 'dark' ? 'dark' : 'light');

	toggle.addEventListener('click', () => {
		const nextTheme = shell.classList.contains('dark-theme') ? 'light' : 'dark';
		localStorage.setItem('arkan-theme', nextTheme);
		setTheme(nextTheme);
	});

	document.querySelectorAll('[data-numeric-only]').forEach((input) => {
		input.addEventListener('input', () => {
			input.value = input.value.replace(/\D/g, '').slice(0, 10);
		});
	});
})();

document.addEventListener('DOMContentLoaded', () => {
    const html = document.documentElement;
    const btn = document.getElementById('theme-toggle-btn');
    const icon = document.getElementById('mode-icon');

    // Function to update theme
    function updateTheme(isDark) {
        if (isDark) {
            html.classList.add('dark');
            if (icon) icon.textContent = '☀️';
            localStorage.setItem('theme', 'dark');
        } else {
            html.classList.remove('dark');
            if (icon) icon.textContent = '🌙';
            localStorage.setItem('theme', 'light');
        }
    }

    // Initialize theme from saved value or OS preference
    const saved = localStorage.getItem('theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (saved === 'dark' || (!saved && prefersDark)) {
        updateTheme(true);
    } else {
        updateTheme(false);
    }

    // Toggle handler
    if (btn) {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const isCurrentlyDark = html.classList.contains('dark');
            updateTheme(!isCurrentlyDark);
        });
    }

    // Listen for system theme changes
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                updateTheme(e.matches);
            }
        });
    }
});

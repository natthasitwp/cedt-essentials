(() => {
  try { const theme = localStorage.getItem('cedt-demo-theme'); if(theme) document.documentElement.dataset.theme = theme; } catch {}
  document.getElementById('demo-theme')?.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme === 'dark';
    const theme = dark ? 'light' : 'dark'; document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('cedt-demo-theme', theme); } catch {}
  });
  document.getElementById('demo-reset')?.addEventListener('click', () => {
    try { Object.keys(localStorage).filter(k => k.startsWith('cedt-demo-') && k !== 'cedt-demo-theme').forEach(k => localStorage.removeItem(k)); location.reload(); } catch { alert('เบราว์เซอร์ไม่อนุญาตให้ล้างข้อมูล'); }
  });
})();
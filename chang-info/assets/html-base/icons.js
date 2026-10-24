// 라인 아이콘 (24x24, stroke). <span class="ic" data-ic="cpu"></span> 형태로 사용
const ICONS = {
  cpu:'<rect x="6" y="6" width="12" height="12" rx="1"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
  threads:'<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="18" r="2.5"/><circle cx="12" cy="19" r="2.5"/><circle cx="19" cy="18" r="2.5"/><path d="M12 7.5v9M10.5 7l-4.5 9M13.5 7l4.5 9"/>',
  layers:'<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/><path d="M3 17.5l9 5 9-5"/>',
  warn:'<path d="M12 3l10 18H2L12 3z"/><path d="M12 10v5M12 18v.5"/>',
  bang:'<path d="M12 6v8M12 18v.5"/>',
  target:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
  doc:'<path d="M6 2h9l4 4v16H6z"/><path d="M9 10h7M9 14h7M9 18h5"/>',
  search:'<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/>',
  chart:'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
  gear:'<circle cx="12" cy="12" r="3.5"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
  sync:'<path d="M20 8a8 8 0 0 0-14.5-2M4 4v4h4"/><path d="M4 16a8 8 0 0 0 14.5 2M20 20v-4h-4"/>',
  check:'<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.8 2.8L16.5 9"/>',
  clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
  game:'<rect x="2" y="7" width="20" height="11" rx="5"/><path d="M7 10.5v4M5 12.5h4"/><circle cx="16" cy="11.5" r="1"/><circle cx="18" cy="14" r="1"/>',
  car:'<path d="M3 16v-3l2.5-5h13L21 13v3z"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M5.5 12h13"/>',
  arm:'<circle cx="6" cy="19" r="2"/><path d="M6 17l4-8 6 3"/><circle cx="10" cy="9" r="1.6"/><path d="M16 12l3-3M16 12l3 2"/><path d="M3 22h7"/>',
  maze:'<rect x="3" y="3" width="18" height="18"/><path d="M3 9h12M9 15h12M9 9v6M15 3v6"/>',
  scale:'<path d="M12 3v18M5 21h14M4 8h16"/><path d="M4 8l-2.5 6a3 3 0 0 0 5 0L4 8zM20 8l-2.5 6a3 3 0 0 0 5 0L20 8z"/>',
  noreplay:'<rect x="4" y="6" width="16" height="12" rx="2"/><path d="M8 10h8M8 14h5"/><path d="M3 3l18 18"/>',
  brain:'<circle cx="5" cy="6" r="1.8"/><circle cx="5" cy="12" r="1.8"/><circle cx="5" cy="18" r="1.8"/><circle cx="12" cy="9" r="1.8"/><circle cx="12" cy="15" r="1.8"/><circle cx="19" cy="12" r="1.8"/><path d="M6.7 6.6l3.6 1.8M6.7 12l3.6-2.4M6.7 12l3.6 2.4M6.7 17.4l3.6-1.8M13.7 9.6l3.6 1.8M13.7 14.4l3.6-1.8"/>',
  dice:'<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8" cy="8" r="1"/><circle cx="16" cy="16" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="16" cy="8" r="1"/><circle cx="8" cy="16" r="1"/>',
  speed:'<path d="M4 18a9 9 0 1 1 16 0"/><path d="M12 14l5-5"/>',
  medal:'<circle cx="12" cy="15" r="6"/><path d="M8 3l4 6 4-6"/><path d="M12 12.5v5"/>'
};
document.querySelectorAll('[data-ic]').forEach(el=>{
  el.innerHTML='<svg viewBox="0 0 24 24">'+ICONS[el.dataset.ic]+'</svg>';
});

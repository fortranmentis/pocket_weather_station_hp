(() => {
  'use strict';
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const motion = () => reducedMotion.matches ? 'instant' : 'smooth';

  const menu = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#main-nav');
  const closeMenu = () => {
    menu.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
  };
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menu.focus();
    }
  });

  const tabs = [...document.querySelectorAll('[role="tab"]')];
  function selectTab(tab, focus = false) {
    tabs.forEach(item => {
      const active = item === tab;
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !active;
    });
    if (focus) tab.focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectTab(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) {
        event.preventDefault();
        selectTab(tabs[next], true);
      }
    });
  });

  const track = document.querySelector('.gallery-track');
  const cards = [...track.querySelectorAll('.gallery-card')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const count = document.querySelector('.gallery-count');
  const scrollButtons = [...document.querySelectorAll('[data-scroll]')];
  function updateArrows() {
    scrollButtons[0].disabled = track.scrollLeft <= 2;
    scrollButtons[1].disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 2;
  }
  filters.forEach(button => button.addEventListener('click', () => {
    const group = button.dataset.filter;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    cards.forEach(card => { card.hidden = group !== '0' && card.dataset.group !== group; });
    count.textContent = `${cards.filter(card => !card.hidden).length} ${count.dataset.countSuffix}`;
    track.scrollTo({ left: 0, behavior: 'instant' });
    updateArrows();
  }));
  scrollButtons.forEach(button => button.addEventListener('click', () => {
    track.scrollBy({ left: track.clientWidth * 0.8 * Number(button.dataset.scroll), behavior: motion() });
  }));
  track.addEventListener('scroll', updateArrows, { passive: true });
  window.addEventListener('resize', updateArrows, { passive: true });
  window.addEventListener('load', updateArrows, { once: true });
  updateArrows();

  const catalog = JSON.parse(document.querySelector('#screenshot-catalog').textContent);
  const dialog = document.querySelector('.screenshot-dialog');
  const dialogImage = dialog.querySelector('.dialog-image');
  const zoomButton = dialog.querySelector('.dialog-zoom');
  const assetPrefix = document.body.dataset.assetPrefix;
  let current = 0;
  let opener;
  function displayImage(index) {
    current = (index + catalog.length) % catalog.length;
    const screen = catalog[current];
    dialog.classList.remove('is-zoomed');
    zoomButton.setAttribute('aria-pressed', 'false');
    dialog.scrollTop = 0;
    dialogImage.src = `${assetPrefix}assets/screenshots/${screen.id}.jpg`;
    dialogImage.alt = screen.title;
    dialog.querySelector('#dialog-title').textContent = screen.title;
    dialog.querySelector('#dialog-position').textContent = `${String(current + 1).padStart(2, '0')} / ${catalog.length}`;
    dialog.querySelector('#dialog-description').textContent = screen.body;
  }
  document.querySelectorAll('[data-screen]').forEach(button => {
    button.addEventListener('click', () => {
      const index = catalog.findIndex(screen => screen.id === button.dataset.screen);
      if (index < 0) return;
      opener = button;
      displayImage(index);
      dialog.showModal();
      document.body.classList.add('dialog-open');
      dialog.querySelector('.dialog-close').focus();
    });
  });
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  zoomButton.addEventListener('click', () => {
    const zoomed = dialog.classList.toggle('is-zoomed');
    zoomButton.setAttribute('aria-pressed', String(zoomed));
    dialog.scrollTop = 0;
  });
  dialog.querySelector('.dialog-prev').addEventListener('click', () => displayImage(current - 1));
  dialog.querySelector('.dialog-next').addEventListener('click', () => displayImage(current + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      displayImage(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('dialog-open');
    opener?.focus({ preventScroll: true });
  });

  // Keep the section when changing language, without replacing native links.
  document.querySelectorAll('a[hreflang]').forEach(link => {
    link.addEventListener('click', () => {
      const destination = new URL(link.href);
      destination.hash = window.location.hash;
      link.href = destination.href;
    });
  });
})();

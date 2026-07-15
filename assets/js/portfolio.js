(() => {
  const list = document.querySelector('#algorithm-list');
  if (!list) return;

  const items = [...list.querySelectorAll('li')];
  const search = document.querySelector('#algorithm-search');
  const tag = document.querySelector('#algorithm-tag');
  const status = document.querySelector('#algorithm-status');
  const pagination = document.querySelector('#algorithm-pagination');
  const platformButtons = [...document.querySelectorAll('[data-platform]')];
  const pageSize = 20;
  let platform = 'all';
  let page = 1;

  const normalize = (value) => value.trim().toLocaleLowerCase();

  function render() {
    const query = normalize(search.value);
    const selectedTag = tag.value;
    const matches = items.filter((item) => {
      const titleMatches = !query || item.dataset.title.includes(query);
      const platformMatches = platform === 'all' || item.dataset.platform === platform;
      const tags = item.dataset.tags.split('|');
      const tagMatches = selectedTag === 'all' || tags.includes(selectedTag);
      return titleMatches && platformMatches && tagMatches;
    });

    const pages = Math.max(1, Math.ceil(matches.length / pageSize));
    page = Math.min(page, pages);
    const visible = new Set(matches.slice((page - 1) * pageSize, page * pageSize));
    items.forEach((item) => { item.hidden = !visible.has(item); });
    status.textContent = `${matches.length}개 풀이${matches.length ? ` · ${page} / ${pages} 페이지` : ''}`;
    pagination.replaceChildren();

    if (pages > 1) {
      const start = Math.max(1, page - 2);
      const end = Math.min(pages, start + 4);
      for (let number = start; number <= end; number += 1) {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = number;
        button.className = number === page ? 'active' : '';
        button.setAttribute('aria-label', `${number}페이지`);
        if (number === page) button.setAttribute('aria-current', 'page');
        button.addEventListener('click', () => { page = number; render(); list.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
        pagination.append(button);
      }
    }
  }

  search.addEventListener('input', () => { page = 1; render(); });
  tag.addEventListener('change', () => { page = 1; render(); });
  platformButtons.forEach((button) => button.addEventListener('click', () => {
    platform = button.dataset.platform;
    platformButtons.forEach((candidate) => candidate.classList.toggle('active', candidate === button));
    page = 1;
    render();
  }));
  render();
})();

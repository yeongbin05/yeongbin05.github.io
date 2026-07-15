---
title: Algorithm
icon: fas fa-code
order: 4
---

{% assign algorithm_posts = site.posts | where_exp: 'post', 'post.categories contains "Algorithm"' %}
<div class="tab-intro"><p class="eyebrow">Problem archive</p><h1>Algorithm</h1><p>BOJ와 LeetCode 문제 풀이를 검색하고 주제별로 탐색할 수 있습니다.</p></div>

<div class="algorithm-tools" aria-label="알고리즘 목록 필터">
  <label class="algorithm-search"><span class="visually-hidden">문제 번호 또는 제목 검색</span><i class="fas fa-search" aria-hidden="true"></i><input id="algorithm-search" type="search" placeholder="문제 번호 또는 제목 검색" autocomplete="off"></label>
  <div class="filter-row" role="group" aria-label="플랫폼 필터"><button class="filter-button active" type="button" data-platform="all">전체</button><button class="filter-button" type="button" data-platform="boj">BOJ</button><button class="filter-button" type="button" data-platform="leetcode">LeetCode</button></div>
  <label class="tag-select">태그 <select id="algorithm-tag"><option value="all">전체 태그</option>{% assign all_tags = algorithm_posts | map: 'tags' | join: ',' | split: ',' | uniq | sort %}{% for tag in all_tags %}{% assign clean_tag = tag | strip %}{% if clean_tag != empty %}<option value="{{ clean_tag | downcase | escape }}">{{ clean_tag }}</option>{% endif %}{% endfor %}</select></label>
</div>

<p id="algorithm-status" class="algorithm-status" aria-live="polite"></p>
<ul id="algorithm-list" class="algorithm-list">
  {% for post in algorithm_posts %}
    {% assign platform = post.categories[1] | downcase %}
    <li data-title="{{ post.title | downcase | escape }}" data-platform="{{ platform }}" data-tags="{{ post.tags | join: '|' | downcase | escape }}">
      <a href="{{ post.url | relative_url }}"><span class="platform-badge {{ platform }}">{{ post.categories[1] }}</span><span class="algorithm-title">{{ post.title }}</span><span class="algorithm-tags">{% for tag in post.tags limit: 3 %}<span>{{ tag }}</span>{% endfor %}</span><span aria-hidden="true">→</span></a>
    </li>
  {% endfor %}
</ul>
<nav id="algorithm-pagination" class="algorithm-pagination" aria-label="알고리즘 목록 페이지"></nav>
<noscript><p class="empty-state">검색과 필터를 사용하려면 JavaScript를 활성화해 주세요. 전체 목록은 아래에 표시됩니다.</p></noscript>
<script src="{{ '/assets/js/portfolio.js' | relative_url }}" defer></script>

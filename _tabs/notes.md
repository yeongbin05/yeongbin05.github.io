---
title: Notes
icon: fas fa-book
order: 3
---

{% assign cs_posts = site.posts | where_exp: 'post', 'post.categories contains "CS"' %}
{% assign note_groups = cs_posts | group_by_exp: 'post', 'post.categories[1]' | sort: 'name' %}

<div class="tab-intro"><p class="eyebrow">Knowledge base</p><h1>CS Notes</h1><p>컴퓨터 과학과 백엔드 기반 지식을 주제별로 정리합니다.</p></div>
<div class="notes-groups">
  {% for group in note_groups %}
    <section class="notes-group" aria-labelledby="notes-{{ group.name | slugify }}">
      <div class="notes-heading"><h2 id="notes-{{ group.name | slugify }}">{{ group.name }}</h2><span>{{ group.items.size }} notes</span></div>
      <ul>{% for post in group.items %}<li><a href="{{ post.url | relative_url }}"><span>{{ post.title }}</span><span aria-hidden="true">→</span></a></li>{% endfor %}</ul>
    </section>
  {% endfor %}
</div>

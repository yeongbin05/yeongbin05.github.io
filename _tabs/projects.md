---
title: Projects
icon: fas fa-briefcase
order: 1
---

{% assign project_posts = site.posts | where_exp: 'post', 'post.categories contains "Projects"' %}

<div class="tab-intro">
  <p class="eyebrow">Selected work</p>
  <h1>Projects</h1>
  <p>서비스의 구조를 설계하고 백엔드를 구현한 프로젝트입니다.</p>
</div>

<div class="project-grid project-page-grid">
  {% for post in project_posts %}
    <a class="project-card" href="{{ post.url | relative_url }}">
      {% assign image_path = post.image.path | default: post.image %}
      <div class="project-media"><img src="{{ image_path | relative_url }}" alt="{{ post.image.alt | default: post.title | escape }}"></div>
      <div class="project-body"><h2>{{ post.title }}</h2><p>{{ post.description }}</p><ul class="tech-list" aria-label="핵심 기술">{% for tag in post.tags limit: 6 %}<li>{{ tag }}</li>{% endfor %}</ul></div>
    </a>
  {% endfor %}
</div>

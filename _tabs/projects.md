---
title: Projects
icon: fas fa-briefcase
order: 1
---

{% assign project_posts = site.posts | where_exp: 'post', 'post.categories contains "Projects"' %}

<div class="tab-intro">
  <p class="eyebrow">주요 작업 · {{ project_posts.size }}개 프로젝트</p>
  <p>서비스의 구조를 설계하고 백엔드를 구현한 프로젝트입니다.</p>
</div>

<div class="project-grid project-page-grid">
  {% for post in project_posts %}
    {% include project-card.html post=post %}
  {% endfor %}
</div>

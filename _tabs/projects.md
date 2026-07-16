---
title: Projects
icon: fas fa-briefcase
order: 1
---

{% assign stockq_post = site.posts | where: 'slug', 'stockq' | first %}
{% assign xbench_post = site.posts | where: 'slug', 'django-xbench' | first %}
{% assign ving_post = site.posts | where: 'slug', 'ving-streaming' | first %}
{% assign mozzi_post = site.posts | where: 'slug', 'mozzi-recommendation' | first %}
{% assign featured_projects = '' | split: '' | push: stockq_post | push: xbench_post %}
{% assign previous_projects = '' | split: '' | push: ving_post | push: mozzi_post %}

<div class="tab-intro">
  <p class="eyebrow">주요 작업 · {{ featured_projects.size }}개 프로젝트</p>
  <p>성능 병목을 측정하고 비동기 작업의 신뢰성을 설계한 대표 프로젝트입니다.</p>
</div>

<section class="projects-section" aria-labelledby="featured-projects-title">
  <h2 id="featured-projects-title">주요 프로젝트</h2>
  <div class="project-grid project-page-grid featured-project-grid">
    {% if stockq_post %}{% include project-card.html post=stockq_post featured=true %}{% endif %}
    {% if xbench_post %}{% include project-card.html post=xbench_post featured=true %}{% endif %}
  </div>
</section>

<section class="projects-section previous-projects" id="previous-projects" aria-labelledby="previous-projects-title">
  <div class="projects-section-heading"><h2 id="previous-projects-title">이전 프로젝트</h2><span>{{ previous_projects.size }}개 프로젝트</span></div>
  <div class="project-grid project-page-grid">
    {% for post in previous_projects %}{% include project-card.html post=post %}{% endfor %}
  </div>
</section>

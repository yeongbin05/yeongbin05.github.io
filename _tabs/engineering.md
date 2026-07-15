---
title: Engineering
icon: fas fa-microchip
order: 2
---

{% assign engineering_posts = '' | split: '' %}
{% for post in site.posts %}
  {% unless post.categories contains 'Algorithm' or post.categories contains 'CS' or post.categories contains 'Projects' %}
    {% assign engineering_posts = engineering_posts | push: post %}
  {% endunless %}
{% endfor %}

<div class="tab-intro"><p class="eyebrow">문제 해결 기록</p><p>시스템을 만들며 마주한 문제와 측정, 개선 과정을 기록합니다.</p></div>
{% if engineering_posts.size > 0 %}
  <div class="document-list">{% for post in engineering_posts %}<a href="{{ post.url | relative_url }}"><span>{{ post.title }}</span><span aria-hidden="true">→</span></a>{% endfor %}</div>
{% endif %}

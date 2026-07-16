---
# the default layout is 'page'
icon: fas fa-info-circle
title: About
order: 5
---

<p class="about-lead">요청이 느리다는 감각에서 멈추지 않고, DB 쿼리·애플리케이션 로직·외부 API 구간을 측정해 병목의 원인을 추적하고 개선하는 백엔드 개발자 김영빈입니다.</p>

미국 주식 뉴스 서비스 StockQ에서는 OpenAI API 호출을 사용자 요청 경로에서 분리한 Celery 비동기 파이프라인을 설계했습니다. DB row lock, lease token, stuck job recovery를 적용해 중복 실행을 방지하고 멈춘 작업을 다시 처리할 수 있도록 구성했습니다. 또한 N+1과 serializer 병목을 분석해 API 응답 시간을 1750ms에서 37ms로, 쿼리 수를 1001개에서 1개로 개선했습니다.

개발 과정에서 반복적으로 겪은 성능 분석 문제를 해결하기 위해 Django 요청의 total·db·app 시간을 분리하는 오픈소스 라이브러리 django-xbench를 개발해 PyPI에 배포했습니다. GitHub에서 30+ stars를 얻었으며, Django 공동 창시자 Simon Willison으로부터 in-memory 통계 집계 방식에 대한 긍정적인 피드백을 받았습니다.

기능 구현에 그치지 않고 측정 가능한 근거를 바탕으로 성능과 신뢰성을 개선하며, 운영 가능한 백엔드 시스템을 만드는 것을 목표로 합니다.

## 핵심 역량

- **성능 병목 분석**: DB 쿼리, serializer와 애플리케이션 로직을 구분해 측정하고 N+1과 응답 크기 병목을 개선합니다.
- **비동기 작업 파이프라인**: Celery와 Redis를 기반으로 외부 API 호출을 요청 경로에서 분리하고 처리량을 제어합니다.
- **작업 신뢰성과 복구**: 작업 상태, DB row lock, lease token, stuck job recovery로 중복 실행과 중단 상황을 다룹니다.
- **Django 오픈소스 개발**: 재사용 가능한 middleware를 설계하고 테스트해 PyPI package로 배포합니다.

## 대표 프로젝트

- [StockQ]({{ '/posts/stockq/' | relative_url }}) — AI 주식 뉴스 요약 비동기 백엔드
- [django-xbench]({{ '/posts/django-xbench/' | relative_url }}) — Django 요청 시간 분석 오픈소스 라이브러리

## 기술 스택

- Backend: Python, Django, Django REST Framework
- Data & Async: PostgreSQL, Redis, Celery
- Performance: Django Middleware, Server-Timing, Prometheus, Grafana
- Infra: Docker Compose, Nginx, Gunicorn, AWS EC2, GitHub Actions

## 교육

SSAFY(삼성 소프트웨어 아카데미)에서 Django 기반 프로젝트를 수행하며 AWS, Git, Notion을 활용한 협업 경험을 쌓았습니다.

## 어학

| 시험 | 성적 |
| --- | --- |
| TOEIC | 915 |
| TOEIC Speaking | AL |
| JLPT | 1급 |
| JPT | 825 |

## 연락처

- Email: <bigstar96115@hanmail.net>
- GitHub: [github.com/yeongbin05](https://github.com/yeongbin05)

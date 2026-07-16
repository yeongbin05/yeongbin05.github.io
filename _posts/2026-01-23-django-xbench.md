---
title: django-xbench
date: 2026-01-23 22:15:47 +0900
categories: [Projects, Open Source]
tags: [python, django, middleware, performance, profiling, server-timing]
description: 무거운 APM 없이 Django 요청의 전체·DB·애플리케이션 시간을 분리하고 느린 엔드포인트를 집계하는 경량 성능 분석 도구입니다.
---

## 프로젝트 개요

django-xbench는 Django 요청의 전체 처리 시간, DB 실행 시간, 애플리케이션 시간을 분리해 보여주는 1인 개발 오픈소스 라이브러리입니다. 별도 agent나 SaaS 없이 middleware 하나로 요청 구간과 쿼리 수를 확인할 수 있도록 만들었습니다.

- GitHub: [yeongbin05/django-xbench](https://github.com/yeongbin05/django-xbench)
- PyPI: [django-xbench](https://pypi.org/project/django-xbench/)
- 배포 현황: PyPI Published · 30+ stars

## 개발 배경

Django API가 느릴 때 전체 응답 시간만으로는 원인이 SQL인지, serializer와 Python 로직인지 빠르게 구분하기 어렵습니다. 개발 환경에서 병목을 확인하기 위해 무거운 외부 APM을 먼저 구성하는 것도 부담이었습니다.

반복해서 겪은 이 문제를 줄이기 위해 Django middleware와 `connection.execute_wrapper`를 이용해 요청 단위 측정값을 수집하고, 브라우저 개발자 도구와 응답 헤더에서 바로 확인할 수 있는 도구를 만들었습니다.

## 측정 구조

요청 시간은 다음 세 구간으로 나눕니다.

- `total`: middleware가 측정한 전체 요청 시간
- `db`: Django DB wrapper에서 누적한 쿼리 실행 시간
- `app`: `max(0, total - db)`로 계산한 애플리케이션 구간

DB 쿼리 수도 함께 집계해 느린 요청이 많은 쿼리에서 비롯됐는지 확인할 수 있습니다. `app`에는 serializer, template, Python 로직 등 DB 밖에서 수행된 시간이 포함됩니다.

## Server-Timing 활용

측정 결과는 표준 `Server-Timing` 헤더와 `X-Bench-Queries` 헤더로 노출합니다.

```text
Server-Timing: xbench-total;dur=52.300, xbench-db;dur=14.100, xbench-app;dur=38.200
X-Bench-Queries: 5
```

Chrome 등 Server-Timing을 지원하는 브라우저의 Network 패널에서 별도 UI 없이 요청 구간을 확인할 수 있습니다.

## Slow Endpoint Aggregation

선택적으로 최근 요청을 process memory에 집계해 느린 endpoint를 찾을 수 있습니다. 요청별 total, DB 비율, 평균 쿼리 수와 누적 지연 시간을 기준으로 endpoint를 비교하며 JSON snapshot과 간단한 HTML dashboard를 제공합니다.

이 기능은 외부 저장소 없이 개발 환경에서 빠르게 확인하기 위한 실험적 기능입니다. 여러 worker를 사용하면 각 process가 독립된 window를 가지므로 분산 환경 전체를 집계하는 APM을 대체하지는 않습니다.

## 사용 예시

PyPI에서 패키지를 설치합니다.

```bash
pip install django-xbench
```

`settings.py`의 middleware 목록에 실제 middleware 경로를 추가합니다.

```python
MIDDLEWARE = [
    "django_xbench.middleware.XBenchMiddleware",
    # ...
]
```

slow endpoint 집계가 필요하면 `XBENCH` 설정을 활성화합니다.

```python
XBENCH = {
    "ENABLED": True,
    "SLOW_AGG": True,
}
```

개발용 endpoint는 프로젝트 URL에 명시적으로 연결합니다.

```python
from django.urls import include, path

urlpatterns = [
    path("__xbench__/", include("django_xbench.slowagg.urls")),
]
```

- JSON: `GET /__xbench__/slow/?n=20`
- Dashboard: `GET /__xbench__/slow/ui/?n=20`

내부 성능 정보를 포함하므로 이 endpoint는 공개 환경에 그대로 노출하지 않는 것을 전제로 합니다.

## PyPI 배포와 오픈소스 피드백

재사용 가능한 Django package 구조로 정리해 PyPI에 배포했으며 GitHub에서 30+ stars를 얻었습니다. Django 공동 창시자 Simon Willison으로부터 in-memory 통계 집계 방식에 대한 긍정적인 피드백을 받았습니다.

이는 공식 추천이나 Django 프로젝트의 보증을 의미하지 않습니다. 직접 인용할 수 있는 코멘트 원문은 이번 작성 과정에서 확인하지 못해 인용문은 포함하지 않았습니다.

## 기술적 한계와 향후 개선점

- `app`은 전체 시간에서 DB 시간을 뺀 값이므로 serializer, template, 외부 API 등 애플리케이션 내부 구간을 더 세밀하게 분리하지는 않습니다.
- slow endpoint aggregation은 process별 memory에 저장되므로 여러 worker의 데이터를 통합하지 않습니다.
- 개발 및 내부 진단을 위한 도구이며 분산 trace와 장기 보관이 필요한 운영 APM을 대체하지 않습니다.
- 기존 Server-Timing metric과의 병합, DRF serializer 구간 측정, dashboard 필터 개선을 발전 과제로 두고 있습니다.

## 기술 스택

- Python 3.9+
- Django Middleware
- `connection.execute_wrapper`
- Server-Timing
- pytest, pytest-django
- PyPI

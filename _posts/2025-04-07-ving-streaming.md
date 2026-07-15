---
title: 유저와 아티스트를 잇는 실시간 스트리밍 서비스
date: 2025-04-07 00:00:00 +0900
categories: [Projects]
tags: [django, spring, mysql, mongodb, docker, nginx, aws, streaming]
description: 아티스트의 실시간 방송을 시청할 수 있는 서비스의 백엔드 구축 프로젝트입니다.
image:
  path: /assets/img/projects/ving/mockup.png
  alt: 실시간 스트리밍 서비스 화면
---

아티스트의 실시간 방송을 시청할 수 있는 서비스 백엔드를 구축했습니다.

## 주요 기능

- 실시간 방송 스트리밍
- 채팅 기능
- Adaptive Bitrate Streaming

## 기술 스택

- Backend: Django, Spring
- Database: MySQL, MongoDB
- DevOps: Docker, Nginx, AWS EC2·S3·CloudFront

## 맡은 역할

- DB 및 서비스 설계
- Nginx RTMP를 이용한 미디어 서버 구축
- Django를 이용한 API 개발
- 스트리밍 영상을 실시간으로 처리하여 S3에 업로드
- CloudFront를 이용한 정적 파일 CDN 구현

## ERD

![Ving ERD](/assets/img/projects/ving/erd.webp)

## 아키텍처

![Ving 아키텍처](/assets/img/projects/ving/architecture.png)

## 협업 문서

[Notion에서 프로젝트 문서 보기](https://grizzled-lord-170.notion.site/8aa729dea449454fb222e21c6e2863c4)

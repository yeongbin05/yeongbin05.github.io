---
title: Docker 이미지와 컨테이너 명령어
date: 2025-04-16 00:00:00 +0900
categories: [CS, Docker]
tags: [docker, container, image, command]
description: Docker 이미지 조회·삭제와 컨테이너 생성·실행 명령어를 정리합니다.
---

## 이미지 조회와 삭제

### 내려받은 이미지 조회

```bash
docker image ls
```

- `ls`: list의 약자
- `REPOSITORY`: 이미지 이름
- `TAG`: 이미지 태그명
- `IMAGE ID`: 이미지 ID
- `CREATED`: 이미지가 생성된 날짜이며 내려받은 날짜가 아님
- `SIZE`: 이미지 크기

### 이미지 삭제

특정 이미지를 삭제합니다.

```bash
docker image rm [이미지 ID 또는 이미지명]
```

이미지 ID는 다른 이미지와 구분할 수 있는 일부만 입력해도 됩니다. 컨테이너에서 사용하고 있지 않은 이미지만 삭제할 수 있습니다.

중지된 컨테이너에서 사용하는 이미지는 `-f` 옵션으로 강제 삭제할 수 있습니다. 실행 중인 컨테이너가 사용하는 이미지는 강제로 삭제할 수 없습니다.

```bash
docker image rm -f [이미지 ID 또는 이미지명]
```

전체 이미지를 삭제하는 명령은 다음과 같습니다.

```bash
# 컨테이너에서 사용하지 않는 이미지 삭제
docker image rm $(docker images -q)

# 컨테이너에서 사용하는 이미지를 포함해 강제 삭제
docker image rm -f $(docker images -q)
```

`docker images -q`는 시스템에 있는 모든 이미지의 ID만 반환합니다.

## 컨테이너 생성과 실행

이미지를 바탕으로 컨테이너를 생성합니다. `create`는 컨테이너를 실행하지 않고 생성만 합니다.

```bash
docker create 이미지명[:태그명]
docker create nginx
docker ps -a
```

로컬에 이미지가 없다면 Docker Hub에서 이미지를 내려받아 컨테이너를 생성합니다.

정지된 컨테이너는 다음과 같이 실행합니다.

```bash
docker start 컨테이너명[또는 컨테이너 ID]
docker ps
```

Nginx 컨테이너를 중단하고 삭제한 뒤 이미지까지 삭제하는 순서는 다음과 같습니다.

```bash
docker ps
docker stop {Nginx 컨테이너 ID}
docker rm {Nginx 컨테이너 ID}
docker image rm nginx
```

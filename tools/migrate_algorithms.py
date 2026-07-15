#!/usr/bin/env python3
"""Migrate selected algorithm content from the legacy site to Chirpy posts.

The default mode is a read-only dry run. Pass ``--write`` only after the
preflight report succeeds.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


EXPECTED_POST_COUNT = 137
EXCLUDED_BOJ = {
    "1004",
    "1167",
    "1415",
    "1629",
    "1655",
    "1932",
    "2096",
    "2212",
    "2503",
    "2531",
    "3085",
    "6236",
    "9019",
    "9435",
    "11052",
}

TARGET_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = TARGET_ROOT.parent
SOURCE_ROOT = WORKSPACE_ROOT / "my-site"
ALGORITHM_ROOT = SOURCE_ROOT / "public" / "data" / "algorithm"
POSTS_ROOT = TARGET_ROOT / "_posts"
IMAGE_ROOT = TARGET_ROOT / "assets" / "img" / "algorithm"


@dataclass(frozen=True)
class PostPlan:
    platform: str
    source_slug: str
    title: str
    date: str
    tags: tuple[str, ...]
    description: str
    code: str
    source_code: Path
    target: Path
    image_path: str
    image_alt: str

    @property
    def permalink(self) -> str:
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", self.target.stem)
        return f"/posts/{slug}/"


@dataclass(frozen=True)
class ImagePlan:
    source: Path
    target: Path


def fail(message: str) -> None:
    raise RuntimeError(message)


def ensure_within(path: Path, root: Path, label: str) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise RuntimeError(f"{label} is outside target root: {path}") from exc


def normalize_slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not normalized:
        fail(f"Cannot normalize empty slug: {value!r}")
    return normalized


def normalize_tag(value: str) -> str:
    normalized = normalize_slug(value.replace("&", " and "))
    return normalized


def read_description(path: Path) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    kept = [line for line in text.splitlines() if not line.strip().startswith("tags:")]
    return "\n".join(kept).strip()


def first_added_date(paths: list[Path]) -> str:
    relative_paths = [str(path.relative_to(SOURCE_ROOT)).replace("\\", "/") for path in paths]
    command = [
        "git",
        "-c",
        f"safe.directory={SOURCE_ROOT.as_posix()}",
        "-C",
        str(SOURCE_ROOT),
        "log",
        "--diff-filter=A",
        "--format=%as",
        "--",
        *relative_paths,
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    dates = sorted({line.strip() for line in result.stdout.splitlines() if line.strip()})
    if not dates:
        fail(f"No Git first-added date for: {', '.join(relative_paths)}")
    return dates[0]


def build_post_plans() -> list[PostPlan]:
    index_path = ALGORITHM_ROOT / "index.json"
    entries = json.loads(index_path.read_text(encoding="utf-8"))
    plans: list[PostPlan] = []

    for entry in entries:
        source_id = entry.get("id", "")
        if "/" not in source_id:
            fail(f"Invalid index id: {source_id!r}")
        platform, source_slug = source_id.split("/", 1)

        if platform == "boj":
            if source_slug in EXCLUDED_BOJ:
                continue
            title = f"BOJ {source_slug}"
            category = "BOJ"
            filename_slug = f"boj-{source_slug}"
            image_path = "/assets/img/algorithm/boj-default.png"
            image_alt = "BOJ 기본 이미지"
        elif platform == "leetcode":
            title = str(entry.get("title", "")).strip()
            if not title:
                fail(f"Missing LeetCode title: {source_id}")
            category = "LeetCode"
            normalized_source_slug = normalize_slug(source_slug)
            filename_slug = f"leetcode-{normalized_source_slug}"
            image_path = f"/assets/img/algorithm/leetcode/{normalized_source_slug}.png"
            image_alt = title
        else:
            fail(f"Unsupported platform in index: {platform}")

        source_dir = ALGORITHM_ROOT / platform / source_slug
        description_path = source_dir / "description.md"
        code_path = source_dir / "code.py"
        if not code_path.is_file() or code_path.stat().st_size == 0:
            fail(f"Selected item has missing or empty code: {source_id}")

        date_sources = [code_path]
        if description_path.exists():
            date_sources.append(description_path)
        thumbnail_path = source_dir / "thumbnail.png"
        if thumbnail_path.exists():
            date_sources.append(thumbnail_path)

        date = first_added_date(date_sources)
        target = POSTS_ROOT / f"{date}-{filename_slug}.md"
        ensure_within(target, POSTS_ROOT, "Post target")

        raw_tags = entry.get("tags") or []
        tags = tuple(normalize_tag(str(tag)) for tag in raw_tags)
        if len(tags) != len(set(tags)):
            fail(f"Duplicate normalized tags for {source_id}: {tags}")

        plans.append(
            PostPlan(
                platform=category,
                source_slug=source_slug,
                title=title,
                date=date,
                tags=tags,
                description=read_description(description_path),
                code=code_path.read_text(encoding="utf-8"),
                source_code=code_path,
                target=target,
                image_path=image_path,
                image_alt=image_alt,
            )
        )

    plans.sort(key=lambda plan: plan.target.name)
    return plans


def build_image_plans() -> list[ImagePlan]:
    mappings = [
        (SOURCE_ROOT / "public" / "baekjoon-default.png", IMAGE_ROOT / "boj-default.png"),
        (SOURCE_ROOT / "public" / "leetcode-default.png", IMAGE_ROOT / "leetcode-default.png"),
        (
            ALGORITHM_ROOT / "leetcode" / "missing_number" / "thumbnail.png",
            IMAGE_ROOT / "leetcode" / "missing-number.png",
        ),
        (
            ALGORITHM_ROOT / "leetcode" / "two_sum" / "thumbnail.png",
            IMAGE_ROOT / "leetcode" / "two-sum.png",
        ),
    ]
    plans = [ImagePlan(source=source, target=target) for source, target in mappings]
    for plan in plans:
        if not plan.source.is_file() or plan.source.stat().st_size == 0:
            fail(f"Missing or empty source image: {plan.source}")
        ensure_within(plan.target, IMAGE_ROOT, "Image target")
    return plans


def existing_post_permalinks() -> set[str]:
    permalinks: set[str] = set()
    for path in POSTS_ROOT.glob("*.md"):
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        permalinks.add(f"/posts/{slug}/")
    return permalinks


def render_post(plan: PostPlan) -> str:
    tags = json.dumps(list(plan.tags), ensure_ascii=False)
    lines = [
        "---",
        f"title: {json.dumps(plan.title, ensure_ascii=False)}",
        f"date: {plan.date} 00:00:00 +0900",
        f"categories: [Algorithm, {plan.platform}]",
        f"tags: {tags}",
        "image:",
        f"  path: {plan.image_path}",
        f"  alt: {json.dumps(plan.image_alt, ensure_ascii=False)}",
        "---",
        "",
    ]
    if plan.description:
        lines.extend([plan.description, ""])
    lines.extend(["## 풀이 코드", "", "```python"])
    prefix = "\n".join(lines) + "\n"
    code = plan.code
    suffix = "" if code.endswith("\n") else "\n"
    return prefix + code + suffix + "```\n"


def validate_rendered_post(plan: PostPlan, content: str) -> None:
    if not content.startswith("---\n"):
        fail(f"Missing front matter start: {plan.target}")
    if "\n---\n\n" not in content:
        fail(f"Missing front matter end: {plan.target}")
    if content.count("```python\n") != 1 or not content.endswith("```\n"):
        fail(f"Invalid Python Markdown fence: {plan.target}")
    code_start = content.index("```python\n") + len("```python\n")
    embedded_code = content[code_start : -len("```\n")]
    if embedded_code.endswith("\n") and not plan.code.endswith("\n"):
        embedded_code = embedded_code[:-1]
    if embedded_code != plan.code:
        fail(f"Embedded code differs from source: {plan.source_code}")


def preflight(posts: list[PostPlan], images: list[ImagePlan]) -> None:
    if len(posts) != EXPECTED_POST_COUNT:
        fail(f"Expected {EXPECTED_POST_COUNT} posts, found {len(posts)}")

    target_names = [plan.target.name for plan in posts]
    if len(target_names) != len(set(target_names)):
        fail("Duplicate target filenames detected")

    permalinks = [plan.permalink for plan in posts]
    if len(permalinks) != len(set(permalinks)):
        fail("Duplicate generated permalinks detected")

    collisions = sorted(set(permalinks) & existing_post_permalinks())
    if collisions:
        fail(f"Permalink collisions with existing posts: {collisions}")

    existing_targets = [plan.target for plan in posts if plan.target.exists()]
    existing_targets.extend(plan.target for plan in images if plan.target.exists())
    if existing_targets:
        fail("Refusing to overwrite existing files: " + ", ".join(map(str, existing_targets)))

    for plan in posts:
        validate_rendered_post(plan, render_post(plan))


def write_plans(posts: list[PostPlan], images: list[ImagePlan]) -> None:
    for plan in posts:
        plan.target.write_text(render_post(plan), encoding="utf-8", newline="\n")
    for plan in images:
        plan.target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(plan.source, plan.target)

    for plan in posts:
        validate_rendered_post(plan, plan.target.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="write posts and images after all preflight checks pass",
    )
    parser.add_argument("--verbose", action="store_true", help="list every planned post")
    args = parser.parse_args()

    if not SOURCE_ROOT.is_dir() or not POSTS_ROOT.is_dir():
        fail("Expected sibling my-site and target _posts directories")

    posts = build_post_plans()
    images = build_image_plans()
    preflight(posts, images)

    mode = "write" if args.write else "dry-run"
    boj_count = sum(plan.platform == "BOJ" for plan in posts)
    leetcode_count = sum(plan.platform == "LeetCode" for plan in posts)
    print(f"mode={mode}")
    print(f"posts={len(posts)}")
    print(f"boj={boj_count}")
    print(f"leetcode={leetcode_count}")
    print(f"images={len(images)}")
    print(f"excluded_boj={len(EXCLUDED_BOJ)}")
    print("unindexed_content=leetcode/count_good_triplets (not selected)")

    if args.verbose:
        for plan in posts:
            print(f"post={plan.target.relative_to(TARGET_ROOT)} permalink={plan.permalink}")
        for plan in images:
            print(f"image={plan.target.relative_to(TARGET_ROOT)}")

    if args.write:
        write_plans(posts, images)
        print("result=created")
    else:
        print("result=validated-no-files-written")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"error={exc}", file=sys.stderr)
        raise SystemExit(1)

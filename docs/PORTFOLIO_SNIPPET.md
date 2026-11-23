# Portfolio-ready project summary

## Korean

**AI-Native Architecture Lab — 자율형 AI 개발을 위한 아키텍처 실험**

Spring Boot·React 기반 주문 관리 기능을 기존 계층형 구조와 도메인 중심 FE/BE 통합 구조로 각각 구현하고, 자동 빌드 및 통합 테스트를 구축했습니다. 후속 연구를 위해 7개 아키텍처 관점을 반영한 **동일 소스 파일 배치 마이크로벤치마크**를 Python 표준 라이브러리로 구현했습니다. GitHub Actions에서 반복 측정을 수행하여 **원본 CSV, 요약 JSON, 시각화 SVG, Markdown 리포트**를 생성·보관합니다.

**현재 입증 범위:** 재현 가능한 소스 디렉터리 탐색 지표와 CI 검증. **아직 입증하지 않은 범위:** AI Agent의 토큰 효율·구현 성공률·아키텍처 간 실질적 우열.

Stack: Java 21, Spring Boot, React, Vite, Gradle, Python, GitHub Actions.

[Repo](https://github.com/issac-52/AI-Native-Architecture) | [Measurements](../results/latest/RESULTS.md)

## English

**AI-Native Architecture Lab — Benchmarking source organization for autonomous software agents.**

Implemented two functionally equivalent Spring Boot/React order-management apps, comparing conventional technical layers with domain-centered frontend/backend co-location. Built a reproducible, seven-layout **filesystem discovery microbenchmark** with Python, CI-driven repeated measurements, raw CSV/JSON outputs and SVG charts.

**Measured:** deterministic lexical scanning of identical code across directory layouts. **Not yet measured:** AI-agent task completion, tokens, regression rates or real-world architecture superiority.

[Repository](https://github.com/issac-52/AI-Native-Architecture)

# Portfolio-ready summary (v0.3)

## 한국어

**AI-Native Architecture Lab | 자율형 AI 개발을 위한 소스 아키텍처 비교 연구**

Spring Boot(Java 21) 기반 주문 관리 API를 계층형·DDD·Hexagonal·Vertical Slice·Modular Monolith·도메인 중심 AI-Native의 6개 구조로 각각 구현하고, React의 일반형·AI-Native형·FSD형 3개 빌드를 구성했습니다. 동일한 HTTP 계약을 검증하는 JUnit 공통 테스트와 아키텍처 의존성 검사를 GitHub Actions CI에 통합했습니다.

Python 기반 재현 가능 벤치마크를 개발해 **(1) 소스가 동일한 7가지 디렉터리 배치**와 **(2) 서로 다른 실행 구현 7개 조합**의 파일 탐색 시간·파일 수·코드량을 각각 반복 측정했습니다. 검색어 4개 × 구조당 100회씩, 각 데이터셋에서 총 **2,800개 원시 측정 기록**을 CSV·JSON·SVG·Markdown으로 생성하고 GitHub에 저장합니다.

**검증한 것:** 동일 HTTP 기능, 빌드 및 일부 아키텍처 경계 규칙, 실제 파일시스템의 검색 지표.

**아직 검증하지 않은 것:** LLM Agent의 토큰 사용량, 자율 개발 성공률, 회귀 오류, 아키텍처의 AI 개발 생산성 우열. 단순 검색 시간은 AI 성능으로 주장하지 않습니다.

**Stack:** Java 21, Spring Boot, React, Vite, Gradle, Python, JUnit, GitHub Actions.

[저장소](https://github.com/issac-52/AI-Native-Architecture) | [실행 구현 비교](../results/runnable/RESULTS.md) | [동일 코드 배치 비교](../results/latest/RESULTS.md)

## English

**AI-Native Architecture Lab | A reproducible architecture experiment for autonomous coding agents**

Implemented six Spring Boot order-API variations (Layered, DDD, Hexagonal, Vertical Slice, Modular Monolith and AI-Native domain co-location) with a shared JUnit HTTP contract suite, plus three React frontends including a Feature-Sliced Design example. Integrated CI, structural dependency checks and two distinct reproducible source-discovery microbenchmarks. Archived 2,800 raw observations per benchmark, machine-readable summaries and SVG charts.

**Evidence:** functional contract parity and deterministic lexical-source scanning. **Not yet measured:** actual AI-agent success, token consumption, regression rates or causal superiority of any architecture.

[GitHub repository](https://github.com/issac-52/AI-Native-Architecture)

# NEXT SIGHT: 시각장애인의 안전한 보행을 위한 AI 기반 스마트 시스템 👓

## 개요
**NEXT SIGHT**는 시각장애인을 위한 지능형 보행 보조 시스템으로,  
카메라・라이다・플렉스 센서・LLM 등을 통합하여  
사용자의 주변 상황을 인식하고 안전한 보행을 돕는 것을 목표로 한 프로젝트입니다.

본 프로젝트는 **광운대학교 로봇학부 2025-1학기 캡스톤** 과목을 통해 진행되었으며,  
**HOPE Project 대상** 을 수상하였습니다.

## 주요 기능
- 카메라를 통한 객체 인식 (YOLOv8 기반)  
- 라이다 센서를 이용한 거리 및 장애물 감지  
- 플렉스 센서를 이용한 손 제스처 명령 인식  
- 음성 인식(STT) 및 음성 안내(TTS) 기능 통합  
- ROS 2 기반 다중 보드 간 통신 구조 구성  

## 하드웨어 구성
- **스마트 안경:** Radxa Zero 3W (카메라, 마이크)  
- **스마트 지팡이:** Raspberry Pi 4 (LiDAR, 점자 디스플레이)  
- **스마트 장갑:** Raspberry Pi Zero 2W (Flex 센서)  
- **통신:** ROS 2 Humble + WireGuard VPN

## 프로젝트 정보
- **프로젝트명:** 시각장애인의 안전한 보행을 위한 AI 기반 스마트 시스템
- **팀명:** NEXT SIGHT  
- **소속:** 광운대학교 로봇학부  
- **기간:** 2025년 3월 ~ 2025년 9월  
- **수상:** HOPE Project 대상 (2025)


## 논문 / 연구자료
- **논문 제목:** *Development of an AI-Based Assistive Eyewear System for Safe Walking of the Visually Impaired*
- **발표 학회:** 2025 제40회 제어로봇시스템학회 학술대회
- **논문 링크:** [📎 클릭하여 보기](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12313588)  

---  

> 📍 *본 저장소는 NEXT SIGHT 프로젝트의 핵심 코드 및 자료를 포함하고 있으며,  
> 실제 하드웨어 환경에 따라 일부 설정이 상이할 수 있습니다.*

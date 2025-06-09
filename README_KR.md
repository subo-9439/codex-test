# 한국어 법률 QA 서비스

이 저장소는 FastAPI를 이용한 간단한 한국 법률 질의응답 데모 서비스를 제공합니다.

## 설치

1. Python 3.8 이상이 필요합니다.
2. 필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

## 서비스 실행

다음 명령으로 API 서버를 실행할 수 있습니다.

```bash
uvicorn api.main:app --reload
```

또는 Makefile의 `run` 타겟을 사용할 수 있습니다.

```bash
make run
```

## 학습

`docs/LEGAL_SERVICE_KR.md` 문서에서 예시 데이터로 모델을 학습하는 방법을 설명합니다. 기본 명령은 다음과 같습니다.

```bash
python scripts/train.py --model skt/kogpt2-base-v2 --dataset data/legal_cases.jsonl --output_dir model
```

## 테스트 실행

다음 명령으로 테스트를 실행합니다.

```bash
pytest
```

## 주의 사항

본 서비스는 데모용으로 제공됩니다. AI가 생성한 답변은 부정확하거나 불완전할 수 있으며 공식적인 법률 자문으로 간주해서는 안 됩니다. 필요한 경우 반드시 전문 변호사와 상담하시기 바랍니다.

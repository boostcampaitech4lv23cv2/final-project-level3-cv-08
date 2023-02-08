## Repository 구조

```
|-- README.md
|-- app
|   |-- DB
|   |   `-- README.md
|   |-- Makefile
|   |-- README.md
|   |-- __main__.py
|   |-- backend.py
|   |-- config.py
|   |-- config.yaml
|   |-- firm-lacing-374306-530d5efe30ba.json
|   |-- frontend.py
|   |-- gcs.py
|   |-- model.py
|   |-- model_db
|   |   |-- model.pth
|   |   |-- model_config.py
|   `-- notion.py
|-- mmseg
|   |-- apis
|   |   |-- __init__.py
|   |   `-- inference.py
|   |-- datasets
|   |   |-- __init__.py
|   |   |-- builder.py
|   |   `-- pipelines
|   |       `-- compose.py
|   `-- models
|       |-- __init__.py
|       `-- builder.py
|-- poetry.lock
`-- pyproject.tom
```

## Getting Started

0. 현재 위치를 app 으로 변경합니다
   ```shell
   cd app
   ```
1. Frontend(Streamlit)와 Server를 같이 실행합니다
   ```shell
   make -j 2 run_app
   # or

   python3 -m app
   # in other shell
   streamlit run app/frontend.py --server.port=30001
   ```

## Repository 구조
```
|-- DB
|-- Makefile
|-- README.md
|-- __main__.py
|-- backend.py
|-- config.py
|-- config.yaml
|-- confirm_button_hack.py
|-- db.py
|-- frontend.py
|-- model.py
`-- models
    |-- breakaged.pth
    |-- breakaged.py
    |-- crushed.pth
    |-- crushed.py
    |-- scratched.pth
    |-- scratched.py
    |-- separated.pth
    `-- separated.py
```
## Getting Started
0. 현재 위치를 mmsegmentation/app 으로 변경합니다
      ```shell
      cd mmsegmentation/app
      ```
1. Frontend(Streamlit)와 Server를 같이 실행합니다
      ```shell
      make -j 2 run_app
      # or
      
      python3 -m app
      # in other shell
      streamlit run app/frontend.py --server.port=30001
      ```
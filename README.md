

# CV-08 8bit | RDC(렌터카 회사를 위한 차량 손상 여부 관리 서비스)
<p align='center'>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> 
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white">
  <img src="https://img.shields.io/badge/Google Cloud-4285F4?style=for-the-badge&logo=Google Cloud&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white">
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=React&logoColor=white">
  <img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white">
</p>
  
## 🚗 프로젝트 개요
<img width="1878" alt="image" src="https://user-images.githubusercontent.com/74412423/217641603-cd8e3bed-5358-475b-ab89-c57d75eefc66.png">

- 여행에서 차량을 렌트할 때 차량의 상태를 제대로 확인하지 않거나 기록해놓지 않으면, 자신이 내지 않은 사고에 대해 오해 받을 수 있다. 따라서 차량을 렌트하는 소비자도 차량을 운행하기 전에 **차량의 상태**를 인지하는 것이 필요하다.

- 전국 렌터카 회사 중 69%가 차량을 100대 정도 보유하고 있는 **소규모 렌터카 회사**이고, 이들 대부분은 차량의 상태를 확인할 때 직원이 **직접 확인**하거나 **사진**을 찍어서 차량의 손상 여부를 파악하는 것으로 나타났다. 하지만 소규모 렌터카에서 차량 관리를 위해 AI 개발 인력을 투입하여 서비스를 구축하는 것은 무리가 있다.

- **RDC(Recognition Damage of Cars)** 렌터카 회사를 위한 차량 손상 여부 관리 서비스 프로젝트를 진행하게 되었다.
<br></br>
  
## 💾 데이터셋
- **차량 손상 이미지**를 수집한 데이터셋 (AI Hub)
- 훈련 데이터(train) 402,143장, 검증 데이터(valid) 50,445장 사용
- **손상 여부**가 중요하기 때문에 하나의 클래스로 만든 후 학습에 사용
<br></br>
  
## 📊 모델 학습

### - SegFormer
<img width="1920" alt="image" src="https://user-images.githubusercontent.com/74412423/217646568-40d26fa0-6871-45b2-8ada-aff626d24d24.png">

- Encoder-Decoder로 이루어진 모델
- **Transformer** 기반의 encoder → multi-scale feature를 뽑아냄
- **MLP** decoder → 낮은 연산량으로 적은 학습 시간
<br></br>

### - 모델 비교
|  |SegFormer-b2|ConvNeXt Base|Swin Transformer v2|Swin Transformer v1|
|--|--|--|--|--|
| mIoU | 76.83 | 77.51 | 66.72 | 71.59 |
| Background IoU | 95.37 | 95.53 | 86.91 | 89.82 |
| Damage IoU | 58.28 | 59.49 | 46.53 | 53.46 |
| 이미지 추론 시간(s) |  2.19   |  9.59     |     |     |

<br></br>

  
## 🗃️ 서비스 아키텍쳐

### - 전체 구성도
<img width="1920" alt="image" src="https://user-images.githubusercontent.com/74412423/217645344-7845d766-2ebc-4684-8243-bce4322bacea.png">

### - 고객 화면
- **고객 정보**와 **차량 정보**를 입력한 뒤 추론된 결과를 통해 **손상 여부를 파악**할 수 있음
<img width="1920" alt="image" src="https://user-images.githubusercontent.com/74412423/217643777-ee598880-0fc0-4197-bf2c-386cccc95988.png">

### - 관리자 화면
- 고객이 입력한 **데이터를 확인**할 수 있고, 노션의 API로 제작되어 관리자가 원하는 **편의 기능**을 자유롭게 구현할 수 있음
<img width="1920" alt="image" src="https://user-images.githubusercontent.com/74412423/217645912-7f863c62-93a0-4e6b-a176-e8d3ed5f24ad.png">
<br></br>

  
## 🚍 결론

### - 후속 개발 및 연구
-   성능 측면
    -   TensorRT의 도입 → inference 속도 향상
    -   유저 피드백을 기반으로 잘못된 inference 재학습 → 모델의 정확도 향상
-   관리자 사용 측면
    -   검수 알림 기준 개선 → 손상 수 변화나 위치 정보를 기준으로 추가적인 손상 구분
    -   추가 고객 정보 활용 → 예) 보험 유무 등
<br></br>

## 📑 참고자료

-   https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=581
-   Hao, S., Zhou, Y., & Guo, Y. (2020). A brief survey on semantic segmentation with deep learning. Neurocomputing, 406, 302-321.
-   Xie, E., Wang, W., Yu, Z., Anandkumar, A., Alvarez, J. M., & Luo, P. (2021). SegFormer: Simple and efficient design for semantic segmentation with transformers. Advances in Neural Information Processing Systems, 34, 12077-12090.
-   https://tech.socarcorp.kr/data/2020/02/13/car-damage-segmentation-model.html
-   https://www.flaticon.com/kr/
<br></br>

## 👨‍👨‍👧‍👧 팀 구성 및 역할

<table>
  <tr height="35px">
    <td align="center" width="180px">
      <a href="https://github.com/miinngdok">김동인_T4029</a>
    </td>
    <td align="center" width="180px">
      <a href="https://github.com/shinunjune">신원준_T4113</a>
    </td>
    <td align="center" width="180px">
      <a href="https://github.com/iihye">이혜진_T4177</a>
    </td>
    <td align="center" width="180px">
      <a href="https://github.com/22eming">정혁기_T4205</a>
    </td>
    <td align="center" width="180px">
      <a href="https://github.com/jun981015">홍준형_T4235</a>
    </td>
  </tr>
  <tr height="35px">
    <td align="center" width="180px">
      <a> 모델 학습 </a>
    </td>
    <td align="center" width="180px">
      <a> 모델 학습 </a>
    </td>
    <td align="center" width="180px">
      <a> 모델 학습, 프론트 개발 </a>
    </td>
    <td align="center" width="180px">
      <a> 서비스 아키텍쳐 개발 </a>
    </td>
    <td align="center" width="180px">
      <a> 데이터 분석, 모델 학습 </a>
    </td>
  </tr>
</table>

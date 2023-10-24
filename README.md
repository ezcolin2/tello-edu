# Tello Edu 드론 자율 주행 대회
# 주행 미션
1. 색 감지
2. 도형 감지
3. 사각형 링 감지 및 통과
4. QR 코드 감지 및 해석
5. 숫자 손글씨 인식
6. 비행기 기체 분류

# 사용 기술
1. openCV (색, 도형, 링 감지)
2. pyzbar (QR 코드 해석)
3. CNN model (숫자 손글씨 인식)
4. YOLO v8 (비행기 기체 분류)
5. Tello SDK (드론 제어)

# 미션 구현 방법
1. 색 감지 : RGB 색 공간을 HSV 색 공간으로 바꾼 후 색상, 명도, 채도 범위를 정해서 색 감지
2. 도형 감지 : contour 정보를 받아서 꼭짓점 개수로 도형 분류
3. 사각형 링 감지 : 아래 문제 해결 과정에서 기술
4. QR 코드 감지 : pyzbar 라이브러리 사용
5. 숫자 손글씨 인식 : CNN 모델과 MNIST 데이터 사용
6. 비행기 기체 분류 : robo flow에서 데이터 셋 생성 후 YOLO V8 모델 사요

# 전체적인 흐름 
![image](https://github.com/ezcolin2/tello-edu/assets/105545215/950d10e7-8e04-4c81-9014-3c947d14ef58)
1. Cam : 드론 캠으로 이미지 인식
2. Handler : 이미지 가공 후 감지한 객체의 외접 사각형 좌표 정보를 Tello에게 넘긴다.
3. AI model : 손글씨, 비행기 기체 분류의 경우 AI model에 넣어서 예측 값을 받는다.
4. Tello : Handler로부터 받은 좌표 정보를 바탕으로 오차 거리를 계산 후 PI 제어를 적용하여 드론을 제어한다.

# 문제 해결
## 1. 사각형과 링 구별
처음에 도형 구분을 할 때 외접 사각형의 꼭짓점 개수로만 판단을 하였다.

그래서 추후 링 통과 미션이 나왔을 때 사각형과 링을 같은 도형으로 판단하는 문제가 발생하였다.

하지만 둘은 확실한 차이가 존재했고 이 차이점을 기준으로 링과 도형을 구분하였다.

먼저 외접 contour를 그리고 그 안에 또 하나의 contour가 있으면 링으로 판단하였다.

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/b8121de6-aca0-4bd3-92cd-85b1fcd6ef12)

이 방법은 링 전체가 드론 캠 안에 들어왔을 때 거의 완벽하게 도형과 링을 구분할 수 있었다.

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/37f42f95-d026-469f-958b-5a960e18c882)

그러나 위 사진 처럼 캠 안에 전부 들어오지 않았을 때 contour는 단 하나밖에 검출하지 못했기 때문에 문제가 발생했다.

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/64b87434-1a81-43c7-8699-2b4bb33bdcc6)

그래서 이러한 경우 외접 사각형을 그리고 내부에 작은 사각형 하나를 그려서 이 안에 해당 색상의 존재 여부를 통해 추가적인 링 판단을 진행하였다.

이 안의 색상 면적 비율이 일정 비율 이하면 링이라고 판단한다.

## 2. 객체가 중심에 없음
객체 판단을 정확하게 하기 위해서는 객체가 중심에 있어야 한다.

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/94dd6a71-5a9a-4f38-a02e-9561bec4c270)

처음에는 단순히 캠 중심 좌표와 객체 중심 좌표의 거리를 계산해서 그만큼 이동하는 함수를 작성하였다.

그런데 tello sdk에서는 최소 이동 거리가 20cm이기 때문에 미세한 제어가 불가능하다.

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/2da7838f-c948-4dc8-8c89-6d0a468f10c6)

위 그림처럼 중심 좌표와의 거리가 20cm 미만이라면 계속 중심을 맞추지 못하고 좌우로 이동한다.

그래서 미세한 제어를 위해 거리가 아닌 속도로 드론을 제어하였다.

tello SDK에서는 거리 기반 제어 외에도 속도 기반 제어를 제공한다.
![image](https://github.com/ezcolin2/tello-edu/assets/105545215/8486b801-b586-4f39-8092-1bca357bb512)

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/5cc3518c-671a-45d8-8bcd-48ba45239946)

객체와의 거리가 멀다면 속도를 빠르게 하고 거리가 가까우면 속도를 느리게 하도록 PI 제어를 적용해서 드론이 중심을 맞추지 못하고 계속 움직이는 현상을 방지하였다

## 3. 회전 및 이동 방향 판단
![image](https://github.com/ezcolin2/tello-edu/assets/105545215/a71e4e60-0c06-4b3c-a28b-8783b5189f1c)
만약 감지한 도형의 width/height의 값이 1과 차이가 많이 난다면 측면을 보고 있다고 판단한다.
드론이 도형의 정면을 보기 위해서는 회전을 하면서 lr 방향으로 이동해야 한다.

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/d98f6cba-54c2-42b6-a70b-8e9663a02737)

하지만 위 그림처럼 width, height 비율만으로는 정확히 어떤 방향으로 회전하고 이동할지 결정할 수 없다.

그래서 조금 이동한 후 width/height 비율의 변화를 살펴보고 지금 방향이 옳은지

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/b7a8d158-dafa-42c2-86a5-8f266a9c2495)
만약 위 그림처럼 width/height의 값이 1에 가까워졌다면 옳은 방향이다.

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/9f09148b-92a5-466e-b3e2-de230583ec54)

하지만 위 그림처럼 width/height의 값이 1과 멀어졌다면 잘못된 방향이다.

이 경우 방향을 바꿔서 진행한다.

## 4. 회전, 이동 속도 문제

도형의 측면을 볼 때 여러 경우의 수가 존재한다.
그리고 드론의 각도, 떨어진 거리와 같은 요소에 따라 회전 속도와 이동 속도를 다르게 해야 한다.

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/7b05461a-ed02-4bd6-aa95-555c5128fdf0)
위 처럼 상황 1의 경우 회전을 많이 해야 한다.

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/fd720218-e64d-4c25-809d-4dedcddddf39)
위 처럼 상황 2의 경우 상황 2는 회전을 적게 해야 한다.

만약 상황 1과 같은 속도를 상황 2에 적용한다면 드론은 객체를 벗어날 수 있다.

만약 객체 사이의 거리, 각도 등을 모두 고려해서 속도를 조절하는 함수를 작성하기는 너무 번거로웠다.

그래서 회전 및 이동 속도는 특정 상수 값을 사용하였다.

하지만 그러다 보면 특정 경우에 객체를 벗어나는 경우가 발생한다.

![image](https://github.com/ezcolin2/tello-edu/assets/105545215/2061dc36-359c-42a1-a363-5a0a648abd9a)

그래서 만약 객체를 벗어났을 경우에 회전 속도를 0으로 만들고 다시 객체를 찾을 때까지 lr 방향으로 이동하도록 구현하였다.


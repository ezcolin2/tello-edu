
import logging
from djitellopy import Tello
# 로그 설정
logging.getLogger('djitellopy').setLevel(logging.WARNING)

tello = Tello()





# 연결
tello.connect()
print("연결 완료")

print(f'남은 배터리 : {tello.get_battery()}')
from glob import glob
import os.path

# 특정확장자를 가진 목록뽑기
files = glob(r'D:\wav\*.opus')

for x in files:
    # 파일만 걸러내기
    if not os.path.isdir(x):
        # 확장자와 순수파일명 구분하기
        filename = os.path.splitext(x)
        # temp(임시), m4a(중복) 파일은 제거
        if filename[1] == '.temp' or filename[1] == '.m4a':
            os.remove(x)
            print('{} ---- removed'.format(filename))
        else:
            # convert opus to wav
            try:
                # 순수파일명에 wav확장자 붙이기
                os.rename(x, filename[0]  + '.wav')
            except:
                # 중복된 wav 파일이 있을 경우 제거
                os.remove(x)
                print('{} ---- removed'.format(filename))
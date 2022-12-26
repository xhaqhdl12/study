#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 코드 통합버전
import pandas as pd
import numpy as np

# 추후에 merge 시킬 것을 고려해서, 아래 계산식은 별도 함수로 생성하기

def data_processing() :
    
    # 1. 전처리할 데이터 로드
    df = pd.read_excel('./file/(야간)주차장수급 실태조사 관리카드(남목1,2,3동)-구.xls', 
                          header=4,
                          usecols='A:BT',
                          skipfooter=68)
    df_notnull = df.fillna(0) #null 값은 0으로 대체

    #2. 컬럼명 변경(영문)
    df_notnull.columns =['OBJECTID','HJD_NM','YOD_NM','CAR_CNT','GAGU_CNT','INGU_CNT','BLOCK_NM','ONP_LSUM','ONP_GG_LCNT','ONP_P_LCNT','ONP_DT_SUM','ONP_DT_ICNT','ONP_DT_OCNT','ONP_DT_BBCNT',\
        'ONP_DT_V_SUM','ONP_DT_V_ICNT','ONP_DT_V_OCNT','ONP_DT_V_BCNT','ONP_DT_HSUM','ONP_DT_H_ICNT','ONP_DT_H_OCNT','ONP_DT_H_BCNT','ONP_DT_WSUM','ONP_DT_W_ICNT','ONP_DT_W_OCNT','ONP_DT_W_BCNT',\
        'ONP_NT_SUM','ONP_NT_ICNT','ONP_NT_OCNT','ONP_NT_BCNT','ONP_NT_V_SUM','ONP_NT_V_ICNT','ONP_NT_V_OCNT','ONP_NT_V_BCNT','ONP_NT_HSUM','ONP_NT_H_ICNT','ONP_NT_H_OCNT','ONP_NT_H_BCNT',\
        'ONP_NT_WSUM','ONP_NT_W_ICNT','ONP_NT_W_OCNT','ONP_NT_W_BCNT','OFP_SUM','OFP_LSUM','OFP_P_CNT','OFP_P_LCNT','OFP_M_CNT','OFP_M_LCNT','OFP_DT_PTD','OFP_DT_MTD','OFP_NT_PTD','OFP_NT_MTD',\
        'OFP_DT_ETC','OFP_DT_W','OFP_NT_ETC','OFP_NT_W','BUP_SUM','BUP_LSUM','BUP_JG_CNT','BUP_JG_LCNT','BUP_BJG_CNT','BUP_BJG_LCNT','BUP_DT_TD','BUP_NT_BJGTD','BUP_NT_JGTD','BUP_NT_TD','BUP_NT_BJGTD',\
        'BUP_NT_JGTD','BUP_DT_ETC','BUP_DT_W','BUP_NT_ETC','BUP_NT_W']

    # 실태조사 결과값은 새로 컬럼 추가+계산식 추가하는 방식으로 진행하기
    # 현재 컬럼 수 72개+16개(컬럼추가&통계적용)

    df_index = df_notnull

    # 3. 컬럼 추가+통계값 구하기
    # 3.1. 실태조사 주차장 개소 합계(TOT_PK_SUM)
    df_index['TOT_PK_SUM'] = df_index['BUP_SUM'] + df_index['OFP_SUM']

    # 3.2. 실태조사 주차장면수 합계(TOT_PKL_SUM)
    df_index['TOT_PKL_SUM'] = df_index['ONP_LSUM']+ df_index['OFP_LSUM']+df_index['BUP_LSUM'] #젤마지막 계산식이 틀렸었음
        ## (계산식) 노상주차장면수합계+노외주차장면수합계+부설주차장면수합계

    # 3.3. 주간차량적법(DT_CAR_IN)
    df_index['DT_CAR_IN'] = df_index['ONP_DT_ICNT']+df_index['ONP_DT_OCNT']+df_index['OFP_DT_ETC']+df_index['BUP_DT_ETC']
        ## (계산식) 노상주차장주간구역내+노상주차장주간구역밖+노외주간이륜외수요+부설주간이륜외수요

    # 3.4. 주간차량불법
    df_index['DT_CAR_OUT'] = df_index['ONP_DT_BBCNT']
        ## 노상주간불법

    # 3.5. 주간차량수요(DT_TD) -> 순서대로 코드 처리하는 방식 때문에 순서바꿔야함
    df_index['DT_TD'] = df_index['DT_CAR_IN']+df_index['DT_CAR_OUT']
        ## (계산식) 주간차량적법+주간차량불법

    # 3.6. 야간차량적법(NT_CAR_IN)
    df_index['NT_CAR_IN'] = df_index['ONP_NT_ICNT'] + df_index['ONP_NT_OCNT'] + df_index['OFP_NT_ETC'] + df_dg_index['BUP_NT_ETC']
        ## (계산식) 노상야간구역내+노상야간구역밖+야간노외이륜외+야간부설이륜외

    # 3.7. 야간차량불법(NT_CAR_OUT)
    df_index['NT_CAR_OUT'] = df_index['ONP_NT_BCNT']
        ## 노상야간불법

    # 3.8. 야간차량수요(NT_TD) -> 순서대로 코드 처리하는 방식 때문에 순서바꿔야함
    df_index['NT_TD'] = df_index['NT_CAR_IN'] + df_index['NT_CAR_OUT']
        ## (계산식) 야간차량적법+야간차량불법

    # 3.9. 차량등록대수(실태조사) = 등록차량수
    df_index['R_CAR_CNT'] = df_index['CAR_CNT']

    ## RATIO의 경우, round함수를 쓰면, 딱 떨어지는 경우 0.0과 같이 표현해주지 않음 
    ## 무조건 동일하게 소수첫째짜리까지 표현되게 하기 위해선 format 함수를 써야할듯(후순위)

    # 3.10. 확보율(소수 첫째짜리)
    df_index['HRATIO'] = round(df_index['TOT_PKL_SUM']/df_index['R_CAR_CNT']*100,1)
        # '실태조사 주차장면수/등록대수*100

    # 3.11. 주간이용률
    df_index['DT_ARATIO'] = round(df_index['DT_TD']/df_index['TOT_PKL_SUM']*100,1)
        ## 주간차량수요/실태조사 주차장면수*100

    # 3.12. 야간이용률
    df_index['NT_ARATIO'] = round(df_index.NT_TD/df_index.TOT_PKL_SUM*100,1)
        ## 야간차량수요/실태조사 주차장면수*100

    # 3.13. 주간확보율
    df_index['DT_HRATIO'] = round(df_index.TOT_PKL_SUM/df_index.DT_TD*100,1)
        ## 실태조사 주차장면수/주간차량수요*100

    # 3.14. 야간확보율
    df_index['NT_HRATIO'] = round(df_index.TOT_PKL_SUM/df_index.NT_TD*100,1)
        ## 실태조사 주차장면수/야간차량수요*100

    # 3.15. 주간불법율
    df_index['DT_OUT_RATIO'] = round(df_index.DT_CAR_OUT/df_index.DT_TD*100,1)
        ## 주간차량불법/주간차량수요

    # 3.16. 야간불법율
    df_index['NT_OUT_RATIO'] = round(df_index.NT_CAR_OUT/df_index.NT_TD*100,1)
        ## 야간차량불법/야간차량수요

    # 4. inf, null 값 >> 0으로 대체하기
    df_index = df_index.replace([np.inf],0.0) #inf 값 확인 >> np함수 기반 0으로 대체
    df_index_f = df_index.fillna(0) #새로 값을 추가하면서 '-' or null값 확인 >> 0으로 대체
    
    # # 5. 결과 출력
    return(df_index_f)

    # 6. 결과 파일 저장하기 작동은 안함.. 저장이 안되네?
    df_index_f.to_csv('./file/주차장수급 실태조사 관리카드_동구_전체(py5).csv', index = False, encoding='cp949')


# %%

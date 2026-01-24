import streamlit as st
import plotly.graph_objects as go
import requests
import re
import datetime as dt

st.set_page_config(layout="wide")

# 사이드바
with st.sidebar:
    st.subheader("기본 정보 입력")
    with st.container(border=True):        
        atpt_code = st.text_input("시도교육청코드", value="I10")
        schul_code = st.text_input("행정표준코드", value="9300117")
        meal_type = st.selectbox("급식 유형", ["중식(2)", "조식(1)", "석식(3)"], index=0)
        meal_code = meal_type[-2:-1]   # "중식(2)" → "2"
    c1, c2 = st.columns([2,1])
    with c2:
        run = st.button("조회")
    st.markdown("[🔎시도교육청/학교코드 확인](https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17320190722180924242823&infSeq=1)")

if not run:
    st.info("사이드바에서 기본 정보를 입력한 후, [조회]를 눌러 주세요.")
    st.stop()

# 이번주 시작일과 종료일 찾기
today = dt.date.today()
monday = today - dt.timedelta(days=today.weekday())  # 이번주 월요일
sunday = monday + dt.timedelta(days=6)               # 이번주 일요일
start_date = monday.strftime("%Y%m%d")
end_date = sunday.strftime("%Y%m%d")

# 데이터 불러오기
url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'	# 신청 주소
params ={'KEY' : st.secrets["NEIS_KEY"],		        # 인증키
         'Type' : 'json',			# json, xml?
         'pIndex' : 1,			# 불러올 페이지 번호
         'pSize' : 100,			# 한 페이지 당 불러올 요소 수
         'ATPT_OFCDC_SC_CODE' : atpt_code, 	# 시도교육청코드
         'SD_SCHUL_CODE' : schul_code,	# 행정표준코드(학교코드)
         'MMEAL_SC_CODE' : meal_code,		# 급식 유형(조식-1, 중식-2, 석식-3)
         'MLSV_FROM_YMD' : start_date,	# 급식 시작 일자
         'MLSV_TO_YMD' : end_date}	# 급식 종료 일자
response = requests.get( url, params = params )

if "mealServiceDietInfo" not in response.json():
    st.error(start_date+"~"+end_date+"의 급식 데이터가 없습니다.")
    st.stop()

count = response.json()[ 'mealServiceDietInfo' ][ 0 ][ 'head' ][ 0 ][ 'list_total_count' ]
data = response.json()[ 'mealServiceDietInfo' ][ 1 ][ 'row' ]

meal_list = []
kcal_list = []
date_list = []

for i in range(count) :    
    kcal_list.append( float( data[ i ][ 'CAL_INFO' ].replace(" Kcal", "") ) )
    date_list.append( data[ i ][ 'MLSV_YMD' ][-2:]+"일" )

    text = data[ i ][ 'DDISH_NM' ].replace("<br/>", "\n")
    meal_list.append( re.sub(r'<[^>]*>|\([^)]*\)', '', text) )

# 제목
shcool_name = data[0]['SCHUL_NM']
st.title(shcool_name+"의 이번주 급식")

# 여백 생성
for _ in range(3): 
    st.write("")

# 이번주 메뉴 출력하기
n_cols = count
cols = st.columns(n_cols)

for i, (d, m) in enumerate(zip(date_list, meal_list)):
    with cols[i % n_cols]:
        with st.container(border=True):
            st.subheader(d)
            st.text(m)

left, center, right = st.columns([4,1,1])

# 칼로리 막대 그래프 출력하기
with left:
    fig = go.Figure()
    fig.add_trace( go.Bar( x=date_list, y=kcal_list, marker_color='#4374D9') )
    fig.update_layout( title_text='칼로리 변화', title_x=0.5 )
    fig.update_xaxes( title_text='날짜' )
    fig.update_yaxes( title_text='칼로리' )
    st.plotly_chart(fig)

# 칼로리 통계 출력하기
with right:
    # 여백 생성
    for _ in range(5): 
        st.write("")
    avg_kcal = sum(kcal_list)/len(kcal_list)
    max_i = kcal_list.index(max(kcal_list))
    min_i = kcal_list.index(min(kcal_list))
    st.metric("평균 칼로리", f"{avg_kcal:.0f} kcal")
    st.metric("최고 칼로리", f"{kcal_list[max_i]:.0f} kcal")
    st.metric("최저 칼로리", f"{kcal_list[min_i]:.0f} kcal")

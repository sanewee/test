# code4
import streamlit as st            	
import plotly.graph_objects as go    	# Plotly의 그래프 객체 사용

year = [2021, 2022, 2023, 2024, 2025]	# 연도 데이터
areum = [150, 152, 155, 160, 163]		# 아름이 키 데이터
boram = [153, 154, 154, 159, 170]		# 보람이 키 데이터

fig = go.Figure()		# 빈 Figure(그래프) 객체 생성

fig.add_trace(		# 아름이 키 변화를 꺾은선 그래프로 추가
    go.Scatter(
        x=year,                      # 연도를 x축으로
        y=areum,                     # 키(cm)를 y축으로
        marker_color='orange',      # 선/마커 색상
        name='아름이 키(cm)'         # 범례에 표시될 텍스트
    )
)

fig.add_trace(		# 보람이 키 변화를 꺾은선 그래프로 추가
    go.Scatter(
        x=year,
        y=boram,
        marker_color='purple',
        name='보람이 키(cm)'
    )
)

fig.update_layout(
    title="아름이와 보람이의 최근 5년간 키(cm) 변화",	# 그래프 제목
    xaxis_title="연도",	# x축 설명
    yaxis_title="키(cm)"	# y축 설명
)

st.plotly_chart(fig) 	# Streamlit 화면에 Plotly 그래프 그리기

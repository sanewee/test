# code3
import streamlit as st
import streamlit as st            	
import plotly.graph_objects as go    	# Plotly의 그래프 객체 사용

# 사이드바 (슬라이더)
st.sidebar.title("사이드바")
st.sidebar.write("사이드바 설명")

# 탭
tab1, tab2 = st.tabs(["탭이름1", "탭이름2"])

with tab1:				# 첫 번째 탭의 콘텐츠
    st.header("첫 번째 탭")
    st.write("첫 번째 탭의 세부 내용")

    # 첫 번째 행
    col1, col2 = st.columns(2)
    with col1:
        st.header("영역1")
        st.info("긍정적 결과, 완료, 성공 출력")
    with col2:
        st.header("영역2")
        st.success("일반 안내, 참고사항 출력")

    # 두 번째 행
    col3, col4 = st.columns(2)
    with col3:
        st.header("영역3")
        st.warning("오류, 실패, 심각한 문제 출력")
    with col4:
        st.header("영역4")
        st.error("파이선 예외 메시지 출력")            

with tab2:				# 두 번째 탭의 콘텐츠
    st.header("두 번째 탭")
        # code4
    
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

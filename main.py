import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2",
    page_icon="🎬",
    layout="wide"
)

@st.cache_data
def load_data():
    """GitHub에서 영화 데이터를 불러오고 전처리합니다."""
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    try:
        df = pd.read_csv(url)
        # 장르 처리: 세로막대(|)로 구분된 경우 첫 번째 장르만 추출
        df['genre_main'] = df['genre'].apply(lambda x: x.split('|')[0] if pd.notnull(x) else '알 수 없음')
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

df = load_data()

st.title('영화 데이터 그래프 도감 2 - 분포와 관계')
st.write("1년간 박스오피스 10위권에 든 영화 중 이 기간에 개봉한 216편의 데이터 시각화")
st.divider()

if df is not None:
    st.subheader("1. 장르별 영화 편수 분포")
    
    # 장르별 편수 계산
    genre_counts = df['genre_main'].value_counts().reset_index()
    genre_counts.columns = ['장르', '편수']
    
    # Plotly 도넛 그래프 생성
    fig1 = px.pie(
        genre_counts, 
        names='장르', 
        values='편수', 
        hole=0.4, # 도넛 모양을 위한 구멍 크기 설정
        title='장르별 개봉 영화 편수',
        hover_data=['편수']
    )
    
    # 툴팁 형식 설정 (비율과 편수가 잘 보이도록)
    fig1.update_traces(textposition='inside', textinfo='percent+label', 
                       hovertemplate='<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}')
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # 시사점 영역
    st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 장르 분포에 대한 인사이트를 작성하세요. 예: 특정 장르의 편중 현상 등)")
    
    st.divider()

    st.subheader("2. 장르 및 영화별 총 관객 수 분포 (트리맵)")
    
    # Plotly 트리맵 그래프 생성
    # 계층 구조: 장르 -> 영화명, 크기: 총 관객 수(total_audi)
    fig2 = px.treemap(
        df,
        path=['genre_main', 'movieNm'],
        values='total_audi',
        title='장르 및 영화별 총 관객 수',
        color='total_audi',
        color_continuous_scale='Reds'
    )
    
    # 마우스 호버 시 표시될 내용 설정 (영화명/장르명과 총 관객 수)
    fig2.update_traces(
        hovertemplate='<b>%{label}</b><br>총 관객 수: %{value:,.0f}명<extra></extra>'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # 시사점 영역
    st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 트리맵 분석 인사이트를 작성하세요. 예: 특정 장르 내 대작 영화의 관객 집중도나 장르별 총 흥행 규모 비교 등)")
    
    st.divider()

else:
    st.warning("데이터를 불러오지 못해 그래프를 표시할 수 없습니다.")

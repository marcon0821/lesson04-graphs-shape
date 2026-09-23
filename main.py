import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 타이틀
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("KOBIS 박스오피스 상위권 영화 데이터를 바탕으로 장르별 분포와 관객 수 사이의 관계를 살펴봅니다.")

# 데이터 불러오기 및 전처리 캐싱
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르가 세로막대(|)로 구분된 경우 첫 번째 장르만 추출
    if 'genre' in df.columns:
        df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0].strip() if '|' in x else x.strip())
        
    return df

# 데이터 로드 실행
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# --- 첫 번째 그래프: 장르별 영화 편수 도넛 그래프 ---
st.header("1. 장르별 영화 편수 분포")
st.markdown("상위권에 진입한 영화들의 장르별 비중을 확인합니다.")

# 장르별 빈도수 계산
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# 플롯리 도넛 그래프 생성
fig1 = px.pie(
    genre_counts, 
    names='genre', 
    values='count', 
    hole=0.4,
    title="장르별 영화 편수 및 비율"
)
fig1.update_traces(
    textinfo='percent+label', 
    hovertemplate="<b>장르</b>: %{label}<br><b>편수</b>: %{value}편<br><b>비율</b>: %{percent}"
)
st.plotly_chart(fig1, use_container_width=True)

# '이 그래프로 알 수 있는 것' 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 박스오피스 상위권에 가장 많이 이름을 올린 주력 장르가 무엇인지, 관객들에게 인기 있는 영화 장르의 분포 비율을 직관적으로 파악할 수 있습니다.")

st.divider()

# --- 두 번째 그래프: 개봉 첫 주 관객수와 총 관객수의 관계 (산점도) ---
st.header("2. 개봉 첫 주 관객수와 총 관객수의 관계")
st.markdown("개봉 첫 주에 동원한 관객수가 최종 총 관객수에 어떤 영향을 미치는지 살펴봅니다.")

fig2 = px.scatter(
    df,
    x='first_week_audi',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    labels={'first_week_audi': '개봉 첫 주 관객수', 'total_audi': '총 관객수', 'genre': '장르'},
    title="개봉 첫 주 관객수 vs 총 관객수 산점도"
)
st.plotly_chart(fig2, use_container_width=True)

# '이 그래프로 알 수 있는 것' 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 개봉 첫 주 관객수와 총 관객수 사이의 상관관계를 볼 수 있습니다. 대개 첫 주에 관객이 많이 들었던 영화일수록 최종 총 관객수도 비례해서 높아지는 흐름을 확인할 수 있습니다.")

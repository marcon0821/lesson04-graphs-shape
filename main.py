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
    url = "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"
    try:
        df = pd.read_csv(url)
        # 장르 처리: 세로막대(|)로 구분된 경우 첫 번째 장르만 추출
        df['genre_main'] = df['genre'].apply(lambda x: x.split('|')[0] if pd.notnull(x) else '알 수 없음')
        # 제작 국가 결측치 처리
        df['nation'] = df['nation'].fillna('알 수 없음')
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

    top_movie = df.loc[df['total_audi'].idxmax()]
    top_movie_name = top_movie['movieNm']
    top_movie_audi = top_movie['total_audi']

    st.subheader("3. 총 관객 수 분포 (히스토그램)")
    
    fig3 = px.histogram(
        df,
        x='total_audi',
        nbins=25,
        title='영화별 총 관객 수 분포',
        labels={'total_audi': '총 관객 수', 'count': '영화 편수'},
        color_discrete_sequence=['#E50914']
    )
    
    fig3.update_layout(
        xaxis_title="총 관객 수 (명)",
        yaxis_title="영화 편수 (개)",
        bargap=0.1
    )
    
    fig3.update_traces(
        hovertemplate='관객 수 구간: %{x}<br>영화 편수: %{y}편<extra></extra>'
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # 시사점 영역 (가장 관객 수가 많은 영화 및 분포 구간 자동 안내)
    st.info(
        f"💡 **이 그래프로 알 수 있는 것:** 대다수의 영화는 총 관객 수 100만~200만 명 이하의 하위 구간에 모여 있으며, "
        f"가장 많은 관객을 동원한 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,.0f}명)입니다."
    )
    
    st.divider()

    st.subheader("4. 개봉일 스크린 수와 총 관객 수의 관계 (산점도)")
    
    # Plotly 산점도 생성 (x: 개봉일 스크린 수, y: 총 관객 수, 점 색상: 장르, 호버: 영화명)
    fig4 = px.scatter(
        df,
        x='first_scrn',
        y='total_audi',
        color='genre_main',
        hover_name='movieNm',
        hover_data={'first_scrn': ':,', 'total_audi': ':,', 'genre_main': True},
        title='개봉일 스크린 수 vs 총 관객 수',
        labels={
            'first_scrn': '개봉일 스크린 수 (개)',
            'total_audi': '총 관객 수 (명)',
            'genre_main': '장르'
        }
    )
    
    fig4.update_layout(
        xaxis_title="개봉일 스크린 수 (개)",
        yaxis_title="총 관객 수 (명)"
    )
    
    fig4.update_traces(
        marker=dict(size=10, opacity=0.8)
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    # 시사점 영역
    st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린 수가 많을수록 대체로 총 관객 수도 증가하는 비례 관계를 보이지만, 초기 스크린 수가 적음에도 대형 흥행을 기록한 영화(입소문 흥행)나 그 반대의 예외 사례들도 함께 파악할 수 있습니다.")
    
    st.divider()

    st.subheader("5. 주요 장르별 총 관객 수 분포 (박스플롯)")
    
    # 영화 편수가 10편 이상인 장르 필터링
    genre_counts = df['genre_main'].value_counts()
    top_genres = genre_counts[genre_counts >= 10].index
    df_top_genres = df[df['genre_main'].isin(top_genres)]
    
    # Plotly 박스플롯 생성 (x: 장르, y: 총 관객 수, 아웃라이어 호버: 영화명)
    fig5 = px.box(
        df_top_genres,
        x='genre_main',
        y='total_audi',
        color='genre_main',
        hover_name='movieNm',
        hover_data={'total_audi': ':,', 'genre_main': False},
        points='outliers', # 상자 밖의 이상치(아웃라이어) 점 표시
        title='영화 10편 이상 장르별 총 관객 수 분포',
        labels={
            'genre_main': '장르',
            'total_audi': '총 관객 수 (명)'
        }
    )
    
    fig5.update_layout(
        xaxis_title="장르",
        yaxis_title="총 관객 수 (명)",
        showlegend=False
    )
    
    st.plotly_chart(fig5, use_container_width=True)
    
    # 시사점 영역
    st.info("💡 **이 그래프로 알 수 있는 것:** 주요 장르별 관객 수의 중간값(중앙값)과 50% 범위를 비교할 수 있으며, 상자 밖으로 튀어 나온 점(아웃라이어)에 마우스를 올려 해당 장르에서 이례적으로 대형 흥행을 기록한 영화가 무엇인지 확인할 수 있습니다.")
    
    st.divider()

    st.subheader("6. 개봉일 스크린 수 vs 총 관객 수 (버블 크기: 개봉 첫 주 관객 수)")
    
    # Plotly 버블 그래프 생성 (x: 개봉일 스크린 수, y: 총 관객 수, size: 개봉 첫 주 관객 수, color: 장르)
    fig6 = px.scatter(
        df,
        x='first_scrn',
        y='total_audi',
        size='first_week_audi',
        color='genre_main',
        hover_name='movieNm',
        hover_data={
            'first_scrn': ':,',
            'total_audi': ':,',
            'first_week_audi': ':,',
            'genre_main': True
        },
        size_max=40,  # 버블 최대 크기 설정
        title='개봉일 스크린 수 vs 총 관객 수 (버블 크기: 개봉 첫 주 관객 수)',
        labels={
            'first_scrn': '개봉일 스크린 수 (개)',
            'total_audi': '총 관객 수 (명)',
            'first_week_audi': '개봉 첫 주 관객 수 (명)',
            'genre_main': '장르'
        }
    )
    
    fig6.update_layout(
        xaxis_title="개봉일 스크린 수 (개)",
        yaxis_title="총 관객 수 (명)"
    )
    
    st.plotly_chart(fig6, use_container_width=True)
    
    # 시사점 영역
    st.info("💡 **이 그래프로 알 수 있는 것:** 버블의 크기(개봉 첫 주 관객 수)를 함께 비교하면, 초기 스크린 수가 비슷하더라도 개봉 초반 흥행 폭발력이 우수했던 영화와 장기 입소문으로 총 관객 수를 확대한 영화의 차이를 입체적으로 관찰할 수 있습니다.")
    
    st.divider()

    st.subheader("7. 제작 국가 및 장르별 영화 편수 분포 (선버스트)")
    
    # Plotly 선버스트 그래프 생성 (계층 구조: 제작 국가 -> 장르, 크기: 영화 편수)
    fig7 = px.sunburst(
        df,
        path=['nation', 'genre_main'],
        title='제작 국가 및 장르별 영화 편수 계층 구조',
        color='nation',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig7.update_traces(
        hovertemplate='<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>'
    )
    
    st.plotly_chart(fig7, use_container_width=True)
    
    # 시사점 영역
    st.info("💡 **이 그래프로 알 수 있는 것:** 중앙의 제작 국가(한국, 미국 등)에서 외곽의 장르로 이어지는 계층 구조를 통해, 각 국가별 전체 영화 수와 국가 내 장르 다양성/비중을 계층적으로 손쉽게 비교할 수 있습니다.")
    
    st.divider()

else:
    st.warning("데이터를 불러오지 못해 그래프를 표시할 수 없습니다.")

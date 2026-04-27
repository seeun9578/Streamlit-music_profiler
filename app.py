import streamlit as st
import time

@st.cache_data
def load_quiz_data():
    time.sleep(1) 
    return [
        {
            "question": "1. 당신이 평소 즐겨듣는 음악 장르는?",
            "options": ["발라드", "힙합", "댄스(아이돌)", "인디음악"]
        },
        {
            "question": "2. 하루 평균 음악 감상 시간은 어느 정도인가요?",
            "options": ["거의 듣지 않음", "1시간 이상 2시간 미만", "2시간 이상 3시간 미만", "3시간 이상"]
        },
        {
            "question": "3. 현재 좋아하거나 응원하는 가수/밴드/그룹의 수는?",
            "options": ["없음", "1~3개", "4~6개", "7개 이상"]
        }
    ]

def get_recommendations(genre):
    recommendations = {
        "발라드": ["10CM", "박효신", "아이유", "권진아"],
        "힙합": ["빈지노", "창모", "지코", "박재범"],
        "댄스(아이돌)": ["뉴진스", "아이브", "아일릿", "NCT WISH"],
        "인디음악": ["한로로", "잔나비", "데이먼스 이어", "혁오"]
    }
    return recommendations.get(genre, [])

def main():
    st.set_page_config(page_title="음악 몰입도 및 취향 진단", layout="centered")
    st.title("Music Profiler")
    st.markdown("#### : 당신의 음악적 취향을 정밀 분석합니다.")
    st.success("Developer Info | 학번: 2025404037 | 이름: 홍세은")
    
    st.divider()

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.header("🔐 로그인")
        with st.form("login_form"):
            user_id = st.text_input("아이디")
            user_pw = st.text_input("비밀번호", type="password")
            if st.form_submit_button("접속"):
                if user_id == "홍세은" and user_pw == "1234":
                    st.session_state.logged_in = True
                    st.success("로그인에 성공했습니다.")
                    st.rerun()
                else:
                    st.error("로그인 정보가 틀렸습니다. 다시 시도해주세요.")
    else:
        st.sidebar.button("로그아웃", on_click=lambda: st.session_state.update({"logged_in": False}))
        
        st.header("음악 소비 성향 설문")
        quiz_data = load_quiz_data()
        
        responses = []
        with st.form("quiz_form"):
            for i, item in enumerate(quiz_data):
                ans = st.radio(item["question"], item["options"], key=f"q{i}")
                responses.append(ans)
            
            submitted = st.form_submit_button("분석 결과 확인 및 가수 추천")
            
        if submitted:
            st.divider()
            
            score = quiz_data[1]["options"].index(responses[1]) + quiz_data[2]["options"].index(responses[2])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("몰입도 진단")
                if score >= 5:
                    st.success("### '몰입도: 상'")
                    st.write("음악 전문가이시군요!.")
                elif 2 <= score <= 4:
                    st.info("### '몰입도: 중'")
                    st.write("일상에서 음악을 즐겁게 소비하고 계시네요.")
                else:
                    st.warning("### '몰입도: 하'")
                    st.write("취향에 맞는 가수를 추천드릴테니, 들어보세요!")

            with col2:
                # 질문 1(장르)에 따른 맞춤형 추천 아티스트 출력
                selected_genre = responses[0]
                st.subheader("추천 아티스트")
                recs = get_recommendations(selected_genre)
                st.write(f"**{selected_genre}** 취향을 위한 추천:")
                for artist in recs:
                    st.write(f"- {artist}")

            st.divider()
        

if __name__ == "__main__":
    main()
import pandas as pd
import streamlit as st
import time
from streamlit_server_state import server_state, server_state_lock

df = pd.read_csv('./res/list-of-players.csv', delimiter=';')

list_of_teams = sorted(list(set(df["TeamName"])))

check_in_dict = {}

if "check_in_dict" not in server_state:
    server_state.check_in_dict = {}

def check_team_in(team):
    if team in server_state.check_in_dict.keys():
        if server_state.check_in_dict[team] == 1:
            server_state.check_in_dict[team] = 0
            st.markdown(f'{team}, er nu tjekket ud igen.')
        else:
            server_state.check_in_dict[team] = 1
            st.balloons()
            time.sleep(2)
            st.markdown(f'## Velkommen {team}, I er nu tjekket ind. ##')
    else:
        server_state.check_in_dict[team] = 1
        st.balloons()
        time.sleep(2)
        st.markdown(f'### Velkommen {team}, I er nu tjekket ind. ###')
    

with st.sidebar:
    view = st.radio('Vælg visning', ['Indmelding', 'Dommerbord'])

st.markdown("# DPT NYTÅRSKUR #")

if view == 'Indmelding':

    col1, col2 = st.columns([4,2])

    with col1:
        st.markdown('### SPILLER CHECK-IN ###')
    with col2:
        st.image('res/dpt text.png')
    
    st.markdown('---')
    team = st.selectbox('Vælg par', list_of_teams)

    check_in = st.button('Check in')

    if check_in:
        check_team_in(team)
else:
    check_in_df = pd.DataFrame.from_dict(server_state["check_in_dict"], orient='index')
    check_in_df.rename({0:'Check-in status'}, axis=1, inplace=True)
    hold_df = df.join(check_in_df, on="TeamName", how='left')
    hold_df["Checked In"] = hold_df["Check-in status"].apply(lambda x: "Ja" if x == 1 else "Nej")
    hold_df_grouped = hold_df.groupby(["Class", "TeamName"])["Check-in status"].agg('mean').fillna(0)
    class_df = hold_df[["Class", "TeamName", "Check-in status"]].copy()
    class_df.drop_duplicates(inplace=True)
    class_df_grouped = class_df.groupby(["Class"])[["TeamName", "Check-in status"]].agg('count')
    
    st.markdown("### DOMMERBORD ###")
    st.markdown("---")
    st.dataframe(class_df_grouped)
    st.markdown("---")
    st.dataframe(hold_df[["Class", "TeamName", "Checked In"]].drop_duplicates())


#st.write(server_state["check_in_dict"])

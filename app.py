import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('orange_cap.csv')
df.drop(columns='Span', inplace=True)

# Define Player class and analysis functions
class Player:
    def __init__(self, name, span, matches, innings, not_out, runs, highest_score, average, balls_faced, strike_rate, hundreds, fifties, ducks, fours, sixes):
        self.name = name
        self.span = span
        self.matches = matches
        self.innings = innings
        self.not_out = not_out
        self.runs = runs
        self.highest_score = highest_score
        self.average = average
        self.balls_faced = balls_faced
        self.strike_rate = strike_rate
        self.hundreds = hundreds
        self.fifties = fifties
        self.ducks = ducks
        self.fours = fours
        self.sixes = sixes

def highest_run_scorer(players):
    return max(players, key=lambda p: p.runs)

def best_batting_average(players):
    return max(players, key=lambda p: p.average)

def highest_strike_rate(players):
    return max(players, key=lambda p: p.strike_rate)

def most_sixes(players):
    return max(players, key=lambda p: p.sixes)

def most_fours(players):
    return max(players, key=lambda p: p.fours)

def highest_individual_score(players):
    return max(players, key=lambda p: int(p.highest_score.rstrip('*')))

# Function to display percentage of runs by boundaries
def runs_by_boundaries(player):
    df_new = df[df['Player'].str.contains(player, case=False)]
    if not df_new.empty:
        total_runs = df_new['4s'].values * 4 + df_new['6s'].values * 6
        percentage = (total_runs * 100) // df_new['Runs'].values
        return f"{percentage[0]}% runs through boundaries"
    else:
        return "Player not found"

# Function to find team players
def find_team_players(team):
    team_players = df[df['Player'].str.contains(team, case=False)]
    if not team_players.empty:
        return team_players
    else:
        return "Team not found"

# Streamlit UI
st.title("Cricket Player Analysis")

# User input for player name and team




# Analysis options
st.sidebar.title("Analysis Options")
analysis_option = st.sidebar.selectbox("Choose Analysis", 
                                       ["Most Sixes", "Most Fours", "Most Balls Faced", 
                                        "Most 6s and 4s (Stacked)", "Most 6s and 4s (Grouped)", 
                                        "Balls Faced vs Runs Scored", "200+ Strike Rate", 
                                        "Most Ducks", "Player Stats", "Team Stats"])

# Visualization based on analysis option
if analysis_option == "Most Sixes":
    most_sixes = df.sort_values('6s', ascending=False).head(10)
    fig = px.bar(most_sixes, x='Player', y='6s', title='Most Number of Sixes By Players')
    st.plotly_chart(fig)

elif analysis_option == "Most Fours":
    most_fours = df.sort_values('4s', ascending=False).head(10)
    fig = px.bar(most_fours, x='Player', y='4s', title='Most Number of Fours By Players')
    st.plotly_chart(fig)

elif analysis_option == "Most Balls Faced":
    most_balls_faced = df.sort_values('BF', ascending=False).head(10)
    fig = px.bar(most_balls_faced, x='Player', y='BF', title='Most Number of Balls Faced By Players', labels={'BF':'Balls Faced'})
    st.plotly_chart(fig)

elif analysis_option == "Most 6s and 4s (Stacked)":
    fig = px.bar(df.head(20), x='Player', y=['4s', '6s'], title='Most Number 6s and 4s By Players', barmode='stack')
    st.plotly_chart(fig)

elif analysis_option == "Most 6s and 4s (Grouped)":
    fig = px.bar(df.head(20), x='Player', y=['4s', '6s'], title='Most Number 6s and 4s By Players', barmode='group')
    st.plotly_chart(fig)

elif analysis_option == "Balls Faced vs Runs Scored":
    fig = px.scatter(df.head(20), x='BF', y='Runs', color='Player', title='Balls Faced Vs Runs Scored', labels={'BF':'Balls Faced'})
    st.plotly_chart(fig)

elif analysis_option == "200+ Strike Rate":
    good_strike_rate = df[(df['BF'] > 50) & (df['SR'] > 200)]
    fig = px.bar(good_strike_rate, x='Player', y='SR', title="Players With 200+ Strike Rate (Faced at least 50 Balls)", labels={'SR':'Strike Rate'})
    st.plotly_chart(fig)

elif analysis_option == "Most Ducks":
    ducks = df.sort_values('0', ascending=False).head(10)
    fig = px.bar(ducks, x='Player', y='0', labels={'0':'Ducks'}, title='Players With Most Ducks')
    st.plotly_chart(fig)

elif analysis_option == "Player Stats":
    player_name = st.text_input("Enter Player Name Ex.(Kohli)")

    if player_name:
        player_data = df[df['Player'].str.contains(player_name, case=False)]
        if not player_data.empty:
            # Display player stats in a stylish way
            st.markdown(f"## {player_name}'s Statistics")
            st.markdown(f"### Highest Score: {player_data.iloc[0]['HS']}")
            st.markdown(f"### Average: {player_data.iloc[0]['Ave']}")
            st.markdown(f"### Strike Rate: {player_data.iloc[0]['SR']}")
            st.markdown(f"### Runs: {player_data.iloc[0]['Runs']}")
            st.markdown(f"### 100s: {player_data.iloc[0]['100']}, 50s: {player_data.iloc[0]['50']}")
            st.markdown(f"### 4s: {player_data.iloc[0]['4s']}, 6s: {player_data.iloc[0]['6s']}")
            st.markdown(f"### Ducks: {player_data.iloc[0]['0']}")
            st.table(player_data)
        else:
            st.write("Player not found")

elif analysis_option == "Team Stats":
    team_name = st.text_input("Enter Team Name")
    if team_name:
        team_data = find_team_players(team_name)
        if isinstance(team_data, pd.DataFrame):
            st.table(team_data)
        else:
            st.write(team_data)

# Display percentage of runs by boundaries for a given player
st.sidebar.title("Percentage of Runs by Boundaries")
player_for_boundaries = st.sidebar.text_input("Enter Player Name for Boundaries Analysis")
if player_for_boundaries:
    percentage = runs_by_boundaries(player_for_boundaries)
    st.sidebar.write(percentage)

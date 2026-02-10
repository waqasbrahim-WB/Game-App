import streamlit as st
import random
import time
import pandas as pd
import numpy as np
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Mini Games Collection",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px #000000;
    }
    .game-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 1rem;
        transition: transform 0.3s;
    }
    .game-card:hover {
        transform: translateY(-5px);
    }
    .score-board {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0
if 'total_score' not in st.session_state:
    st.session_state.total_score = 0
if 'current_game' not in st.session_state:
    st.session_state.current_game = None
if 'number_to_guess' not in st.session_state:
    st.session_state.number_to_guess = None
if 'guess_count' not in st.session_state:
    st.session_state.guess_count = 0
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'memory_board' not in st.session_state:
    st.session_state.memory_board = None
if 'memory_flipped' not in st.session_state:
    st.session_state.memory_flipped = []
if 'memory_matched' not in st.session_state:
    st.session_state.memory_matched = []
if 'memory_last_click' not in st.session_state:
    st.session_state.memory_last_click = None

# Header
st.markdown('<h1 class="main-header">🎮 Ultimate Games Collection</h1>', unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/controller.png", width=100)
    st.title("Navigation")
    game_choice = st.radio(
        "Choose a Game:",
        ["🏠 Home", "🎯 Number Guesser", "❓ Quiz Game", "🎲 Dice Roller", 
         "🧠 Memory Game", "✂️ Rock Paper Scissors", "📊 Game Stats"]
    )
    
    st.markdown("---")
    st.markdown('<div class="score-board">', unsafe_allow_html=True)
    st.metric("Games Played", st.session_state.games_played)
    st.metric("Total Score", st.session_state.total_score)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Reset All Scores"):
        st.session_state.games_played = 0
        st.session_state.total_score = 0
        st.success("Scores reset successfully!")

# Home Page
if game_choice == "🏠 Home":
    st.markdown("## Welcome to the Ultimate Games Collection!")
    st.write("Select a game from the sidebar to start playing!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.subheader("🎯 Number Guesser")
        st.write("Guess the number between 1-100")
        st.write("Score: Up to 100 points")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.subheader("❓ Quiz Game")
        st.write("Test your knowledge")
        st.write("Score: 10 points per question")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.subheader("🧠 Memory Game")
        st.write("Match the pairs")
        st.write("Score: 5 points per pair")
        st.markdown('</div>', unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.subheader("🎲 Dice Roller")
        st.write("Roll and win prizes")
        st.write("Score: Random rewards")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.subheader("✂️ Rock Paper Scissors")
        st.write("Beat the computer")
        st.write("Score: 5 points per win")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.subheader("📊 Game Stats")
        st.write("Track your progress")
        st.write("View all statistics")
        st.markdown('</div>', unsafe_allow_html=True)

# Number Guessing Game
elif game_choice == "🎯 Number Guesser":
    st.header("🎯 Number Guessing Game")
    
    if st.button("🔄 Start New Game"):
        st.session_state.number_to_guess = random.randint(1, 100)
        st.session_state.guess_count = 0
        st.success("New game started! Guess a number between 1 and 100")
    
    if st.session_state.number_to_guess is None:
        st.info("Click 'Start New Game' to begin!")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            guess = st.number_input("Enter your guess (1-100):", 
                                   min_value=1, max_value=100, step=1)
            
            if st.button("Submit Guess"):
                st.session_state.guess_count += 1
                
                if guess < st.session_state.number_to_guess:
                    st.warning("Too low! Try a higher number.")
                elif guess > st.session_state.number_to_guess:
                    st.warning("Too high! Try a lower number.")
                else:
                    score = max(0, 100 - (st.session_state.guess_count * 5))
                    st.balloons()
                    st.success(f"🎉 Correct! The number was {st.session_state.number_to_guess}")
                    st.success(f"You guessed it in {st.session_state.guess_count} tries!")
                    st.success(f"Score earned: {score} points")
                    
                    st.session_state.total_score += score
                    st.session_state.games_played += 1
                    st.session_state.number_to_guess = None
        
        with col2:
            st.markdown('<div class="score-board">', unsafe_allow_html=True)
            st.write(f"**Guesses made:** {st.session_state.guess_count}")
            if st.session_state.number_to_guess:
                st.write(f"**Possible score:** {max(0, 100 - (st.session_state.guess_count * 5))}")
            st.markdown('</div>', unsafe_allow_html=True)

# Quiz Game
elif game_choice == "❓ Quiz Game":
    st.header("❓ Quiz Game")
    
    # Quiz questions and answers
    quiz_data = [
        {
            "question": "What is the capital of France?",
            "options": ["London", "Berlin", "Paris", "Madrid"],
            "answer": "Paris"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"],
            "answer": "Mars"
        },
        {
            "question": "What is the largest mammal in the world?",
            "options": ["Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
            "answer": "Blue Whale"
        },
        {
            "question": "Who painted the Mona Lisa?",
            "options": ["Van Gogh", "Picasso", "Da Vinci", "Rembrandt"],
            "answer": "Da Vinci"
        }
    ]
    
    score = 0
    for i, q in enumerate(quiz_data):
        st.subheader(f"Question {i+1}: {q['question']}")
        
        # Initialize answer in session state if not exists
        if f"quiz_q{i}" not in st.session_state:
            st.session_state[f"quiz_q{i}"] = None
        
        # Create radio buttons for options
        user_answer = st.radio(
            f"Select your answer for Q{i+1}:",
            q["options"],
            key=f"quiz_radio_{i}",
            index=None
        )
        
        # Store answer
        st.session_state[f"quiz_q{i}"] = user_answer
        
        # Check answer if submitted
        if user_answer == q["answer"]:
            st.success("✅ Correct!")
            score += 10
        elif user_answer is not None:
            st.error(f"❌ Wrong! Correct answer: {q['answer']}")
    
    if st.button("Submit Quiz"):
        st.session_state.total_score += score
        st.session_state.games_played += 1
        st.balloons()
        st.success(f"🎉 Quiz Completed! Your score: {score} points")
        st.info(f"Total Games Played: {st.session_state.games_played}")
        st.info(f"Overall Score: {st.session_state.total_score}")

# Dice Roller Game
elif game_choice == "🎲 Dice Roller":
    st.header("🎲 Dice Roller Game")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Roll the Dice")
        if st.button("🎲 Roll Dice", use_container_width=True):
            dice_roll = random.randint(1, 6)
            st.session_state.last_roll = dice_roll
            
            # Calculate score
            if dice_roll == 6:
                points = 50
                message = "🎉 Jackpot! You rolled a 6!"
            elif dice_roll >= 4:
                points = 20
                message = "👍 Good roll!"
            else:
                points = 5
                message = "🎯 Try again!"
            
            st.session_state.total_score += points
            st.session_state.games_played += 1
            
            st.success(f"You rolled: **{dice_roll}**")
            st.success(f"{message}")
            st.success(f"Points earned: **{points}**")
    
    with col2:
        st.subheader("Last Roll")
        if 'last_roll' in st.session_state:
            st.markdown(f"<h1 style='text-align: center; font-size: 4rem;'>{st.session_state.last_roll}</h1>", 
                       unsafe_allow_html=True)
        else:
            st.info("No rolls yet")
    
    with col3:
        st.subheader("Dice Values")
        dice_data = pd.DataFrame({
            'Roll': [1, 2, 3, 4, 5, 6],
            'Points': [5, 5, 5, 20, 20, 50]
        })
        st.dataframe(dice_data, use_container_width=True)

# Memory Game
elif game_choice == "🧠 Memory Game":
    st.header("🧠 Memory Game")
    
    # Initialize memory board
    if st.session_state.memory_board is None:
        symbols = ['🎮', '🎯', '🎲', '🎨', '🎪', '🎭', '🎸', '🎺'] * 2
        random.shuffle(symbols)
        st.session_state.memory_board = symbols
        st.session_state.memory_flipped = []
        st.session_state.memory_matched = []
        st.session_state.memory_last_click = None
    
    # Create game board
    st.write("Click on cards to flip them. Match pairs!")
    
    # Create 4x4 grid
    cols = st.columns(4)
    for i in range(16):
        col_idx = i % 4
        with cols[col_idx]:
            if i in st.session_state.memory_matched:
                st.button(st.session_state.memory_board[i], 
                         key=f"mem_{i}", 
                         disabled=True,
                         use_container_width=True)
            elif i in st.session_state.memory_flipped:
                st.button(st.session_state.memory_board[i], 
                         key=f"mem_{i}",
                         on_click=lambda idx=i: flip_card(idx),
                         use_container_width=True)
            else:
                st.button("❓", 
                         key=f"mem_{i}",
                         on_click=lambda idx=i: flip_card(idx),
                         use_container_width=True)
    
    # Game status
    matched_pairs = len(st.session_state.memory_matched) // 2
    if matched_pairs == 8:
        st.balloons()
        st.success(f"🎉 You won! All pairs matched!")
        points = 40 - len(st.session_state.memory_flipped)
        st.success(f"Score earned: {points} points")
        st.session_state.total_score += max(5, points)
        st.session_state.games_played += 1
    
    st.write(f"**Matched pairs:** {matched_pairs}/8")
    
    if st.button("🔄 Reset Memory Game"):
        st.session_state.memory_board = None
        st.rerun()

def flip_card(index):
    """Handle card flipping in memory game"""
    if index in st.session_state.memory_matched:
        return
    
    if index not in st.session_state.memory_flipped:
        st.session_state.memory_flipped.append(index)
    
    if len(st.session_state.memory_flipped) == 2:
        idx1, idx2 = st.session_state.memory_flipped
        if st.session_state.memory_board[idx1] == st.session_state.memory_board[idx2]:
            st.session_state.memory_matched.extend([idx1, idx2])
        st.session_state.memory_flipped = []
    st.rerun()

# Rock Paper Scissors Game
elif game_choice == "✂️ Rock Paper Scissors":
    st.header("✂️ Rock Paper Scissors")
    
    choices = ["✊ Rock", "✋ Paper", "✂️ Scissors"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Your Choice")
        user_choice = st.radio("Select:", choices, key="rps_user")
        
        if st.button("Play!", use_container_width=True):
            computer_choice = random.choice(choices)
            st.session_state.rps_computer = computer_choice
            
            # Determine winner
            if user_choice == computer_choice:
                result = "It's a tie!"
                points = 2
            elif (user_choice == "✊ Rock" and computer_choice == "✂️ Scissors") or \
                 (user_choice == "✋ Paper" and computer_choice == "✊ Rock") or \
                 (user_choice == "✂️ Scissors" and computer_choice == "✋ Paper"):
                result = "🎉 You win!"
                points = 10
            else:
                result = "💻 Computer wins!"
                points = 0
            
            st.session_state.rps_result = result
            st.session_state.rps_points = points
            st.session_state.total_score += points
            st.session_state.games_played += 1
    
    with col2:
        st.subheader("Computer's Choice")
        if 'rps_computer' in st.session_state:
            st.markdown(f"<h1 style='text-align: center; font-size: 3rem;'>{st.session_state.rps_computer}</h1>", 
                       unsafe_allow_html=True)
        else:
            st.info("Waiting for your move...")
    
    with col3:
        st.subheader("Result")
        if 'rps_result' in st.session_state:
            st.markdown(f"<h2 style='text-align: center;'>{st.session_state.rps_result}</h2>", 
                       unsafe_allow_html=True)
            if 'rps_points' in st.session_state:
                st.success(f"Points earned: {st.session_state.rps_points}")
        
        st.markdown("---")
        st.write("**Rules:**")
        st.write("• Rock beats Scissors")
        st.write("• Paper beats Rock")
        st.write("• Scissors beats Paper")

# Game Statistics
elif game_choice == "📊 Game Stats":
    st.header("📊 Game Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="score-board">', unsafe_allow_html=True)
        st.metric("Total Games Played", st.session_state.games_played)
        st.metric("Total Score", st.session_state.total_score)
        if st.session_state.games_played > 0:
            avg_score = st.session_state.total_score / st.session_state.games_played
            st.metric("Average Score", f"{avg_score:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Create a sample progress chart
        progress_data = pd.DataFrame({
            'Metric': ['Games Played', 'Score Progress'],
            'Value': [
                min(st.session_state.games_played, 100),
                min(st.session_state.total_score / 500 * 100, 100)
            ]
        })
        
        st.subheader("Progress")
        for _, row in progress_data.iterrows():
            st.write(f"{row['Metric']}:")
            st.progress(int(row['Value']))
    
    # Achievement system
    st.subheader("🏆 Achievements")
    achievements = []
    
    if st.session_state.games_played >= 5:
        achievements.append("🎮 Game Enthusiast (Played 5+ games)")
    if st.session_state.total_score >= 100:
        achievements.append("⭐ Scoring Star (100+ points)")
    if st.session_state.games_played >= 10:
        achievements.append("🏆 Veteran Player (10+ games)")
    
    if achievements:
        for achievement in achievements:
            st.success(achievement)
    else:
        st.info("Keep playing to unlock achievements!")
    
    # Export data option
    st.subheader("Export Your Data")
    if st.button("📥 Download Stats as CSV"):
        stats_data = pd.DataFrame({
            'Statistic': ['Games Played', 'Total Score', 'Average Score'],
            'Value': [
                st.session_state.games_played,
                st.session_state.total_score,
                st.session_state.total_score / max(st.session_state.games_played, 1)
            ]
        })
        csv = stats_data.to_csv(index=False)
        st.download_button(
            label="Click to download",
            data=csv,
            file_name="game_stats.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Made with ❤️ using Streamlit | "
    "Save to GitHub with 'app.py' and 'requirements.txt'"
    "</div>",
    unsafe_allow_html=True
)

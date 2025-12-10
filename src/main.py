
import streamlit as st
import time
import pandas as pd
from puzzle_generator import generate_puzzle
from tracker import PerformanceTracker
from adaptive_engine import determine_next_difficulty
import streamlit.components.v1 as components

# --- Setup & Initialization ---
def initialize_session():
    if 'tracker' not in st.session_state:
        st.session_state.tracker = PerformanceTracker()
    if 'current_difficulty' not in st.session_state:
        st.session_state.current_difficulty = 'Easy' # User can change start diff, but default
    if 'current_puzzle' not in st.session_state:
        st.session_state.current_puzzle = None
    if 'question_start_time' not in st.session_state:
        st.session_state.question_start_time = None
    if 'session_active' not in st.session_state:
        st.session_state.session_active = False
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    # We use a unique key for the input widget to force reset it
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0

def start_new_session():
    st.session_state.session_active = True
    st.session_state.tracker = PerformanceTracker()
    st.session_state.current_puzzle = None
    st.session_state.input_key = 0

def process_submission():
    """Callback for answer submission."""
    # This runs BEFORE the script rerun
    # Get the value from the input state
    val = st.session_state.get(f"answer_input_{st.session_state.input_key}", "")
    
    # Check if input is valid number
    try:
        user_num = int(val)
    except ValueError:
        # If empty or not a number, just return (do nothing, let user type more)
        # Or we could show a warning? For now, we assume user might have hit enter by mistake.
        # But if they hit enter on empty, we probably shouldn't penalize them yet or change question.
        # However, `on_change` fires on Enter. If empty, maybe ignore.
        return

    puzzle = st.session_state.current_puzzle
    if puzzle:
        end_time = time.time()
        start_time = st.session_state.question_start_time
        time_taken = end_time - start_time
        
        correct = (user_num == puzzle['answer'])
        
        # Log
        st.session_state.tracker.log_attempt(
            difficulty=puzzle['difficulty'],
            correct=correct,
            time_taken=time_taken
        )
        
        # Adapt
        recent_history = st.session_state.tracker.get_recent_history(5)
        new_diff = determine_next_difficulty(
            st.session_state.current_difficulty,
            recent_history
        )
        st.session_state.current_difficulty = new_diff
        
        # Feedback (stored in state to display after rerun)
        st.session_state.last_feedback = (correct, time_taken, puzzle['answer'])
        
        # Reset Puzzle
        st.session_state.current_puzzle = None
        st.session_state.input_key += 1 # Force new input widget

# --- Javascript Stopwatch ---
def stopwatch_component():
    # Simple JS to update a div with time elapsed
    # We pass the start time (ms) to JS
    # Streamlit re-renders trigger this, so we need to be careful not to reset it?
    # Actually, we just start counting from 0 when the question loads.
    # Or, we can calculate offset from server start time?
    # Let's just run a timer from 0 when this component mounts.
    
    js = """
    <script>
    function startTimer(duration, display) {
        var start = Date.now();
        var timer = setInterval(function () {
            var diff = Date.now() - start;
            var ms = diff % 1000;
            var s = Math.floor(diff / 1000);
            var m = Math.floor(s / 60);
            s = s % 60;
            
            s = s < 10 ? "0" + s : s;
            ms = ms < 10 ? "00" + ms : (ms < 100 ? "0" + ms : ms);
            
            display.textContent = m + ":" + s + ":" + ms;
        }, 33);
    }
    window.onload = function () {
        var display = document.querySelector('#time-display');
        if(display) startTimer(0, display);
    };
    // Also try running immediately in case window loaded
    var display = document.querySelector('#time-display');
    if(display) startTimer(0, display);
    </script>
    <div style="font-size: 24px; font-weight: bold; color: #333;">
        Time: <span id="time-display">00:00:000</span>
    </div>
    """
    components.html(js, height=50)

# --- Main App ---
def main():
    st.set_page_config(page_title="Adaptive Math", page_icon="🧮", layout="wide")
    initialize_session()

    st.title("🧮 Adaptive Math Tutor")

    # Side Bar
    with st.sidebar:
        st.header("Session Info")
        if st.session_state.session_active:
            metrics = st.session_state.tracker.get_metrics()
            st.metric("Total questions", metrics['total_attempts'])
            st.metric("Accuracy", f"{metrics['accuracy']:.1f}%")
            st.metric("Level", st.session_state.current_difficulty)
            
            if st.button("End Session"):
                st.session_state.session_active = False
                st.rerun()

    if not st.session_state.session_active:
        # END / START SCREEN
        metrics = st.session_state.tracker.get_metrics()
        if metrics['total_attempts'] > 0:
            st.success(f"Session Completed! Final Accuracy: {metrics['accuracy']:.1f}%")
            
            # --- Visualizations & CSV ---
            st.subheader("Performance Analysis")
            
            # Get Data
            df = st.session_state.tracker.get_data_frame()
            if not df.empty:
                # 1. Line Chart: Time vs Question
                st.write("### Response Time per Question")
                st.line_chart(df['time_taken'])
                
                # 2. Metric Breakdown
                # Maybe bar chart of accuracy by difficulty?
                st.write("### Accuracy by Difficulty")
                if 'difficulty' in df.columns:
                    # Group by difficulty
                    # We need to manually compute accuracy per group safely
                    diff_stats = df.groupby('difficulty').apply(
                        lambda x: pd.Series({
                            'accuracy': (x['correct'].sum() / len(x)) * 100
                        })
                    ).reset_index()
                    st.bar_chart(diff_stats, x='difficulty', y='accuracy')

                # CSV Download
                csv_data = st.session_state.tracker.get_data_as_csv()
                st.download_button(
                    label="📥 Download Session CSV",
                    data=csv_data,
                    file_name='math_session_report.csv',
                    mime='text/csv'
                )

        st.markdown("---")
        st.header("New Session")
        st.session_state.user_name = st.text_input("Enter User Name", value=st.session_state.user_name)
        st.session_state.current_difficulty = st.selectbox("Start Difficulty", ["Easy", "Medium", "Hard"])
        
        if st.button("Start Learning"):
            if st.session_state.user_name:
                start_new_session()
                st.rerun()
            else:
                st.error("Please enter a name.")

    else:
        # ACTIVE GAME LOOP
        
        # Feedback from previous?
        if 'last_feedback' in st.session_state:
            correct, t_taken, ans = st.session_state.last_feedback
            if correct:
                st.success(f"✅ Correct! Took {t_taken:.2f}s")
            else:
                st.error(f"❌ Incorrect. Answer was {ans}")
            del st.session_state.last_feedback
            
        # Generate new puzzle if needed
        if st.session_state.current_puzzle is None:
            st.session_state.current_puzzle = generate_puzzle(st.session_state.current_difficulty)
            st.session_state.question_start_time = time.time()
            
        puzzle = st.session_state.current_puzzle
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### Level: **{puzzle['difficulty']}**")
            st.markdown(f"# {puzzle['question_text']} = ?")
        
        with col2:
            stopwatch_component()
            
        # Input - Text input for blank default (no '0')
        # We use a dynamic key to force the input to clear/refresh
        input_key = f"answer_input_{st.session_state.input_key}"
        
        # JS for autofocusing the text input
        # We use a timeout to ensure the element exists after Streamlit render
        input_label = "Type answer and press Enter:"
        components.html(
            f"""
            <script>
                setTimeout(function() {{
                    const input = window.parent.document.querySelector('input[aria-label="{input_label}"]');
                    if (input) {{
                        input.focus();
                    }}
                }}, 50);
            </script>
            """,
            height=0, width=0
        )

        st.text_input(
            input_label,
            value="",
            placeholder="",
            key=input_key,
            on_change=process_submission
        )
        st.caption("Press Enter to submit.")

if __name__ == "__main__":
    main()

# Adaptive Math Learning App

A Streamlit-based web application designed for children aged 5–10 to practice math. The app features an adaptive difficulty engine that adjusts problem difficulty based on the user's accuracy and response time.

## Features
- **Adaptive Difficulty**: Dynamically switches between Easy, Medium, and Hard.
- **Real-time Feedback**: Immediate visual feedback for correct/incorrect answers.
- **Performance Tracking**: Tracks accuracy, response time, and detailed session history.
- **Interactive UI**: Stopwatch, progress metrics, and "Enter-to-Submit" for smooth usage.
- **Reporting**: Downloadable CSV reports and performance charts at the end of each session.

## Installation

1. **Prerequisites**
   - Python 3.8 or higher
   - `pip`

2. **Setup**
   Navigate to the project directory:
   ```bash
   git clone https://github.com/himanshugohil10/math-adaptive-prototype.git
   ```

   Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Application**
   The source code is located in the `src` directory. Run the app using:
   ```bash
   streamlit run src/main.py
   ```

2. **How to Play**
   - Enter your name and select a starting difficulty.
   - Solve the math problems displayed.
   - Type your answer and press **Enter**.
   - Watch your stats (Accuracy, Level) update in real-time.
   - Click **End Session** to view your summary and download the report.

## Project Structure
- `src/main.py`: Main application entry point and UI logic.
- `src/puzzle_generator.py`: logic for generating math problems based on difficulty.
- `src/adaptive_engine.py`: Rules for difficulty adjustment.
- `src/tracker.py`: Performance metrics and history management.

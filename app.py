"""
Simple Question-Answer Chatbot using Flask
This chatbot reads answers from text files and responds to user questions.
"""

from flask import Flask, request, jsonify, render_template
from pathlib import Path
import re

# Initialize Flask app
app = Flask(__name__)

# Define base directories
BASE_DIR = Path(__file__).parent
KB_DIR = BASE_DIR / "knowledge_base"

# Default message when question is unclear
FALLBACK_MESSAGE = "I'm not sure I understand. Could you please rephrase your question or mention your year (1st, 2nd, 3rd, or 4th year)?"


# ✅ HOME ROUTE → Loads the chat interface in browser
@app.route("/")
def home():
    """Serve the main chat HTML page"""
    return render_template("chat.html")


def load_year_content(year: int) -> str:
    """
    Load content from a year-specific text file
    
    Args:
        year: The year number (1, 2, 3, or 4)
    
    Returns:
        Content of the file as a string, or empty string if file doesn't exist
    """
    file_path = KB_DIR / f"year{year}.txt"
    if not file_path.exists():
        return ""
    return file_path.read_text(encoding="utf-8")


def detect_year(question: str) -> int:
    """
    Detect which year the student is asking about from their question
    
    Args:
        question: The user's question text
    
    Returns:
        Year number (1, 2, 3, or 4), or 0 if not detected
    """
    question = question.lower()
    
    # Check for year patterns (1st, first, year 1, etc.)
    if re.search(r'\b(1st|first|one|year\s*1)\b', question):
        return 1
    elif re.search(r'\b(2nd|second|two|year\s*2)\b', question):
        return 2
    elif re.search(r'\b(3rd|third|three|year\s*3)\b', question):
        return 3
    elif re.search(r'\b(4th|fourth|four|year\s*4)\b', question):
        return 4
    
    return 0


def find_relevant_answer(question: str, content: str) -> str:
    """
    Find the most relevant answer from content based on keywords in the question
    
    Args:
        question: The user's question
        content: The knowledge base content to search in
    
    Returns:
        Relevant answer text or empty string
    """
    if not content:
        return ""
    
    question_lower = question.lower()
    content_lines = content.split('\n')
    
    # Extract keywords from question (ignore common words)
    common_words = {'what', 'is', 'are', 'the', 'a', 'an', 'how', 'when', 'where', 'why', 'should', 'i', 'am', 'do', 'does', 'can', 'could'}
    question_words = set(re.findall(r'\b\w+\b', question_lower)) - common_words
    
    # Score each line based on keyword matches
    scored_lines = []
    for line in content_lines:
        if not line.strip():
            continue
        line_lower = line.lower()
        # Count how many question keywords appear in this line
        matches = sum(1 for word in question_words if word in line_lower)
        if matches > 0:
            scored_lines.append((matches, line))
    
    # If we found relevant lines, return the best matches
    if scored_lines:
        scored_lines.sort(reverse=True, key=lambda x: x[0])
        # Return top 3 most relevant lines
        top_lines = [line for _, line in scored_lines[:3]]
        return '\n'.join(top_lines)
    
    # If no specific match, return the full content
    return content.strip()


# ✅ CHAT ENDPOINT → Handles POST requests with user questions
@app.route("/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint that processes user questions
    
    Expected JSON input: {"query": "user question here"}
    Returns JSON: {"answer": "bot response"}
    """
    # Get JSON data from request
    data = request.get_json()
    
    # Extract the question, default to empty string if not provided
    question = data.get("query", "").strip() if data else ""
    
    # Validate input
    if not question:
        return jsonify({"answer": "Please enter a question."}), 400
    
    # Try to detect which year the user is asking about
    detected_year = detect_year(question)
    
    # If year is detected, load that year's content
    if detected_year > 0:
        content = load_year_content(detected_year)
        if content:
            # Find relevant answer from the content
            answer = find_relevant_answer(question, content)
            if answer:
                return jsonify({"answer": answer})
    
    # If no year detected or no content found, try searching all years
    all_content = []
    for year in [1, 2, 3, 4]:
        content = load_year_content(year)
        if content:
            relevant = find_relevant_answer(question, content)
            if relevant:
                all_content.append(f"[Year {year}]\n{relevant}")
    
    # If we found relevant content from any year, return it
    if all_content:
        return jsonify({"answer": "\n\n".join(all_content)})
    
    # If nothing found, return fallback message
    return jsonify({"answer": FALLBACK_MESSAGE})


# ✅ RUN THE APP
if __name__ == "__main__":
    # Start Flask development server
    # debug=True enables auto-reload on code changes (useful for development)
    app.run(host="0.0.0.0", port=5000, debug=True)
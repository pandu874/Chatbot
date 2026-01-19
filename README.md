# College Q&A Chatbot

A beginner-friendly question-answer chatbot built with Python Flask and HTML/JavaScript. The chatbot reads answers from text files and responds to user questions through a web interface.

## 📁 Project Structure

```
chatbot/
│
├── app.py                 # Flask backend (main application)
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/
│   └── chat.html         # Frontend UI (HTML + JavaScript)
│
└── knowledge_base/
    ├── year1.txt         # Knowledge base for 1st year
    ├── year2.txt         # Knowledge base for 2nd year
    ├── year3.txt         # Knowledge base for 3rd year
    └── year4.txt         # Knowledge base for 4th year
```

## 🚀 How to Run the Project

### Step 1: Install Python
Make sure you have Python 3.7 or higher installed on your computer.
- Check your Python version: `python --version` or `python3 --version`

### Step 2: Install Dependencies
Open a terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

Or if you're using Python 3:

```bash
pip3 install -r requirements.txt
```

### Step 3: Run the Flask App
Start the Flask server:

```bash
python app.py
```

Or:

```bash
python3 app.py
```

You should see output like:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 4: Open in Browser
Open your web browser and go to:

```
http://localhost:5000
```

or

```
http://127.0.0.1:5000
```

### Step 5: Start Chatting!
- Type your question in the input box
- Click "Send" or press Enter
- See the bot's response appear below

## 📝 How It Works

### Backend (app.py)
1. **Flask Server**: Creates a web server that listens for requests
2. **Home Route (`/`)**: Serves the HTML chat interface
3. **Chat Route (`/chat`)**: Receives questions via POST request and returns answers
4. **Year Detection**: Automatically detects which year (1st, 2nd, 3rd, 4th) from the question
5. **Keyword Matching**: Searches knowledge base files for relevant answers
6. **Response**: Returns JSON with the answer

### Frontend (chat.html)
1. **Input Box**: Where users type their questions
2. **Send Button**: Triggers the request to the backend
3. **Response Area**: Displays the bot's answer
4. **JavaScript**: Handles sending requests and displaying responses

### Knowledge Base
- Text files in `knowledge_base/` folder contain the answers
- Each file (year1.txt, year2.txt, etc.) has information for that year
- You can edit these files to add more information

## 🔧 API Endpoint

### POST /chat

**Request:**
```json
{
  "query": "What should I learn in 1st year?"
}
```

**Response:**
```json
{
  "answer": "1st Year Engineering Student Guidance\n\nStudents should focus on building strong fundamentals.\nSubjects: Engineering Mathematics, Physics, Basic Programming."
}
```

### Example using curl:
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What skills do 2nd year students need?"}'
```

## ✏️ Customizing the Chatbot

### Adding More Knowledge
Edit the text files in `knowledge_base/` folder:
- `year1.txt` - Information for 1st year students
- `year2.txt` - Information for 2nd year students
- `year3.txt` - Information for 3rd year students
- `year4.txt` - Information for 4th year students

### Changing the Port
In `app.py`, change the port number:
```python
app.run(host="0.0.0.0", port=5000, debug=True)  # Change 5000 to any port you want
```

### Modifying the UI
Edit `templates/chat.html` to change colors, layout, or add features.

## 🐛 Troubleshooting

### Port Already in Use
If you see "Address already in use", either:
- Close the other program using port 5000
- Change the port in `app.py` (see above)

### Module Not Found Error
Make sure you installed dependencies:
```bash
pip install -r requirements.txt
```

### Browser Shows "Can't Connect"
1. Make sure Flask app is running (check terminal)
2. Make sure you're using the correct URL: `http://localhost:5000`
3. Check if firewall is blocking the connection

## 📚 Learning Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **JavaScript Fetch API**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- **HTML Basics**: https://www.w3schools.com/html/

## 🎯 Next Steps (Optional Enhancements)

1. Add more knowledge base files for different topics
2. Implement chat history (save previous conversations)
3. Add user authentication
4. Deploy to cloud (Heroku, AWS, etc.)
5. Add database support for storing questions/answers
6. Implement better natural language processing

## 📄 License

This project is open source and available for educational purposes.

---

**Happy Coding! 🚀**

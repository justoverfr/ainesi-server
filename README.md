# AInesi

AInesi is an AI chatbot specialized in providing emotional and mental health support.

# Setup

- Add the following into a .env: OPENAI_API_KEY=<openai_api_key>
  PINECONE_API_KEY=<pinecone_api_key>
- Start server.py
- Use command .\ngrok.exe http 5000
- Copy generated https link and paste it into your Dialogflow Agent
- Add /dialogflow to the end of the link

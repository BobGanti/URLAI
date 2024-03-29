# URL AI with CHROMA VECTORSTORE
The URL AI Assistant is a conversational AI chatbot built using Streamlit, designed to query and understand content from specified url. 
By leveraging the power of LangChain, OpenAI's embeddings, and Streamlit's interactive capabilities, 
URL AI Assistant offers an intuitive interface for users to interact with and retrieve information from a knowledge base constructed from document content.

# Features #
  a. PDF Document Processing: PDFAI Assistant allows for the upload of PDF documents, enhancing its knowledge base with the content extracted from these documents.
  b. Conversational Interface: Built with Streamlit, the application provides a chat-like interface for querying the knowledge base in a natural, conversational manner.
  c. Customizable Prompts: Integrates with OpenAI's embeddings for customizable prompt engineering, enabling refined responses based on the content of the knowledge base.

# Installation #
Before running SMAI Assistant, ensure you have Python 3.6 or later installed. You can then install the necessary dependencies via pip:
git clone https://github.com/BobGanti/PDFAI.git
cd PDFAI
pip install -r requirements.txt

# Dependencies #
  > Streamlit
  > LangChain
  > PyMuPDF (for PDF processing)
  > dotenv (for environment variable management)

# Setup #
1. Environment Variables: Rename .env.local.example to .env.local and update the variables within to match your   
  configuration:
  a. OPENAI_API_KEY: Your OpenAI API key for embeddings and chat.
  b. INSTRUCTIONS: Default instructions for querying.
  c. ASSISTANT_PROFILE: Customize the assistant's profile.
2. Run the Application: Start the SMAI Assistant by running the Streamlit application.
  streamlit run pdfs.py

# Usage #
  > Adding Content Sources: Use the sidebar to upload PDF documents to augment the chatbot's knowledge base.
  > Interacting with the Chatbot: Enter queries in the chat input field to receive responses based on the aggregated knowledge from the specified uploaded PDFs.
  > Customization: Modify the .env.local file to tailor the assistant's behavior and responses to your preferences.

# Contributing #
Contributions are welcome! If you have suggestions for improvements or bug fixes, please open an issue or submit a pull request.

# License #
MIT License - See the LICENSE file for details.


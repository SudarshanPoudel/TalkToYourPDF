# TalkToYourPDF
This project is a simple chatbot that allows users to upload a PDF via a link and then ask questions about the content of the PDF. The chatbot uses a vector database to store and query the content and a language model to generate responses based on the PDF's information.

**Technologies Used:** 
- **Flask**: For creating the web API.
- **ChromaDB**: For storing and querying vector representations of the PDF content.
- **Gemini**: For the language model used to generate responses.
- **Python**: The programming language used for development.

## Installation and Configuration

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SudarshanPoudel/TalkToYourPDF.git
   cd TalkToYourPDF
   ```
2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Required Packages**

   ```bash
   pip install -r requirements.in
   ```

4. **Set Up API Keys**

   Create a .env file in your  project directory and add your API keys for Gemini as
   ```text
   GEMINI_API_KEY=<Your api key>
   ```
5. **Run the Flask Application**

   ```bash
   flask run
   ```

6. **Open the index file**

    Open *frontend/index.html* file using live server and start talking with your pdf. 

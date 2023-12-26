# ecoCompanion: Your Environmental Management Assistant

Welcome to the **ecoCompanion** repository! This project is dedicated to developing an assistant capable of addressing queries related to ISO 14001 and EMS (Environmental Management System) using the RAG method and the Gemini model.

## Project Overview

Our aim is to empower our model to efficiently respond to inquiries regarding ISO 14001 and EMS. We've curated a specialized corpus from an EMS course within our school semester and a relevant book. By doing so, our model focuses solely on this specific topic and politely declines to answer any questions outside its scope.

To facilitate interactions with the model, we've leveraged Chainlit, an excellent tool that simplifies building a visually appealing interface without requiring UI coding.

## Installation

Follow these steps to get the project up and running:

1. Clone this repository:
   ```bash
   git clone https://github.com/ImadSaddik/ecoCompanion.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ecoCompanion
   ```

3. Install the dependencies (assuming you have Python and pip installed):
   ```bash
   pip install -r requirements.txt
   ```
   
4. Create a new file called `.env` and place your API key to be able to use the Gemini model
    ```
    GEMINI_API_KEY=""
    ```

5. Start the app:
   ```bash
    chainlit run app.py -w
   ```

6. Enjoy using ecoCompanion!

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them.
4. Push your changes to your fork: `git push origin feature-name`.
5. Open a pull request describing your changes.

# Spry AI Writer

<center> <img width="400" height="200" alt="image" align='center' src="https://github.com/user-attachments/assets/35c6c6b6-8011-4cbc-9dea-56bfc200d755" /> </center>
<br> </br>
Spry AI Writer is a Python-based tool designed to generate AI-powered content for healthcare topics. It utilizes OpenAI's GPT2/GPT3 models to create blog posts and descriptions, streamlining content creation for healthcare professionals and organizations.
Features

    AI-Generated Content: Leverages OpenAI's GPT models to produce high-quality healthcare-related content.

    CSV Integration: Reads input data from CSV files (spry_blog.csv and spry_desc.csv) to generate corresponding content.

    Configurable Settings: Utilizes a config.toml file for easy configuration of parameters.

    Docker Support: Includes a Dockerfile for containerized deployment.

## Prerequisites

    Python 3.7 or higher

    An OpenAI API key

## Installation

    Clone the Repository:

    git clone https://github.com/Flakes342/Spry_AI_writer.git
    cd Spry_AI_writer

    Create a Virtual Environment (optional but recommended):

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    Install Dependencies:

    pip install -r requirements.txt

    Set Up Environment Variables:
    Create a .env file in the root directory and add your OpenAI API key:

    OPENAI_API_KEY=your_openai_api_key_here

## Configuration

The config.toml file allows you to customize various settings:

[settings]
input_blog_csv = "spry_blog.csv"
input_desc_csv = "spry_desc.csv"
output_directory = "output"
model = "gpt-3.5-turbo"

    input_blog_csv: Path to the CSV file containing blog topics.

    input_desc_csv: Path to the CSV file containing descriptions.

    output_directory: Directory where generated content will be saved.

    model: OpenAI model to use for content generation.

## Usage

To run the application:

python app.py

The script will read the specified CSV files, generate content using the OpenAI API, and save the output to the designated directory.
Docker Deployment

To build and run the application using Docker:

    Build the Docker Image:

    docker build -t spry-ai-writer .

    Run the Docker Container:

    docker run --env-file .env spry-ai-writer
    

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
License

This project is licensed under the MIT License. See the LICENSE file for details.

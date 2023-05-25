# MusicRecommender

MusicRecommender is an application that helps you find similar music compositions based on their musical spectrograms. By uploading your own music, it suggests similar songs that you might enjoy.

## Installation

To get started with MusicRecommender, follow these steps:

1. Clone the repository:

   ```shell
   git clone <repository-url>

2. Navigate to the project directory:
   ```shell
   cd musicRec
3. Install the required dependencies using pip:
    ```shell 
    pip install -r requirements.txt
## Usage
1. Perform database migrations:
     ```shell
     python manage.py migrate

2. Start the development server:
      ```shell
     python manage.py runserver
3. Access the application by visiting http://localhost:8000 in your web browser. To seed the database with songs, go to the <b>/init</b> route. This will seed the database with some initial data.   

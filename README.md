# Anime Image Generator

This project is a simple Flask web application that generates anime-style images using a Deep Convolutional Generative Adversarial Network (DCGAN). The application loads a pre-trained generator model, generates an image based on random noise, and serves the image via a web interface.

## Features

- **DCGAN Model Integration**: The application uses a TensorFlow/Keras model (`DCGEN.h5`) to generate anime-style images.
- **Flask Web Interface**: Provides a simple web interface where users can generate images.
- **Image Generation and Serving**: Images are generated dynamically and served directly to the user.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Flask
- TensorFlow
- Pillow (PIL)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/anime-generator.git
    cd anime-generator
    ```

2. Install the required Python packages:

    ```bash
    pip install Flask tensorflow pillow
    ```

3. Ensure the pre-trained generator model `DCGEN.h5` is located in the root directory of the project.

4. Create a `static` folder in the project directory to store the generated images:

    ```bash
    mkdir static
    ```

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/` to access the application.

3. Click on the "Generate" button to create and view a new anime-style image.

## File Structure

- `app.py`: The main Flask application script.
- `DCGEN.h5`: The pre-trained DCGAN generator model.
- `templates/index.html`: HTML file for the web interface.
- `static/`: Directory where generated images are stored temporarily.

## How It Works

1. **Loading the Model**: The pre-trained generator model (`DCGEN.h5`) is loaded when the Flask application starts.
  
2. **Generating an Image**: When a user navigates to the `/generate` route, the application generates random noise, feeds it into the DCGAN generator, and produces an image.

3. **Serving the Image**: The generated image is saved as `generated_image.png` in the `static/` directory and is served to the user as a PNG file.

## Troubleshooting

- **Model Not Found**: Ensure the `DCGEN.h5` file is in the correct directory.
- **Port Issues**: If the default port `5000` is in use, you can specify a different port by modifying the `app.run()` line in `app.py`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

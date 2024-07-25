import os
from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from database import db
from models import User
from utils.gpt_generate import chat_development
from utils.text_pp import parse_response, create_ppt
from dotenv import load_dotenv
import win32com.client
import os
import pythoncom
import subprocess
import handGesture

load_dotenv()  # This loads the .env file

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt = Bcrypt(app)
db.init_app(app)


# Configure Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', user=current_user)


@app.route('/generator', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        number_of_slide = request.form.get('number_of_slide')
        user_text = request.form.get('user_text')
        template_choice = request.form.get('template_choice')
        presentation_title = request.form.get('presentation_title')
        presenter_name = request.form.get('presenter_name')
        insert_image = 'insert_image' in request.form
        user_message = f"I want you to come up with the idea for the PowerPoint. The number of slides is {number_of_slide}. " \
                       f"The content is: {user_text}.The title of content for each slide must be unique, " \
                       f"and extract the most important keyword within two words for each slide. Summarize the content for each slide. "
        
        # assistant_response = "Slide 1: Heritage of Delhi /n Content: Introduction to Delhi as a cultural hub of India /n Overview of Delhi's historical significance and architectural marvels  /n Keyword: Cultural Heritage /n/n Slide 2: Delhi's Historical Landmarks /n Content: /n Discussion on Delhi's rich history spanning centuries /n Detailed exploration of iconic landmarks such as Red Fort, Qutub Minar, and Humayun's Tomb /n Emphasis on the architectural beauty and cultural significance of each landmark /n Keyword: Historical Landmarks /n/n Slide 3: Gastronomic Delights of Delhi /n Content: /n Introduction to Delhi's diverse culinary scene and street food culture /n Showcase of popular dishes like chaat, parathas, and kebabs /n Recommendations for must-visit food markets and iconic eateries /n Keyword: Culinary Delights /n/n Slide 4: Shopping in Delhi's Markets /n Content: /n Overview of Delhi's vibrant markets and bustling bazaars /n Highlights of shopping destinations like Chandni Chowk, Sarojini Nagar, and Dilli Haat /n Tips for bargaining, exploring hidden gems, and finding unique souvenirs /n Keyword: Vibrant Markets /n/n Slide 5: Modern Facets of Delhi /n Content: /n Discussion on Delhi's rapid urbanization and modern development /n Showcase of contemporary landmarks like Akshardham Temple and Lotus Temple /n Insight into Delhi's role as a major business and technology hub /n Keyword: Modern Development"
        assistant_response = chat_development(user_message)
        # Check the response (for debug)
        print(f"Assistant Response:\n{assistant_response}")
        slides_content = parse_response(assistant_response)
        create_ppt(slides_content, template_choice, presentation_title, presenter_name, insert_image)

    return render_template('generator.html', title='Generate')

@app.route('/presentor', methods=['GET', 'POST'])
def present():
    if request.method == 'POST':
        file = request.files['myFile']
        file_path = r"C:\Users\ky040\OneDrive\Desktop\PowerPoint-Generator-Python-Project-main\PowerPoint-Generator-Python-Project-main\uploads\ppt.pptx"
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        file.save(file_path)
        
        pythoncom.CoInitialize()
        Application = win32com.client.Dispatch("PowerPoint.Application")

        try:
            # Open the presentation
            Presentation = Application.Presentations.Open(file_path, WithWindow=False)
            # Create a folder to save the slides as images
            slides_folder = os.path.join(os.path.dirname(file_path), "Slides")
            if not os.path.exists(slides_folder):
                os.makedirs(slides_folder)
            else:
                # If the folder already exists, delete its contents
                for file in os.listdir(slides_folder):
                    file_path = os.path.join(slides_folder, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Error: {e}")
            # Export each slide as an image
            for i, slide in enumerate(Presentation.Slides):
                image_path = os.path.join(slides_folder, f"{i + 1}.png")
                slide.Export(image_path, "PNG")
            # Close the presentation
            Presentation.Close()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Quit the PowerPoint application
            Application.Quit()
        # script_path = r"C:\Users\ky040\OneDrive\Desktop\PowerPoint-Generator-Python-Project-main\PowerPoint-Generator-Python-Project-main\myapp\handGesture.py"
        # subprocess.run(["python", script_path])
        handGesture.hand_gesture()
    
    return render_template('present.html', title='Present')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory('generated', filename, as_attachment=True)

    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)

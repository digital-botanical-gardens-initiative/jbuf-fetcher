import os

from yattag import Doc
from dotenv import load_dotenv

load_dotenv()

# Check that data folder exists
data_path = os.getenv("DATA_PATH")
if not data_path:
    print("Error : no DATA_PATH")
    exit(1)

resolved_data = os.path.join(data_path, "resolved_data.json")
not_resolved_data = os.path.join(data_path, "not_resolved_data.json")

def generate_homepage(pages, list_items, progress_bars):
    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('head'):
            with tag('title'):
                text('My Responsive Homepage')

            with tag('meta', name="viewport", content="width=device-width, initial-scale=1.0"):

                with tag('style'):
                    text("""
                    /* Global Reset */
                    * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }

                    /* Centered container */
                    .container { width: 90%; max-width: 800px; margin: 20px auto; padding: 20px; border-radius: 10px; background: #f8f9fa; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }

                    /* Button Container */
                    .button-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-bottom: 20px; }
                    .button { padding: 10px 15px; background: #007BFF; color: white; text-decoration: none; border-radius: 5px; transition: 0.3s; }
                    .button:hover { background: #0056b3; }

                    /* List Styling */
                    ul { list-style: none; padding: 10px; }
                    li { padding: 8px; background: white; margin: 5px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }

                    /* Progress Bar */
                    .progress-bar-container { margin: 15px 0; }
                    .progress-bar { width: 100%; background: #eee; border-radius: 5px; overflow: hidden; }
                    .progress { height: 20px; background: green; text-align: center; color: white; border-radius: 5px; }

                    /* Responsive Design */
                    @media (max-width: 600px) {
                        .button { width: 100%; text-align: center; }
                    }
                    """)

        with tag('body'):
            with tag('div', klass="container"):
                with tag('h1'):
                    text('Welcome to My Website')

                # Button container
                with tag('div', klass="button-container"):
                    for page_name, page_url in pages.items():
                        with tag('a', klass="button", href=page_url):
                            text(page_name)

                # List container
                with tag('div', klass="container"):
                    with tag('h2'):
                        text('My List')
                    with tag('ul'):
                        for item in list_items:
                            with tag('li'):
                                text(item)

                # Progress bar container
                with tag('div', klass="container"):
                    with tag('h2'):
                        text('Progress Bars')
                    for label, percentage in progress_bars.items():
                        with tag('div', klass="progress-bar-container"):
                            with tag('p'):
                                text(label)
                            with tag('div', klass="progress-bar"):
                                with tag('div', klass="progress", style=f"width: {percentage}%;"):
                                    text(f"{percentage}%")

    return doc.getvalue()

# Example Data
pages = {"Home": "#", "Projects": "#projects", "Contact": "#contact"}
list_items = ["Learn Python", "Build a Website", "Deploy to Server"]
progress_bars = {"Python Mastery": 80, "Web Development": 60}

data_folder = str(os.getenv("DATA_PATH"))

html_file = os.path.join(data_folder, "home_page.html")

# Generate HTML and save to file
html_content = generate_homepage(pages, list_items, progress_bars)
with open(html_file, "w") as file:
    file.write(html_content)

print("Responsive HTML file generated successfully!")

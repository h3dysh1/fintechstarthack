from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        'author': 'Hedy Shi',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': '30th June 2024'
    },
    {
        'author': 'Hedy Shi',
        'title': 'Blog Post 2',
        'date_posted': '30th June 2024',
        'content': 'Second Post Content'
    }
]

@app.route("/")
def hello_world():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

if __name__== '__main__':
    app.run(debug=True)

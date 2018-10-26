from flask import Flask, render_template, request, url_for, flash, redirect
from database import Database

app = Flask(__name__)
app.config.from_pyfile('server.cfg')

"""
Use the following commands to interact with the database:
  db.get() to get all of the reviews
  db.get(id) to get a single review
  db.create(title, text, rating) to add a new review
  db.update(id, title, text, rating) to update a review
  db.delete(id) to delete a review
"""
db = Database(app)

@app.route('/')
def show_all_reviews():
    return render_template('show_all.html', movies=db.get())

@app.route('/create', methods = ['GET', 'POST'])
def create_movie():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['reviewText']
        rating = request.form.get('rating')

        db.create(title, text, rating)
        return redirect('/')
    return render_template('create_page.html', movie = None)

@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit_movie(id):
    movie = db.get(id)
    if movie:
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['reviewText']
            rating = request.form.get('rating')

            db.update(id, title, text, rating)
            return redirect('/')

    return render_template('create_page.html', movie = movie)

@app.route('/movie/<int:id>')
def movie_description(id):
    movie = db.get(id)
    return render_template('movie_page.html', movie = movie)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_movie(id):
    db.delete(id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

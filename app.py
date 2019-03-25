import markdown
from flask import Flask, url_for, request, render_template, Markup
from flask_sqlalchemy import SQLAlchemy, Pagination
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Jobs(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title_job = db.Column(db.String(255), nullable=False)
    content_job = db.Column(db.String(1000), nullable=False)
    date_update_job = db.Column(db.Date, nullable=False)
    date_created_job = db.Column(db.Date, nullable=False)
    iss_id_job = db.Column(db.Integer, nullable=False)


    def __init__(self,
                 title_job=None,
                 content_job=None,
                 date_update_job=None,
                 date_created_job=None,
                 iss_id_job=None):
        self.title_job = title_job
        self.content_job = content_job
        self.date_update_job = date_update_job
        self.date_created_job = date_created_job
        self.iss_id_job = iss_id_job
@app.route('/')
def show_job():
    page = request.args.get('page', 1, type=int)
    job = Jobs.query.paginate(per_page=20, page=page)
    date = Jobs.query.all()

    return render_template('index.html', job=job, date=date)
@app.route('/job/<string:id_job>/')
def job_detail(id_job):
    query = Jobs.query.filter_by(iss_id_job = '{}'.format(id_job)).first()
    job_title = query.title_job
    job_content = Markup(markdown.markdown(query.content_job))
    date = query.date_update_job
    return render_template('post.html',
                            content=job_content,
                            title=job_title,
                            date=date,
                            job=query)
if __name__ == '__main__':
    app.run(debug=True)
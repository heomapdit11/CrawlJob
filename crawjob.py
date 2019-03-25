from datetime import date
import requests
import os
import json
from math import ceil
from urllib.parse import urljoin
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()
# format column in db

class Jobs(Base):
    # https://docs.sqlalchemy.org/en/latest/orm/tutorial.html
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title_job = Column(String(255), nullable=False)
    content_job = Column(String(1000), nullable=False)
    date_update_job = Column(Date, nullable=False)
    date_created_job = Column(Date, nullable=False)
    iss_id_job = Column(Integer, nullable=False)

    def __init__(
        self,
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

    def __repr__(self):
        return "Jobs(title='%s', content='%s', date_update='%s', date_created='%s', iss_id='%s')" % (
            self.title_job,
            self.content_job,
            self.date_update_job,
            self.date_created_job,
            self.iss_id_job
        )
# create db
engine = create_engine('sqlite:///jobs.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
token = os.environ["api_github"]
# find num_job in 1 repo
repos_url = 'https://api.github.com/users/awesome-jobs/repos'
repos_url_token = urljoin(repos_url, '?access_token={}'.format(token))
ses_repos = requests.session()
req_repos = ses_repos.get(repos_url_token)
js_repos = json.loads(req_repos.text)
num_job = js_repos[1]['open_issues_count']
# find num_job in 1 page
iss_url = 'https://api.github.com/repos/awesome-jobs/vietnam/issues'
iss_url_token = urljoin(iss_url, '?access_token={}'.format(token))
ses_iss = requests.session()
req_iss = ses_iss.get(iss_url_token)
js_iss = json.loads(req_iss.text)
job_in_page = len(js_iss)
# Round decimal, pages
pages = ceil(num_job / job_in_page)
# Get ID list
iss_id = session.query(Jobs.iss_id_job).all()
id_total = [int(id_job[0]) for id_job in iss_id]
# iss_update = session.query(Jobs.date_update_job).all()
# update_total = [int(update_job[0]) for update_job in iss_update]
# Get information form page
for page in range(1, pages + 1):
    page_url = urljoin(iss_url, '?access_token={}&page={}'.format(token, page))
    ses_page = requests.session()
    req_page = ses_page.get(page_url)
    js_page = json.loads(req_page.text)
    for job in js_page:
        title_job = job['title']
        content_job = job['body']
        date_update = job['updated_at']
        date_update_job = (date(
            int(date_update[:4]),
            int(date_update[5:7]),
            int(date_update[8:10])
        ))
        date_created = job['created_at']
        date_created_job = (date(
            int(date_created[:4]),
            int(date_created[5:7]),
            int(date_created[8:10])
        ))
        iss_id_job = job['id']
        # check id from github
        if job['id'] in id_total:
            continue
        else:
            jobs = Jobs(
                title_job,
                content_job,
                date_update_job,
                date_created_job,
                iss_id_job
            )
            session.add(jobs)
            session.commit()


from server import db
from config import PAGINATION_PER_PAGE
from sqlalchemy import desc, or_, not_
from server.utils import send_email
# from server.models.professor import Professor


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(10000))
    professor_id = db.Column(db.String(64), db.ForeignKey('professors.net_id'))
    tags = db.Column(db.String(10000))
    required_courses = db.Column(db.String(10000))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    stale_date = db.Column(db.DateTime)
    contact_email = db.Column(db.String(10000))
    project_link = db.Column(db.String(10000))
    grad_only = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(db.DateTime, default=db.func.now(),
                              onupdate=db.func.now())

    @classmethod
    def get_posts(cls, page=None, compressed=False, descend=True,
                  active_only=False, inactive_only=False,
                  professor_id=None, keywords=None, tags=None,
                  required_courses=None, grad_only=False, stale=None):
        """
            page: current page of pagination, else None to get all posts
            compressed: True to get the compressed serialization
            descend: True to order descending by post id (creation)
            active_only: Only show active posts
            inactive_only: Only show inactive posts
            grad_only: True to only show listings for graduate listings
            professor_id: string, usually netid
            keywords: a string of keywords, exact match searched in the
                title and description of a post
            tags: a string of tags, separated by a comma; posts must have at
                least one tag
            stale: True to only show stale listings
        """

        # Build a query object
        query = Post.query
        if active_only:
            query = query.filter_by(is_active=True)
        if inactive_only:
            query = query.filter_by(is_active=False)
        if professor_id:
            query = query.filter_by(professor_id=professor_id)
        if grad_only:
            query = query.filter_by(grad_only=grad_only)
        if stale:
            query = query.filter(Post.stale_date < db.func.now())

        # search features
        if keywords:
            keywords = keywords.lower().strip()
            query = query.filter(or_(
                Post.description.contains(keywords),
                Post.title.contains(keywords)
            ))
        if tags:
            tags = tags.strip().lower().split(',')
            query = query.filter(or_(Post.tags.contains(tag) for tag in tags))
        if required_courses:
            required_courses = required_courses.strip().lower().split(',')
            unsat_courses = set(
                [x.lower() for x in Post.COURSES]
            ).difference(set(required_courses))

            query = query.filter(not_(
                or_(Post.required_courses.contains(x) for x in unsat_courses)
            ))

        if descend:
            query = query.order_by(desc(Post.id))

        number_pages = 1
        if page is None:
            posts = query.all()
            has_next = None
        else:
            pagination = query.paginate(page=page, per_page=PAGINATION_PER_PAGE)
            has_next = pagination.has_next
            posts = pagination.items
            number_pages = pagination.pages

        if compressed:
            return ([p.serialize_compressed_post for p in posts],
                    has_next, number_pages)
        else:
            return ([p.serialize for p in posts], has_next, number_pages)

    @classmethod
    def create_post(cls, title=None, description=None, professor_id=None,
                    tags=None, stale_date=None, contact_email=None,
                    project_link=None, required_courses=None, grad_only=False):
        if None in (title, description, professor_id, tags, stale_date,
                    contact_email, project_link, required_courses, grad_only):
            return None

        # if not (Professor.get_professor_by_netid(professor_id)):
        #    return None

        post = Post(
            title=title,
            description=description.replace('<br>', '\n'),
            tags=",".join(tags),
            professor_id=professor_id,
            stale_date=stale_date,
            contact_email=contact_email,
            project_link=project_link,
            required_courses=''.join(required_courses),
            grad_only=grad_only
        )
        db.session.add(post)
        db.session.commit()
        return post

    # Keep arguments in alphabetical order!
    @classmethod
    def update_post(cls, post_id,
                    description=None, is_active=None,
                    professor_id=None, tags=None,
                    required_courses=None, title=None, project_link=None,
                    contact_email=None, stale_date=None, grad_only=None):
        post = Post.get_post_by_id(post_id)
        if not post:
            return None
        if title:
            post.title = title
        if description:
            post.description = description.replace('<br>', '\n')
        if tags:
            post.tags = ",".join(tags)
        if professor_id:
            post.professor_id = professor_id
        if is_active is not None:
            post.is_active = is_active
        if project_link is not None:
            post.project_link = project_link
        if contact_email is not None:
            post.contact_email = contact_email
        if required_courses is not None:
            post.required_courses = required_courses
        if stale_date:
            post.stale_date = stale_date
        if grad_only:
            post.grad_only = grad_only

        db.session.commit()
        return post

    @classmethod
    def delete_post(cls, post_id):
        """ This method is currently not in use. """
        post = Post.get_post_by_id(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return True
        else:
            return False

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'tags': self.tags.split(','),
            'professor_id': self.professor_id,
            'is_active': self.is_active,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'stale_date': self.stale_date,
            'project_link': self.project_link,
            'contact_email': self.contact_email,
            'courses': self.required_courses.split(',') if self.required_courses
            else []
        }

    @property
    def serialize_compressed_post(self):
        return {
            'id': self.id,
            'title': self.title,
            # only 60 words
            'description': " ".join(self.description.split(" ")[:60]) + '...',
            # only 5 tags
            'tags': self.tags.split(',')[:5],
            'professor_id': self.professor_id,
            'is_active': self.is_active,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }

    @classmethod
    def empty(cls):
        return {
            'id': '',
            'title': '',
            'description': '',
            'tags': '',
            'professor_id': '',
            'is_active': '',
            'date_created': '',
            'date_modified': '',
            'stale_date': '',
            'project_link': '',
            'contact_email': '',
            'required_courses': '',
        }

    @staticmethod
    def disable_stale_posts():
        """ Triggered by a scheduler that is initialized in server/__init__.py
        Trigger interval is once per day.
        """
        print 'Running stale post scheduler.'
        stale_posts, _, _ = Post.get_posts(active_only=True, stale=True)
        print stale_posts
        for post in stale_posts:
            print 'Setting post %s to inactive.' % post['id']
            Post.update_post(post['id'], is_active=False)
            send_email(post['contact_email'],
                       'Your research listing has expired',
                       'Just to let you know!')

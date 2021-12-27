"""
The database object/handler for the api
"""
import json
from objects.Post import Post
from sqlalchemy import create_engine, MetaData, null
from sqlalchemy.orm import sessionmaker
from utils import upload_to_imgur, can_i_post_to_bodyswap, post_reddit

import json
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    """
    Alchemy API Encoder class
    Args:
        json ([type]): json encocder
    """

    def default(self, o):
        """
        Default function to encode objects
        Args:
            obj ([type]): object to encode

        Returns:
            [type]: json object
        """
        if isinstance(o.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [
                x for x in dir(o) if not x.startswith("_") and x != "metadata"
            ]:
                data = o.__getattribute__(field)
                try:
                    json.dumps(
                        data
                    )  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, o)


class Db:
    """
    Database methods for the api
    """

    def __init__(self):
        """
        Initializes the database object
        """
        self.connection_string = "sqlite:///database.db"
        self.engine = create_engine(
            self.connection_string,
            echo=False,
            connect_args={"check_same_thread": False},
        )
        self.meta = MetaData(self.engine)

    def create_db(self):
        """
        Creates the database if it does not exist
        """
        objects_to_create = [Post()]
        for post in objects_to_create:
            post.__table__.create(bind=self.engine, checkfirst=True)

    def get_posts(self):
        """
        Gets all the posts in the database

        Returns:
            [type]: A json off the posts in the database
        """
        session_maker = sessionmaker(bind=self.engine)
        session = session_maker()
        result = session.query(Post).all()
        return json.dumps(result, cls=AlchemyEncoder, sort_keys=True)

    def get_post_by_id(self, post_id):
        """
        Gets a post by id
        Args:
            post_id ([type]): id of the post to get

        Returns:
            [type]: a json of the post
        """
        session_maker = sessionmaker(bind=self.engine)
        session = session_maker()
        result = session.query(Post).get(post_id)
        return json.dumps(result, cls=AlchemyEncoder, sort_keys=True)

    def delete_post_by_id(self, post_id):
        """
        Deletes a post by id
        Args:
            post_id ([type]): id of the post to delete

        Returns:
            [type]: a json of the result
        """
        session_maker = sessionmaker(bind=self.engine)
        session = session_maker()
        result = session.query(Post).filter(Post.id == post_id).delete()
        session.commit()
        session.flush()
        return json.dumps(result, cls=AlchemyEncoder, sort_keys=True)

    def add_post(self, request):
        """
        Adds a post to the database
        Args:
            request ([type]): The request object for the post that is being added

        Returns:
            [type]: The json of the post that was added
        """
        imgur_link, _ = upload_to_imgur(request)
        post = Post(**request.form)
        post.link = imgur_link
        post.posted = 0
        session_maker = sessionmaker(bind=self.engine)
        session = session_maker()
        session.add(post)
        session.commit()
        session.flush()
        return json.dumps(post, cls=AlchemyEncoder)

    def update_post(self, post_id, edit_dictionary):
        """
        Update a post in the database

        Args:
            post_id ([type]): The id of the post to be updated
            edit_dictionary ([type]): The dictionary of edited parameters

        Returns:
            [type]: The json of the post that was updated
        """

        session_maker = sessionmaker(bind=self.engine)
        session = session_maker()
        result = session.query(Post).filter(Post.id == post_id).update(edit_dictionary)
        session.commit()
        session.flush()
        return json.dumps(result, cls=AlchemyEncoder)

    def post_post_to_reddit(self, post_id):
        """Posts a post to reddit

        Args:
            id ([type]): The id of the post to be posted

        Returns:
            [type]: A json object with the error or nothing if it was posted
        """
        session_maker = sessionmaker(bind=self.engine)
        session = session_maker()

        result = session.query(Post).filter(Post.id == post_id).one()

        if result.posted == 1:
            return {
                "error": "Post already posted",
                "could i post": can_i_post_to_bodyswap(),
            }

        subreddits = result.subreddits.split(",")
        for sub in subreddits:
            print(sub)
            if sub == "Bodyswap":
                if can_i_post_to_bodyswap() is True:
                    post_reddit(result.title, result.link, sub)
                elif can_i_post_to_bodyswap() is False:
                    return {
                        "error": "Could not post to bodyswap",
                        "could i post": can_i_post_to_bodyswap(),
                    }
            else:
                post_reddit(result.title, result.link, sub)
        result = session.query(Post).filter(Post.id == result.id).update({"posted": 1})
        session.commit()
        res = json.dumps(result, cls=AlchemyEncoder, sort_keys=True)
        print(res)
        return res

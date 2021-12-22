from sqlalchemy import create_engine, MetaData
from objects.Post import Post
from sqlalchemy.orm import sessionmaker
from AlchemyEncoder import AlchemyEncoder
import json
from sqlalchemy.orm import load_only
from sqlalchemy.sql.expression import select
from utils import upload_to_imgur, can_i_post_to_bodyswap, post_reddit
class Db():
 
    def __init__(self):
        self.connection_string = 'sqlite:///database.db' 
        self.engine = create_engine(self.connection_string , echo=False, connect_args={'check_same_thread':False})
        self.meta = MetaData(self.engine)
        pass

    def create_db(self):
        objects_to_create = [Post()]
        for object in objects_to_create:
            object.__table__.create(bind=self.engine, checkfirst=True)
            
    def get_posts(self):
        Session = sessionmaker(bind = self.engine)
        session = Session()
        result = session.query(Post).all()
        return json.dumps(result, cls=AlchemyEncoder, sort_keys=True)
    
    def get_post_by_id(self, id):
        Session = sessionmaker(bind = self.engine)
        session = Session()
        result = session.query(Post).get(id)
        return json.dumps(result, cls=AlchemyEncoder, sort_keys=True)
    
    def delete_post_by_id(self, id):
        Session = sessionmaker(bind = self.engine)
        session = Session()
        result = session.query(Post).filter(Post.id == id).delete()
        session.commit()
        session.flush()
        return json.dumps(result, cls=AlchemyEncoder, sort_keys=True)
        
    def add_post(self, request):
        imgur_link, image_string = upload_to_imgur(request)
        post = Post(**request.form)
        post.link = imgur_link
        post.posted = 0
        Session = sessionmaker(bind = self.engine)
        session = Session()
        session.add(post)
        session.commit()
        session.flush()
        return json.dumps(post, cls=AlchemyEncoder)
    
    def update_post(self,id, edit_dictionary):
        Session = sessionmaker(bind = self.engine)
        session = Session()
        result = session.query(Post).filter(Post.id == id).update(edit_dictionary)
        session.commit()
        session.flush()
        return json.dumps(result, cls=AlchemyEncoder)
    
    def post_post_to_reddit(self, id):
        Session = sessionmaker(bind = self.engine)
        session = Session()
        result = session.query(Post).filter(Post.id == id).one()
        
        if result.posted == 1:
            return {'error': 'Post already posted', 'could i post':can_i_post_to_bodyswap() }
        
        x =  result.subreddits.split(",")
        for sub  in x:
            if sub == 'bodyswap':  
                if can_i_post_to_bodyswap() == True:
                    post_reddit(result.title, result.link, sub)
                elif can_i_post_to_bodyswap() == False:
                    return {'error': 'Could not post to bodyswap', 'could i post':can_i_post_to_bodyswap() }
            else:
                post_reddit(result.title, result.link, sub)
                
        result = session.query(Post).filter(Post.id == id).update({"posted": 1})
        session.commit()
        res = json.dumps(result, cls=AlchemyEncoder, sort_keys=True)
        print(res)
        return res
        
# from datetime import datetime
# db =  Db()
# print(db.add_post({
#     'title': 'test',
#     'link': 'test',
#     'posted': 0,
#     'subreddits': 'test',
#     'scheduled': datetime.now()
# }))
# print(db.get_posts())
import datetime
from typing import List, Dict
from sqlalchemy.orm import scoped_session

from .utils import add_arguments, BaseORMHandler
from app.models.post import Post, Comment


class PostORMHandler:
    def __init__(self, handler: scoped_session):
        self.handler = handler

    @add_arguments(
        create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    def add(self, args: List[Dict]):
        if self.handler is None:
            raise Exception("has no active db handler")
        self.handler.add_all([Post.to_model(**item) for item in args])
        self.handler()

    def delete(self, args: List[Dict]):
        if self.handler is None:
            raise Exception("has no active db handler")
        for item in args:
            self.handler.query(Post).filter_by(post_id=item["post_id"]).delete()
        self.handler.commit()

    def update(self):
        if self.handler is None:
            raise Exception("has no active db handler")
        pass

    def get_post_home(self):
        if self.handler is None:
            raise Exception("has no active db handler")
        # return self.handler.query(Post).order_by(-Post.create_time).limit(30).offset(page * 30).all()
        return self.handler.query(Post).order_by(-Post.create_time).all()


class CommentORMHandler(BaseORMHandler):
    def __init__(self, handler: scoped_session):
        super().__init__(Comment, handler)

    @add_arguments(
        is_hidden=True, examine_state=1, is_topping=False,
        create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        modify_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    def add(self, args: List[Dict]):
        super().add(args)

    def delete(self, args: List[Dict], **kwargs):
        super().delete(args, comment_id="comment_id")

    def get(self, **kwargs):
        post = self.handler.query(Post).filter_by(post_id=kwargs["post_id"]).all()
        commit_list = self.handler.query(Comment).filter_by(post_id=kwargs["post_id"])\
            .order_by(Comment.floor).limit(30).offset(kwargs["page"] * 30).all()
        return post, commit_list
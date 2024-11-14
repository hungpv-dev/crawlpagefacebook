from sql.posts import Post
from sql.comments import Comment

post = Post()
comment = Comment()
post.truncate()
comment.truncate()
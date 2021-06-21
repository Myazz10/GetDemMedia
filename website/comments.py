from .models import Comment


def get_comments(name, email, message):
    comment = Comment()

    comment.name = name
    comment.email = email
    comment.message = message

    comment.save()

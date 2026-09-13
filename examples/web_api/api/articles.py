"""Article endpoints."""

from ..shikumi_lib.norms import content, method, path, related, tag
from .users import GetUser


@content
class ListArticles:
    """Return published articles."""

    method @= "GET"
    path @= "/articles"
    tag @= "articles"
    tag @= "read"


@content
class GetArticle:
    """Return one article by identifier."""

    method @= "GET"
    path @= "/articles/{article_id}"
    tag @= "articles"
    tag @= "read"
    related @= ListArticles
    related @= GetUser


@content
class CreateArticle:
    """Create a new article for the current user."""

    method @= "POST"
    path @= "/articles"
    tag @= "articles"
    tag @= "write"
    related @= GetUser

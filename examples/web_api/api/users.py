"""User endpoints."""

from ..shikumi_lib.norms import content, method, path, related, tag


@content
class GetUser:
    """Return one user by identifier."""

    method @= "GET"
    path @= "/users/{user_id}"
    tag @= "users"
    tag @= "read"


@content
class ListUsers:
    """Return the users visible to the caller."""

    method @= "GET"
    path @= "/users"
    tag @= "users"
    tag @= "read"
    related @= GetUser


@content
class UpdateUser:
    """Update mutable fields of one user."""

    method @= "PATCH"
    path @= "/users/{user_id}"
    tag @= "users"
    tag @= "write"
    related @= GetUser

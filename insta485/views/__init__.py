"""Views, one for each Insta485 page."""
from insta485.views.index import show_index
from insta485.views.account_operation import (
    login, logout, create_account, delete_account, edit_account, password
)
from insta485.views.users import show_user, show_follower, show_following
from insta485.views.posts import show_post, posts_operation
from insta485.views.explore import show_explore
from insta485.views.target_operation import (
    likes_operation, comments_operation, following_operation
)

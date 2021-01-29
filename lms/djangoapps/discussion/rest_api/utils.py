import functools
from datetime import datetime

from django.core.exceptions import ValidationError
from opaque_keys.edx.keys import CourseKey
from pytz import UTC

from lms.djangoapps.courseware.courses import get_course_by_id
from lms.djangoapps.discussion.django_comment_client.utils import (
    has_discussion_privileges,
    JsonError
)
from openedx.core.djangoapps.django_comment_common.comment_client.thread import Thread


def discussion_accessible(func):
    """
    View decorator to check if discussions are accessible to user.
    """
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        """
        Wrapper for the view that only calls the view if the user has privileges
        and discussions are accessible.
        """
        def is_discussion_blacked():
            """
            Check if discussion is in blackout period or not.
            """
            is_discussion_in_blackout = True
            for blackout in course.get_discussion_blackout_datetimes():
                if blackout['start'] < datetime.now(UTC) < blackout['end']:
                    is_discussion_in_blackout = False
            return is_discussion_in_blackout

        user = request.user
        if request.data.get('course_id'):
            course_id = request.data['course_id']
        else:
            thread = Thread(id=request.data.get('thread_id')).retrieve('course_id')
            course_id = thread.get('course_id')

        if not course_id:
            raise ValidationError({'course_id': ['This field is required.']})
        course_key = CourseKey.from_string(course_id)
        course = get_course_by_id(course_key)
        is_user_privileged = has_discussion_privileges(user, course_id)

        is_discussion_blacked_out = is_discussion_blacked()
        if is_user_privileged and is_discussion_blacked_out:
            return func(request, *args, **kwargs)
        else:
            return JsonError('Discussions are in a black out period.', status=403)
    return wrapper

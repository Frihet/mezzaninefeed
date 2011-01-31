import mezzanine.pages.models
import djangoobjfeed.models
import django.db.models
import django.contrib.auth.models
import datetime

class ContentPageFeedEntry(djangoobjfeed.models.ObjFeedEntry):
    obj = django.db.models.ForeignKey(mezzanine.pages.models.ContentPage, related_name='feed_entry')

    @classmethod
    def obj_post_save(cls, sender, instance, **kwargs):
        if instance.publish_date is not None:
            super(ContentPageFeedEntry, cls).obj_post_save(sender, instance, **kwargs)

    @classmethod
    def get_author_from_obj(cls, obj):
        return django.contrib.auth.models.User.objects.filter(is_superuser=True).all()[0]

    template = "mezzaninefeed/render_content_page_entry.%(format)s"

    @classmethod
    def copy_feeds(cls, instance, author):
        for feed in djangoobjfeed.models.UserFeed.objects.all():
            yield lambda feed_entry: True, feed.superclassobject

    @classmethod
    def on_pre_save(cls, sender, instance, **kwargs):
        # Don't allow posting back in time (= history revisionism),
        # but allow stuff to be published in the future (= good
        # planning)
        instance.posted_at = max(instance.obj.publish_date, datetime.datetime.now())

    def allowed_to_post_comment(self, user):
        return True

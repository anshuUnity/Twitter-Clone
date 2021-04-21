from django import forms
from tweets.models import Tweet, TweetComments

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['tweet_content', 'media']

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['tweet_content'].label = ""
        self.fields['media'].label = ""

        # assigning class
        self.fields['tweet_content'].widget.attrs.update({'class' : 'tweet__content'})
        self.fields['media'].widget.attrs.update({'class' : 'tweet__media'})

        self.fields['tweet_content'].widget.attrs.update({'placeholder':"What's happening?"})

class CommentForm(forms.ModelForm):
    class Meta:
        model = TweetComments
        fields = ['comment_content', 'comment_media']

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['comment_content'].label = ""
        self.fields['comment_media'].label = ""
        self.fields['comment_content'].required = True
        # assigning class
        self.fields['comment_content'].widget.attrs.update({'class' : 'comment_content'})
        self.fields['comment_media'].widget.attrs.update({'class' : 'comment_media'})

        self.fields['comment_content'].widget.attrs.update({'placeholder':"Tweet Your Reply"})

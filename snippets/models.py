from tutorial.settings import LANGUAGE_CODE
from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# pygments is a syntax highlighter
# LEXERS takes all the lexer tuples, they're of the form:
# (longname, tuple of aliases, tuple of filename patterns, tuple of mimetypes)
LEXERS = [item for item in get_all_lexers() if item[1]]
# sort by (first alias, longname)
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# get all the styles and sort
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    # Snippet model, these variables define the table columns
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,
                             default='friendly', max_length=100)
    owner = models.ForeignKey(
        'auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    # Metadata
    class Meta:
        # The default ordering for the object, for use when obtaining lists of objects
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else False
        formatter = HtmlFormatter(
            style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

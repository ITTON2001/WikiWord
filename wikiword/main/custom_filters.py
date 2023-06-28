from django import template

register = template.Library()

@register.filter
def extract_words(text):
    return text.split()

@register.filter
def wrap_span(text, word_list):
    for word in word_list:
        text = text.replace(word, f'<span>{word}</span>')
    return text

from django.test import TestCase
from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='auto', target='kn').translate(to_translate)
print(translated)

# Create your tests here.

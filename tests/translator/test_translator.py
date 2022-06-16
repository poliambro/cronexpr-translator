import unittest
from src.translator.translator import Translator
from src.translator.enums import CronField


class TestTranslator(unittest.TestCase):

    def test_should_translate_seconds_and_minutes_star_subexpression(self):
        sec_and_min_subexpression = "*"
        translated_expression = Translator.translate_seconds_and_minutes(sec_and_min_subexpression, CronField.SECOND)
        self.assertEquals(translated_expression, "every second")
        translated_expression = Translator.translate_seconds_and_minutes(sec_and_min_subexpression, CronField.MINUTE)
        self.assertEquals(translated_expression, "every minute")

    def test_should_translate_seconds_and_minutes_star_with_slash_subexpression(self):
        seconds_subexpression = "*/5"
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.SECOND)
        self.assertEquals(translated_expression, "every 5 seconds")
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.MINUTE)
        self.assertEquals(translated_expression, "every 5 minutes")

    def test_should_translate_seconds_and_minutes_slash_subexpression(self):
        seconds_subexpression = "5/20"
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.SECOND)
        self.assertEquals(translated_expression, "every 20 seconds, starting at second 5 past the minute")
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.MINUTE)
        self.assertEquals(translated_expression, "every 20 minutes, starting at minute 5 past the hour")

    def test_should_translate_seconds_and_minutes_slash_subexpression_to_every_second_when_the_first_value_is_0(self):
        seconds_subexpression = "0/20"
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.SECOND)
        self.assertEquals(translated_expression, "every 20 seconds")
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.MINUTE)
        self.assertEquals(translated_expression, "every 20 minutes")

    def test_should_translate_seconds_and_minutes_range_subexpression(self):
        seconds_subexpression = "5-10"
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.SECOND)
        self.assertEquals(translated_expression, "seconds 5 through 10 past the minute")
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.MINUTE)
        self.assertEquals(translated_expression, "minutes 5 through 10 past the hour")

    def test_should_translate_seconds_and_minutes_list_subexpression(self):
        seconds_subexpression = "0,5,10,15,20"
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.SECOND)
        self.assertEquals(translated_expression, "at 0, 5, 10, 15, and 20 seconds past the minute")
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.MINUTE)
        self.assertEquals(translated_expression, "at 0, 5, 10, 15, and 20 minutes past the hour")

    def test_should_translate_seconds_and_minutes_list_with_range_within_subexpression(self):
        seconds_subexpression = "0,5,10-15,20"
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.SECOND)
        self.assertEquals(translated_expression, "at 0, 5, 10 through 15, and 20 seconds past the minute")
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.MINUTE)
        self.assertEquals(translated_expression, "at 0, 5, 10 through 15, and 20 minutes past the hour")

    def test_should_translate_seconds_and_minutes_list_with_range_within_subexpression_when_a_range_value_is_the_last(self):
        seconds_subexpression = "0,5,10-15,20-25"
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.SECOND)
        self.assertEquals(translated_expression, "at 0, 5, 10 through 15, and 20 through 25 seconds past the minute")
        translated_expression = Translator.translate_seconds_and_minutes(seconds_subexpression, CronField.MINUTE)
        self.assertEquals(translated_expression, "at 0, 5, 10 through 15, and 20 through 25 minutes past the hour")

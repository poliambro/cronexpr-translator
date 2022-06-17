import unittest
from src.translator.translator import Translator
from src.translator.enums import CronField


class TestTranslator(unittest.TestCase):

    # SECONDS AND MINUTES
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

    # HOURS
    def test_should_translate_hours_star_subexpression(self):
        hours_subexpression = "*"
        translated_expression = Translator.translate_hours(hours_subexpression, CronField.HOUR)
        self.assertEquals(translated_expression, "every hour")

    def test_should_translate_hours_star_with_slash_subexpression(self):
        hours_subexpression = "*/5"
        translated_expression = Translator.translate_hours(hours_subexpression, CronField.HOUR)
        self.assertEquals(translated_expression, "every 5 hours")

    def test_should_translate_hours_slash_subexpression(self):
        hours_subexpression = "5/20"
        translated_expression = Translator.translate_hours(hours_subexpression, CronField.HOUR)
        self.assertEquals(translated_expression, "every 20 hours, starting at 5:00 AM")

    def test_should_translate_hours_slash_subexpression_to_every_second_when_the_first_value_is_0(self):
        hours_subexpression = "0/20"
        translated_expression = Translator.translate_hours(hours_subexpression, CronField.HOUR)
        self.assertEquals(translated_expression, "every 20 hours")

    def test_should_translate_hours_range_subexpression(self):
        hours_subexpression = "5-10"
        translated_expression = Translator.translate_hours(hours_subexpression, CronField.HOUR)
        self.assertEquals(translated_expression, "between 5:00 AM and 10:59 AM")

    def test_should_translate_hours_list_subexpression(self):
        hours_subexpression = "0,5,10,15,20"
        translated_expression = Translator.translate_hours(hours_subexpression, CronField.HOUR)
        self.assertEquals(translated_expression, "at 12:00 AM, 5:00 AM, 10:00 AM, 3:00 PM, and 8:00 PM")

    def test_should_translate_hours_list_with_range_within_subexpression(self):
        hours_subexpression = "0,5,10-15,20"
        translated_expression = Translator.translate_hours(hours_subexpression, CronField.HOUR)
        self.assertEquals(translated_expression, "at 12:00 AM, 5:00 AM, 10:00 AM through 3:59 PM, and 8:00 PM")

    def test_should_translate_hours_list_with_range_within_subexpression_when_a_range_value_is_the_last(self):
        hours_subexpression = "0,5,10-15,20-23"
        translated_expression = Translator.translate_hours(hours_subexpression, CronField.HOUR)
        self.assertEquals(translated_expression, "at 12:00 AM, 5:00 AM, 10:00 AM through 3:59 PM, and 8:00 PM "
                                                 "through 11:59 PM")

    # DAY OF MONTH
    def test_should_translate_day_of_month_star_and_question_mark_subexpression(self):
        day_of_month_subexpression = "*"
        translated_expression = Translator.translate_day_of_month(day_of_month_subexpression, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_expression, "every day")
        day_of_month_subexpression = "?"
        translated_expression = Translator.translate_day_of_month(day_of_month_subexpression, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_expression, "every day")

    def test_should_translate_day_of_month_star_with_slash_subexpression(self):
        day_of_month_subexpression = "*/5"
        translated_expression = Translator.translate_day_of_month(day_of_month_subexpression, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_expression, "every 5 days")

    def test_should_translate_day_of_month_slash_subexpression(self):
        day_of_month_subexpression = "5/20"
        translated_expression = Translator.translate_day_of_month(day_of_month_subexpression, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_expression, "every 20 days, starting on day 5 of the month")

    def test_should_translate_day_of_month_slash_subexpression_to_every_second_when_the_first_value_is_0(self):
        day_of_month_subexpression = "0/20"
        translated_expression = Translator.translate_day_of_month(day_of_month_subexpression, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_expression, "every 20 days")

    def test_should_translate_day_of_month_range_subexpression(self):
        day_of_month_subexpression = "5-10"
        translated_expression = Translator.translate_day_of_month(day_of_month_subexpression, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_expression, "between day 5 and 10 of the month")

    def test_should_translate_day_of_month_list_subexpression(self):
        day_of_month_subexpression = "1,5,10,15,20"
        translated_expression = Translator.translate_day_of_month(day_of_month_subexpression, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_expression, "on day 1, 5, 10, 15, and 20 of the month")

    def test_should_translate_day_of_month_list_with_range_within_subexpression(self):
        day_of_month_subexpression = "1,5,10-15,20"
        translated_expression = Translator.translate_day_of_month(day_of_month_subexpression, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_expression, "on day 1, 5, 10 through 15, and 20 of the month")

    def test_should_translate_day_of_month_list_with_range_within_subexpression_when_a_range_value_is_the_last(self):
        day_of_month_subexpression = "1,5,10-15,20-23"
        translated_expression = Translator.translate_day_of_month(day_of_month_subexpression, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_expression, "on day 1, 5, 10 through 15, and 20 through 23 of the month")

    def test_should_translate_last_day_of_the_month_subexpression(self):
        day_of_month_subexpression = "L"
        translated_expression = Translator.translate_day_of_month(day_of_month_subexpression, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_expression, "on the last day of the month")

    def test_should_translate_first_week_day_expression(self):
        first_week_day = "1W"
        translated_first_week_expression = Translator.translate_day_of_month(first_week_day, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_first_week_expression, "on the first week day of the month")

    def test_should_translate_nearest_week_day_expression(self):
        nearest_day_5 = "5W"
        nearest_day_10 = "W10"
        translated_near_5_expression = Translator.translate_day_of_month(nearest_day_5, CronField.DAY_OF_MONTH)
        translated_near_10_expression = Translator.translate_day_of_month(nearest_day_10, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_near_5_expression, "on the weekday nearest day 5 of the month")
        self.assertEquals(translated_near_10_expression, "on the weekday nearest day 10 of the month")

    def test_should_translate_last_week_day_expression(self):
        last_week = "LW"
        translated_last_week_expression = Translator.translate_day_of_month(last_week, CronField.DAY_OF_MONTH)
        self.assertEquals(translated_last_week_expression, "on the last weekday of the month")

import unittest

from src.translator.expression import Expression
from src.translator.translator import Translator
from src.translator.enums import CronField


class TestTranslator(unittest.TestCase):

    # SECONDS AND MINUTES
    def test_should_translate_seconds_and_minutes_star_subexpression(self):
        sec_and_min_subexpression = "*"
        translated_expression = Translator.translate_seconds_and_minutes(Expression(sec_and_min_subexpression), CronField.SECOND)
        self.assertEqual(translated_expression, "every second")
        translated_expression = Translator.translate_seconds_and_minutes(Expression(sec_and_min_subexpression), CronField.MINUTE)
        self.assertEqual(translated_expression, "every minute")

    def test_should_translate_seconds_and_minutes_star_with_slash_subexpression(self):
        seconds_subexpression = "*/5"
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.SECOND)
        self.assertEqual(translated_expression, "every 5 seconds")
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.MINUTE)
        self.assertEqual(translated_expression, "every 5 minutes")

    def test_should_translate_seconds_and_minutes_slash_subexpression(self):
        seconds_subexpression = "5/20"
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.SECOND)
        self.assertEqual(translated_expression, "every 20 seconds, starting at second 5 past the minute")
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.MINUTE)
        self.assertEqual(translated_expression, "every 20 minutes, starting at minute 5 past the hour")

    def test_should_translate_seconds_and_minutes_slash_subexpression_to_every_second_when_the_first_value_is_0(self):
        seconds_subexpression = "0/20"
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.SECOND)
        self.assertEqual(translated_expression, "every 20 seconds")
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.MINUTE)
        self.assertEqual(translated_expression, "every 20 minutes")

    def test_should_translate_seconds_and_minutes_range_subexpression(self):
        seconds_subexpression = "5-10"
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.SECOND)
        self.assertEqual(translated_expression, "seconds 5 through 10 past the minute")
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.MINUTE)
        self.assertEqual(translated_expression, "minutes 5 through 10 past the hour")

    def test_should_translate_seconds_and_minutes_list_subexpression(self):
        seconds_subexpression = "0,5,10,15,20"
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.SECOND)
        self.assertEqual(translated_expression, "at 0, 5, 10, 15, and 20 seconds past the minute")
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.MINUTE)
        self.assertEqual(translated_expression, "at 0, 5, 10, 15, and 20 minutes past the hour")

    def test_should_translate_seconds_and_minutes_list_with_range_within_subexpression(self):
        seconds_subexpression = "0,5,10-15,20"
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.SECOND)
        self.assertEqual(translated_expression, "at 0, 5, 10 through 15, and 20 seconds past the minute")
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.MINUTE)
        self.assertEqual(translated_expression, "at 0, 5, 10 through 15, and 20 minutes past the hour")

    def test_should_translate_seconds_and_minutes_list_with_range_within_subexpression_when_a_range_value_is_the_last(self):
        seconds_subexpression = "0,5,10-15,20-25"
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.SECOND)
        self.assertEqual(translated_expression, "at 0, 5, 10 through 15, and 20 through 25 seconds past the minute")
        translated_expression = Translator.translate_seconds_and_minutes(Expression(seconds_subexpression), CronField.MINUTE)
        self.assertEqual(translated_expression, "at 0, 5, 10 through 15, and 20 through 25 minutes past the hour")

    # HOURS
    def test_should_translate_hours_star_subexpression(self):
        hours_subexpression = "*"
        translated_expression = Translator.translate_hours(Expression(hours_subexpression), CronField.HOUR)
        self.assertEqual(translated_expression, "every hour")

    def test_should_translate_hours_star_with_slash_subexpression(self):
        hours_subexpression = "*/5"
        translated_expression = Translator.translate_hours(Expression(hours_subexpression), CronField.HOUR)
        self.assertEqual(translated_expression, "every 5 hours")

    def test_should_translate_hours_slash_subexpression(self):
        hours_subexpression = "5/20"
        translated_expression = Translator.translate_hours(Expression(hours_subexpression), CronField.HOUR)
        self.assertEqual(translated_expression, "every 20 hours, starting at 5:00 AM")

    def test_should_translate_hours_slash_subexpression_to_every_second_when_the_first_value_is_0(self):
        hours_subexpression = "0/20"
        translated_expression = Translator.translate_hours(Expression(hours_subexpression), CronField.HOUR)
        self.assertEqual(translated_expression, "every 20 hours")

    def test_should_translate_hours_range_subexpression(self):
        hours_subexpression = "5-10"
        translated_expression = Translator.translate_hours(Expression(hours_subexpression), CronField.HOUR)
        self.assertEqual(translated_expression, "between 5:00 AM and 10:59 AM")

    def test_should_translate_hours_list_subexpression(self):
        hours_subexpression = "0,5,10,15,20"
        translated_expression = Translator.translate_hours(Expression(hours_subexpression), CronField.HOUR)
        self.assertEqual(translated_expression, "at 12:00 AM, 5:00 AM, 10:00 AM, 3:00 PM, and 8:00 PM")

    def test_should_translate_hours_list_with_range_within_subexpression(self):
        hours_subexpression = "0,5,10-15,20"
        translated_expression = Translator.translate_hours(Expression(hours_subexpression), CronField.HOUR)
        self.assertEqual(translated_expression, "at 12:00 AM, 5:00 AM, 10:00 AM through 3:59 PM, and 8:00 PM")

    def test_should_translate_hours_list_with_range_within_subexpression_when_a_range_value_is_the_last(self):
        hours_subexpression = "0,5,10-15,20-23"
        translated_expression = Translator.translate_hours(Expression(hours_subexpression), CronField.HOUR)
        self.assertEqual(translated_expression, "at 12:00 AM, 5:00 AM, 10:00 AM through 3:59 PM, and 8:00 PM "
                                                 "through 11:59 PM")

    # DAY OF MONTH
    def test_should_translate_day_of_month_star_and_question_mark_subexpression(self):
        day_of_month_subexpression = "*"
        translated_expression = Translator.translate_day_of_month(Expression(day_of_month_subexpression))
        self.assertEqual(translated_expression, "every day")
        day_of_month_subexpression = "?"
        translated_expression = Translator.translate_day_of_month(Expression(day_of_month_subexpression))
        self.assertEqual(translated_expression, "every day")

    def test_should_translate_day_of_month_star_with_slash_subexpression(self):
        day_of_month_subexpression = "*/5"
        translated_expression = Translator.translate_day_of_month(Expression(day_of_month_subexpression))
        self.assertEqual(translated_expression, "every 5 days")

    def test_should_translate_day_of_month_slash_subexpression(self):
        day_of_month_subexpression = "5/20"
        translated_expression = Translator.translate_day_of_month(Expression(day_of_month_subexpression))
        self.assertEqual(translated_expression, "every 20 days, starting on day 5 of the month")

    def test_should_translate_day_of_month_slash_subexpression_to_every_second_when_the_first_value_is_0(self):
        day_of_month_subexpression = "1/20"
        translated_expression = Translator.translate_day_of_month(Expression(day_of_month_subexpression))
        self.assertEqual(translated_expression, "every 20 days")

    def test_should_translate_day_of_month_range_subexpression(self):
        day_of_month_subexpression = "5-10"
        translated_expression = Translator.translate_day_of_month(Expression(day_of_month_subexpression))
        self.assertEqual(translated_expression, "between day 5 and 10 of the month")

    def test_should_translate_day_of_month_list_subexpression(self):
        day_of_month_subexpression = "1,5,10,15,20"
        translated_expression = Translator.translate_day_of_month(Expression(day_of_month_subexpression))
        self.assertEqual(translated_expression, "on day 1, 5, 10, 15, and 20 of the month")

    def test_should_translate_day_of_month_list_with_range_within_subexpression(self):
        day_of_month_subexpression = "1,5,10-15,20"
        translated_expression = Translator.translate_day_of_month(Expression(day_of_month_subexpression))
        self.assertEqual(translated_expression, "on day 1, 5, 10 through 15, and 20 of the month")

    def test_should_translate_day_of_month_list_with_range_within_subexpression_when_a_range_value_is_the_last(self):
        day_of_month_subexpression = "1,5,10-15,20-23"
        translated_expression = Translator.translate_day_of_month(Expression(day_of_month_subexpression))
        self.assertEqual(translated_expression, "on day 1, 5, 10 through 15, and 20 through 23 of the month")

    def test_should_translate_last_day_of_the_month_subexpression(self):
        day_of_month_subexpression = "L"
        translated_expression = Translator.translate_day_of_month(Expression(day_of_month_subexpression))
        self.assertEqual(translated_expression, "on the last day of the month")

    def test_should_translate_first_week_day_expression(self):
        first_week_day = "1W"
        translated_first_week_expression = Translator.translate_day_of_month(Expression(first_week_day))
        self.assertEqual(translated_first_week_expression, "on the first week day of the month")

    def test_should_translate_nearest_week_day_expression(self):
        nearest_day_5 = "5W"
        nearest_day_10 = "W10"
        translated_near_5_expression = Translator.translate_day_of_month(Expression(nearest_day_5))
        translated_near_10_expression = Translator.translate_day_of_month(Expression(nearest_day_10))
        self.assertEqual(translated_near_5_expression, "on the week day nearest day 5 of the month")
        self.assertEqual(translated_near_10_expression, "on the week day nearest day 10 of the month")

    def test_should_translate_last_week_day_expression(self):
        last_week = "LW"
        translated_last_week_expression = Translator.translate_day_of_month(Expression(last_week))
        self.assertEqual(translated_last_week_expression, "on the last week day of the month")

    # MONTH
    def test_should_translate_month_star_subexpression(self):
        month_subexpression = "*"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "every month")

    def test_should_translate_month_star_with_slash_subexpression(self):
        month_subexpression = "*/5"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "every 5 months")

    def test_should_translate_month_star_with_slash_subexpression_with_alternative_value(self):
        month_subexpression = "*/oct"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "every 10 months")

    def test_should_translate_month_slash_subexpression(self):
        month_subexpression = "2/5"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "every 5 months, february through december")

    def test_should_translate_month_slash_subexpression_with_alternative_value(self):
        month_subexpression = "feb/may"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "every 5 months, february through december")

    def test_should_translate_month_slash_subexpression_to_every_second_when_the_first_value_is_1(self):
        month_subexpression = "1/7"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "every 7 months")

    def test_should_translate_month_slash_subexpression_to_every_second_when_the_first_value_is_1_with_alternative_value(self):
        month_subexpression = "1/jul"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "every 7 months")

    def test_should_translate_month_range_subexpression(self):
        month_subexpression = "5-10"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "may through october")

    def test_should_translate_month_range_subexpression_with_alternative_value(self):
        month_subexpression = "may-oct"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "may through october")

    def test_should_translate_month_list_subexpression(self):
        month_subexpression = "1,2,3,5"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "only in january, february, march, and may")

    def test_should_translate_month_list_subexpression_with_alternative_value(self):
        month_subexpression = "jan,feb,mar,may"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "only in january, february, march, and may")

    def test_should_translate_month_list_with_range_within_subexpression(self):
        month_subexpression = "1,2,3,5-7,8"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "only in january, february, march, may through july, and august")

    def test_should_translate_month_list_with_range_within_subexpression_with_alternative_value(self):
        month_subexpression = "jan,feb,mar,may-jul,aug"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "only in january, february, march, may through july, and august")

    def test_should_translate_month_list_with_range_within_subexpression_when_a_range_value_is_the_last(self):
        month_subexpression = "1,2,3,5-7,8-10"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "only in january, february, march, may through july, and august "
                                                 "through october")

    def test_should_translate_month_list_with_range_within_subexpr_when_range_value_is_the_last_with_alternative_value(self):
        month_subexpression = "jan,feb,mar,may-jul,aug-oct"
        translated_expression = Translator.translate_month(Expression(month_subexpression), CronField.MONTH)
        self.assertEqual(translated_expression, "only in january, february, march, may through july, and august "
                                                 "through october")

    # DAY OF WEEK
    def test_should_translate_day_of_week_star_subexpression(self):
        day_of_week_subexpression = "*"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "every day of the week")

    def test_should_translate_day_of_week_question_mark_subexpression(self):
        day_of_week_subexpression = "?"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "every day of the week")

    def test_should_translate_day_of_week_star_with_slash_subexpression(self):
        day_of_week_subexpression = "*/5"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "every 5 days of the week")

    def test_should_translate_day_of_week_star_with_slash_subexpression_with_alternative_value(self):
        day_of_week_subexpression = "*/fri"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "every 5 days of the week")

    def test_should_translate_day_of_week_slash_subexpression(self):
        day_of_week_subexpression = "2/5"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "every 5 days of the week, tuesday through saturday")

    def test_should_translate_day_of_week_slash_subexpression_with_alternative_value(self):
        day_of_week_subexpression = "tue/fri"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "every 5 days of the week, tuesday through saturday")

    def test_should_translate_day_of_week_slash_subexpression_to_every_day_when_the_first_value_is_1(self):
        day_of_week_subexpression = "1/7"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "every 7 days of the week, monday through saturday")

    def test_should_translate_day_of_week_slash_subexpr_to_every_day_when_the_first_value_is_1_with_alternative_value(self):
        day_of_week_subexpression = "1/wed"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "every 3 days of the week, monday through saturday")

    def test_should_translate_day_of_week_range_subexpression(self):
        day_of_week_subexpression = "2-5"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "tuesday through friday")

    def test_should_translate_day_of_week_range_subexpression_with_alternative_value(self):
        day_of_week_subexpression = "TUE-FRI"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "tuesday through friday")

    def test_should_translate_day_of_week_list_subexpression(self):
        day_of_week_subexpression = "1,2,3,5"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "only on monday, tuesday, wednesday, and friday")

    def test_should_translate_day_of_week_list_subexpression_with_alternative_value(self):
        day_of_week_subexpression = "mon,tue,wed,fri"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "only on monday, tuesday, wednesday, and friday")

    def test_should_translate_day_of_week_list_with_range_within_subexpression(self):
        day_of_week_subexpression = "1,2,3-5,6"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "only on monday, tuesday, wednesday through friday, and saturday")

    def test_should_translate_day_of_week_list_with_range_within_subexpression_with_alternative_value(self):
        day_of_week_subexpression = "mon,tue,wed-fri,sat"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "only on monday, tuesday, wednesday through friday, and saturday")

    def test_should_translate_day_of_week_list_with_range_within_subexpression_when_a_range_value_is_the_last(self):
        day_of_week_subexpression = "0,1-3,4,5-6"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "only on sunday, monday through wednesday, thursday, and friday "
                                                 "through saturday") 

    def test_should_translate_day_of_week_list_with_range_subexpr_when_range_value_is_the_last_with_alternative_value(self):
        day_of_week_subexpression = "sun,mon-wed,thu,fri-sat"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "only on sunday, monday through wednesday, thursday, and friday "
                                                 "through saturday")

    def test_should_translate_last_day_of_the_week_subexpression(self):
        day_of_week_subexpression = "L"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "only on saturday")

    def test_should_translate_last_day_of_the_week_subexpression_when_it_has_a_value(self):
        day_of_week_subexpression = "3L"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "on the last wednesday of the month")

    def test_should_translate_last_day_of_the_week_subexpression_when_it_has_a_value_with_alternative_value(self):
        day_of_week_subexpression = "wedL"
        translated_expression = Translator.translate_day_of_week(Expression(day_of_week_subexpression))
        self.assertEqual(translated_expression, "on the last wednesday of the month")

    # YEAR
    def test_should_translate_year_star_subexpression(self):
        year_subexpression = "*"
        translated_expression = Translator.translate_year(Expression(year_subexpression), CronField.YEAR)
        self.assertEqual(translated_expression, "every year")

    def test_should_translate_year_star_with_slash_subexpression(self):
        year_subexpression = "*/1985"
        translated_expression = Translator.translate_year(Expression(year_subexpression), CronField.YEAR)
        self.assertEqual(translated_expression, "every 1985 years")

    def test_should_translate_year_slash_subexpression(self):
        year_subexpression = "1990/5"
        translated_expression = Translator.translate_year(Expression(year_subexpression), CronField.YEAR)
        self.assertEqual(translated_expression, "every 5 years, 1990 through 2099")

    def test_should_translate_year_slash_subexpression_to_every_year_when_the_first_value_is_0(self):
        year_subexpression = "0/20"
        translated_expression = Translator.translate_year(Expression(year_subexpression), CronField.YEAR)
        self.assertEqual(translated_expression, "every 20 years")

    def test_should_translate_year_range_subexpression(self):
        year_subexpression = "2010-2020"
        translated_expression = Translator.translate_year(Expression(year_subexpression), CronField.YEAR)
        self.assertEqual(translated_expression, "2010 through 2020")

    def test_should_translate_year_list_subexpression(self):
        year_subexpression = "1970,1980,1990"
        translated_expression = Translator.translate_year(Expression(year_subexpression), CronField.YEAR)
        self.assertEqual(translated_expression, "only in 1970, 1980, and 1990")

    def test_should_translate_year_list_with_range_within_subexpression(self):
        year_subexpression = "1970,1980,1990-2000,2010"
        translated_expression = Translator.translate_year(Expression(year_subexpression), CronField.YEAR)
        self.assertEqual(translated_expression, "only in 1970, 1980, 1990 through 2000, and 2010")

    def test_should_translate_year_list_with_range_within_subexpression_when_a_range_value_is_the_last(self):
        year_subexpression = "1970,1980-1990,2000,2010-2020"
        translated_expression = Translator.translate_year(Expression(year_subexpression), CronField.YEAR)
        self.assertEqual(translated_expression, "only in 1970, 1980 through 1990, 2000, and 2010 through 2020")

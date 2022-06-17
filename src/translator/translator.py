from typing import Callable, Any

from src.translator.enums import CronField, AllowedCharacters
from src.translator.expression import Expression

MONTHS_MAPPER = {1: ("jan", "january"), 2: ("feb", "february"), 3: ("mar", "march"), 4: ("apr", "april"),
                 5: ("may", "may"), 6: ("jun", "june"), 7: ("jul", "july"), 8: ("aug", "august"),
                 9: ("sep", "september"), 10: ("oct", "october"), 11: ("nov", "november"), 12: ("dec", "december")}

DAY_OF_WEEK_MAPPER = {0: ("sun", "sunday"), 1: ("mon", "monday"), 2: ("tue", "tuesday"), 3: ("wed", "wednesday"),
                      4: ("thu", "thursday"), 5: ("fri", "friday"), 6: ("sat", "saturday")}


class Translator:

    @staticmethod
    def translate_seconds_and_minutes(expression: Expression, field_type: CronField) -> str:
        field_name = str(field_type.name).lower()
        past_time = f" past the {str(CronField(field_type.value + 1).name).lower()}"
        return Translator.__find_description(expression=expression,
                                             star_suffix=field_name,
                                             first_prefix_slash=f" {field_name}s",
                                             second_prefix_slash=f"starting at {field_name} ",
                                             second_suffix_slash=past_time,
                                             list_prefix="at ",
                                             list_suffix=f" {field_name}s{past_time}",
                                             range_prefix=f"{field_name}s ",
                                             range_suffix=past_time)

    @staticmethod
    def translate_hours(expression: Expression, field_type: CronField) -> str:
        field_name = str(field_type.name).lower()
        return Translator.__find_description(expression=expression,
                                             star_suffix=field_name,
                                             format_function=Translator.__get_am_pm_formatted_hour,
                                             first_prefix_slash=f" {field_name}s",
                                             second_prefix_slash=f"starting at ",
                                             apply_format_function_in_first_arg=False,
                                             list_prefix="at ",
                                             range_prefix="between ",
                                             arguments_connector="and")

    @staticmethod
    def translate_day_of_month(expression: Expression) -> str:
        if expression.is_last_week_day_expression():
            return "on the last weekday of the month"
        if expression.is_week_day_expression():
            day_of_month = [day for day in expression.expression.split(AllowedCharacters.WEEK_DAY.value) if day]
            if day_of_month[0] == "1":
                return "on the first week day of the month"
            return f"on the weekday nearest day {day_of_month[0]} of the month"
        if expression.is_last_day_expression():
            return "on the last day of the month"
        return Translator.__find_description(expression=expression,
                                             star_suffix="day",
                                             first_prefix_slash=" days",
                                             second_prefix_slash="starting on day ",
                                             second_suffix_slash=" of the month",
                                             zero_based=False,
                                             list_prefix="on day ",
                                             list_suffix=" of the month",
                                             range_prefix="between day ",
                                             range_suffix=" of the month",
                                             arguments_connector="and")

    @staticmethod
    def translate_month(expression: Expression, field_type: CronField) -> str:
        field_name = str(field_type.name).lower()
        return Translator.__find_description(expression=expression,
                                             star_suffix=field_name,
                                             format_function=Translator.__get_full_description,
                                             mapper_dict=MONTHS_MAPPER,
                                             first_prefix_slash=f" {field_name}s",
                                             second_suffix_slash=" through december",
                                             zero_based=False,
                                             list_prefix="only in ")

    @staticmethod
    def translate_day_of_week(expression: Expression) -> str:
        if expression.is_last_day_expression():
            day_of_week = [day for day in expression.expression.split(AllowedCharacters.LAST_DAY.value) if day]
            if len(day_of_week) > 0:
                return f"on the last {Translator.__get_full_description(day_of_week[0], DAY_OF_WEEK_MAPPER)} of the " \
                       f"month"
            return "only on saturday"
        return Translator.__find_description(expression=expression,
                                             star_suffix="day of the week",
                                             format_function=Translator.__get_full_description,
                                             mapper_dict=DAY_OF_WEEK_MAPPER,
                                             first_prefix_slash=f" days of the week",
                                             second_suffix_slash=" through saturday",
                                             list_prefix="only on ")

    @staticmethod
    def translate_year(expression: Expression, field_type: CronField) -> str:
        field_name = str(field_type.name).lower()
        return Translator.__find_description(expression=expression,
                                             star_suffix=field_name,
                                             first_prefix_slash=f" {field_name}s",
                                             second_suffix_slash=" through 2099",
                                             list_prefix="only in ")

    @staticmethod
    def __get_hour_period(hours: str) -> str:
        if 0 <= int(hours) < 12:
            return "AM"
        return "PM"

    @staticmethod
    def __get_am_pm_formatted_hour(value: str, **kwargs) -> str:
        is_last = kwargs.get("is_last", False)
        hour_int_value = int(value)
        if hour_int_value == 0:
            hour_int_value = 12
        if hour_int_value > 12 and is_last:
            return f"{str(hour_int_value - 12)}:59 {Translator.__get_hour_period(value)}"
        elif hour_int_value > 12 and not is_last:
            return f"{str(hour_int_value - 12)}:00 {Translator.__get_hour_period(value)}"
        elif is_last and not hour_int_value > 12:
            return f"{hour_int_value}:59 {Translator.__get_hour_period(value)}"
        return f"{hour_int_value}:00 {Translator.__get_hour_period(value)}"

    @staticmethod
    def __get_full_description(value: str, mapper_dict: dict, **kwargs) -> str:
        numeric_value = kwargs.get("numeric_value", False)
        if value.isnumeric() and numeric_value:
            return value
        if value.isalpha():
            for key in mapper_dict:
                if value.lower() == mapper_dict[key][0]:
                    if numeric_value:
                        return str(key)
                    return mapper_dict[key][1]
        return mapper_dict.get(int(value))[1]

    @staticmethod
    def __find_description(expression: Expression, **kwargs) -> str:
        star_description = Translator.__get_star_and_question_mark_description(expression, **kwargs)
        slashed_description = Translator.__get_slashed_description(expression, **kwargs)
        list_description = Translator.__get_list_description(expression, **kwargs)
        range_description = Translator.__get_range_description(expression, **kwargs)
        descriptions_list = [star_description, slashed_description, list_description, range_description]
        non_empty_descriptions = [description for description in descriptions_list if description]
        if len(non_empty_descriptions) != 1:
            return "ERROR"
        return non_empty_descriptions[0]

    @staticmethod
    def __get_star_and_question_mark_description(expression: Expression, **kwargs) -> str:
        if expression.is_star_expression() or expression.is_question_mark_expression():
            return f"every {kwargs.get('star_suffix', '')}"

    @staticmethod
    def __get_slashed_description(expression: Expression, **kwargs) -> str:
        if expression.has_slash_in_expression():
            first_prefix_slash = kwargs.get("first_prefix_slash", "")
            second_prefix_slash = kwargs.get("second_prefix_slash", "")
            second_suffix_slash = kwargs.get("second_suffix_slash", "")
            format_function = kwargs.get("format_function", None)
            mapper_dict = kwargs.get("mapper_dict", None)
            arguments = expression.expression.rsplit(AllowedCharacters.SLASH.value)
            slash_expr = f"every {arguments[1]}{first_prefix_slash}"
            if format_function and kwargs.get("apply_format_function_in_first_arg", True):
                slash_expr = f"every " \
                             f"{format_function(value=arguments[1], mapper_dict=mapper_dict, numeric_value=True)}" \
                             f"{first_prefix_slash}"
            if expression.is_slashed_star_expression(kwargs.get("zero_based", True)):
                return slash_expr
            if format_function:
                return f"{slash_expr}, {second_prefix_slash}{format_function(value=arguments[0], mapper_dict=mapper_dict)}{second_suffix_slash}"
            return f"{slash_expr}, {second_prefix_slash}{arguments[0]}{second_suffix_slash}"

    @staticmethod
    def __get_list_description(expression: Expression, **kwargs) -> str:
        if expression.is_list_expression():
            list_values = expression.expression.rsplit(AllowedCharacters.LIST.value)
            list_prefix = kwargs.get("list_prefix", "")
            list_suffix = kwargs.get("list_suffix", "")
            format_function = kwargs.get("format_function", None)
            mapper_dict = kwargs.get("mapper_dict", None)
            translation_msg = list_prefix
            for value in list_values:
                element_desc = Expression(value)
                if element_desc.is_range_expression():
                    arguments = element_desc.expression.rsplit(AllowedCharacters.RANGE.value)
                    element_desc.expression = f"{arguments[0]} through {arguments[1]}"
                    if format_function:
                        first_element = format_function(value=arguments[0], mapper_dict=mapper_dict)
                        second_element = format_function(value=arguments[1], is_last=True, mapper_dict=mapper_dict)
                        element_desc.expression = f"{first_element} through {second_element}"
                else:
                    if format_function:
                        element_desc.expression = format_function(value=element_desc.expression, mapper_dict=mapper_dict)
                if list_values[-1] == value:
                    translation_msg += f"and {element_desc.expression}{list_suffix}"
                    break
                translation_msg += f"{element_desc.expression}, "
            return translation_msg

    @staticmethod
    def __get_range_description(expression: Expression, **kwargs) -> str:
        if expression.is_range_expression():
            arguments = expression.expression.rsplit(AllowedCharacters.RANGE.value)
            format_function = kwargs.get("format_function", None)
            range_prefix = kwargs.get("range_prefix", "")
            range_suffix = kwargs.get("range_suffix", "")
            arguments_connector = kwargs.get("arguments_connector", "through")
            if format_function:
                mapper_dict = kwargs.get("mapper_dict", None)
                first_element = format_function(value=arguments[0], mapper_dict=mapper_dict)
                second_element = format_function(value=arguments[1], is_last=True, mapper_dict=mapper_dict)
                return f"{range_prefix}{first_element} {arguments_connector} {second_element}{range_suffix}"
            return f"{range_prefix}{arguments[0]} {arguments_connector} {arguments[1]}{range_suffix}"

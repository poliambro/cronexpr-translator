from src.translator.enums import CronField, AllowedCharacters
from src.translator.expression import Expression
from validator.validator import Validator

MONTHS_MAPPER = {1: ("jan", "january"), 2: ("feb", "february"), 3: ("mar", "march"), 4: ("apr", "april"),
                 5: ("may", "may"), 6: ("jun", "june"), 7: ("jul", "july"), 8: ("aug", "august"),
                 9: ("sep", "september"), 10: ("oct", "october"), 11: ("nov", "november"), 12: ("dec", "december")}

DAY_OF_WEEK_MAPPER = {0: ("sun", "sunday"), 1: ("mon", "monday"), 2: ("tue", "tuesday"), 3: ("wed", "wednesday"),
                      4: ("thu", "thursday"), 5: ("fri", "friday"), 6: ("sat", "saturday")}


class Translator:

    @staticmethod
    def translate_expression(expression: str) -> str:
        if not Validator.validate(expression):
            return "CRON EXPRESSION IS NOT VALID"
        subexpressions = expression.rsplit(AllowedCharacters.CRON_DELIMITER.value)
        second_description = Translator.translate_seconds_and_minutes(Expression(subexpressions[0]), CronField.SECOND)
        minute_description = Translator.translate_seconds_and_minutes(Expression(subexpressions[1]), CronField.MINUTE)
        hour_description = Translator.translate_hours(Expression(subexpressions[2]), CronField.HOUR)
        day_of_month_description = Translator.translate_day_of_month(Expression(subexpressions[3]))
        month_description = Translator.translate_month(Expression(subexpressions[4]), CronField.MONTH)
        day_of_week_description = Translator.translate_day_of_week(Expression(subexpressions[5]))
        year_description = None
        if len(subexpressions) == 7:
            year_description = Translator.translate_year(Expression(subexpressions[6]), CronField.YEAR)
        return f"second -> {second_description}\n" \
               f"minute -> {minute_description}\n" \
               f"hour -> {hour_description}\n" \
               f"day of month -> {day_of_month_description}\n" \
               f"month -> {month_description}\n" \
               f"day of week -> {day_of_week_description}\n" \
               f"year -> {'not informed' if not year_description else year_description}"


    @staticmethod
    def translate_seconds_and_minutes(expression: Expression, field_type: CronField) -> str:
        field_name = str(field_type.name).lower()
        past_time = f" past the {str(CronField(field_type.value + 1).name).lower()}"
        return Translator.__find_description(expression=expression,
                                             value_prefix=f"at {field_name} ",
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
        at_prefix = "at "
        return Translator.__find_description(expression=expression,
                                             value_prefix=at_prefix,
                                             star_suffix=field_name,
                                             format_function=Translator.__get_am_pm_formatted_hour,
                                             first_prefix_slash=f" {field_name}s",
                                             second_prefix_slash=f"starting at ",
                                             apply_format_function_in_first_arg=False,
                                             list_prefix=at_prefix,
                                             range_prefix="between ",
                                             arguments_connector="and")

    @staticmethod
    def translate_day_of_month(expression: Expression) -> str:
        week_day_description = Translator.__get_week_day_description(expression)
        if week_day_description:
            return week_day_description
        field_name = "day"
        on_day_prefix = f"on {field_name} "
        of_the_month_suffix = " of the month"
        return Translator.__find_description(expression=expression,
                                             value_prefix=on_day_prefix,
                                             value_suffix=of_the_month_suffix,
                                             star_suffix=f"{field_name}",
                                             first_prefix_slash=f" {field_name}s",
                                             second_prefix_slash=f"starting {on_day_prefix}",
                                             second_suffix_slash=of_the_month_suffix,
                                             zero_based=False,
                                             list_prefix=on_day_prefix,
                                             list_suffix=of_the_month_suffix,
                                             range_prefix=f"between {field_name} ",
                                             range_suffix=of_the_month_suffix,
                                             arguments_connector="and",
                                             find_last_day=True,
                                             default_last_day=f"on the last {field_name}{of_the_month_suffix}")

    @staticmethod
    def translate_month(expression: Expression, field_type: CronField) -> str:
        field_name = str(field_type.name).lower()
        only_in_prefix = "only in "
        return Translator.__find_description(expression=expression,
                                             value_prefix=only_in_prefix,
                                             star_suffix=field_name,
                                             format_function=Translator.__get_full_description,
                                             mapper_dict=MONTHS_MAPPER,
                                             first_prefix_slash=f" {field_name}s",
                                             second_suffix_slash=" through december",
                                             zero_based=False,
                                             list_prefix=only_in_prefix)

    @staticmethod
    def translate_day_of_week(expression: Expression) -> str:
        only_on_prefix = "only on "
        return Translator.__find_description(expression=expression,
                                             value_prefix=only_on_prefix,
                                             star_suffix="day of the week",
                                             format_function=Translator.__get_full_description,
                                             mapper_dict=DAY_OF_WEEK_MAPPER,
                                             first_prefix_slash=f" days of the week",
                                             second_suffix_slash=" through saturday",
                                             list_prefix=only_on_prefix,
                                             find_last_day=True,
                                             last_day_prefix="on the last ",
                                             last_day_suffix=" of the month",
                                             default_last_day="only on saturday")

    @staticmethod
    def translate_year(expression: Expression, field_type: CronField) -> str:
        field_name = str(field_type.name).lower()
        only_in_prefix = "only in "
        return Translator.__find_description(expression=expression,
                                             value_prefix=only_in_prefix,
                                             star_suffix=field_name,
                                             first_prefix_slash=f" {field_name}s",
                                             second_suffix_slash=" through 2099",
                                             list_prefix=only_in_prefix)

    @staticmethod
    def __get_week_day_description(expression: Expression) -> str:
        if expression.is_week_day_expression():
            day_of_month = [day for day in expression.expression.split(AllowedCharacters.WEEK_DAY.value) if day]
            if len(day_of_month) > 0:
                first = "first" if day_of_month[0] == "1" else ""
                last = "last" if day_of_month[0] == AllowedCharacters.LAST_DAY.value else ""
                if not first and not last:
                    return f"on the week day nearest day {day_of_month[0]} of the month"
                return f"on the {first}{last} week day of the month"

    @staticmethod
    def __get_hour_period(hours: str) -> str:
        return "AM" if 0 <= int(hours) < 12 else "PM"

    @staticmethod
    def __get_am_pm_formatted_hour(value: str, **kwargs) -> str:
        am_or_pm = Translator.__get_hour_period(value)
        hour_int_value = int(value)
        if hour_int_value == 0:
            hour_int_value = 12
        first_arg = str(hour_int_value - 12) if hour_int_value > 12 else str(hour_int_value)
        is_last = kwargs.get("is_last", False)
        return f"{first_arg}{':00' if not is_last else ':59'} {am_or_pm}"

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
    def __get_last_day_description(expression: Expression, **kwargs) -> str:
        if expression.is_last_day_expression():
            days = [day for day in expression.expression.split(AllowedCharacters.LAST_DAY.value) if day]
            if len(days) > 0:
                format_function = kwargs.get("format_function", None)
                last_day_prefix = kwargs.get("last_day_prefix", "")
                last_day_suffix = kwargs.get("last_day_suffix", "")
                if format_function:
                    mapper_dict = kwargs.get("mapper_dict", None)
                    return f"{last_day_prefix}" \
                           f"{format_function(value=days[0], mapper_dict=mapper_dict)}{last_day_suffix}"
                return f"{last_day_prefix}{days[0]}{last_day_suffix}"
            return kwargs.get("default_last_day")

    @staticmethod
    def __get_star_and_question_mark_description(expression: Expression, **kwargs) -> str:
        if expression.is_star_expression() or expression.is_question_mark_expression():
            return f"every {kwargs.get('star_suffix', '')}"

    @staticmethod
    def __get_slashed_description(expression: Expression, **kwargs) -> str:
        if expression.has_slash_in_expression():
            first_prefix_slash = kwargs.get("first_prefix_slash", "")
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
            second_prefix_slash = kwargs.get("second_prefix_slash", "")
            second_suffix_slash = kwargs.get("second_suffix_slash", "")
            if format_function:
                return f"{slash_expr}, {second_prefix_slash}" \
                       f"{format_function(value=arguments[0], mapper_dict=mapper_dict)}{second_suffix_slash}"
            return f"{slash_expr}, {second_prefix_slash}{arguments[0]}{second_suffix_slash}"

    @staticmethod
    def __get_list_description(expression: Expression, **kwargs) -> str:
        if expression.is_list_expression():
            list_values = expression.expression.rsplit(AllowedCharacters.LIST.value)
            list_prefix = kwargs.get("list_prefix", "")
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
                        element_desc.expression = format_function(value=element_desc.expression,
                                                                  mapper_dict=mapper_dict)
                if list_values[-1] == value:
                    list_suffix = kwargs.get("list_suffix", "")
                    translation_msg += f"and {element_desc.expression}{list_suffix}"
                    break
                translation_msg += f"{element_desc.expression}, "
            return translation_msg

    @staticmethod
    def __get_range_description(expression: Expression, **kwargs) -> str:
        if expression.is_range_expression():
            arguments = expression.expression.rsplit(AllowedCharacters.RANGE.value)
            format_function = kwargs.get("format_function", None)
            first_element = arguments[0]
            second_element = arguments[1]
            if format_function:
                mapper_dict = kwargs.get("mapper_dict", None)
                first_element = format_function(value=arguments[0], mapper_dict=mapper_dict)
                second_element = format_function(value=arguments[1], is_last=True, mapper_dict=mapper_dict)
            return f"{kwargs.get('range_prefix', '')}{first_element} {kwargs.get('arguments_connector', 'through')} " \
                   f"{second_element}{kwargs.get('range_suffix', '')}"

    @staticmethod
    def __get_value_description(expression: Expression, **kwargs):
        format_function = kwargs.get("format_function", None)
        value = expression.expression
        if format_function:
            mapper_dict = kwargs.get("mapper_dict", None)
            value = format_function(value=value, mapper_dict=mapper_dict)
        return f"{kwargs.get('value_prefix', '')}{value}{kwargs.get('value_suffix', '')}"

    @staticmethod
    def __find_description(expression: Expression, **kwargs) -> str:
        last_day_description = None
        if kwargs.get("find_last_day", False):
            last_day_description = Translator.__get_last_day_description(expression, **kwargs)
        star_description = Translator.__get_star_and_question_mark_description(expression, **kwargs)
        slashed_description = Translator.__get_slashed_description(expression, **kwargs)
        list_description = Translator.__get_list_description(expression, **kwargs)
        range_description = Translator.__get_range_description(expression, **kwargs)
        descriptions_list = [last_day_description, star_description, slashed_description, list_description,
                             range_description]
        non_empty_descriptions = [description for description in descriptions_list if description]
        if len(non_empty_descriptions) != 1:
            value_description = Translator.__get_value_description(expression, **kwargs)
            if not value_description:
                return "COULD NOT TRANSLATE"
            return value_description
        return non_empty_descriptions[0]

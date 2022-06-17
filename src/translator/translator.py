from src.translator.enums import CronField, AllowedCharacters

MONTHS_MAPPER = {1: ("jan", "january"), 2: ("feb", "february"), 3: ("mar", "march"), 4: ("apr", "april"),
                 5: ("may", "may"), 6: ("jun", "june"), 7: ("jul", "july"), 8: ("aug", "august"),
                 9: ("sep", "september"), 10: ("oct", "october"), 11: ("nov", "november"), 12: ("dec", "december")}

DAY_OF_WEEK_MAPPER = {0: ("sun", "sunday"), 1: ("mon", "monday"), 2: ("tue", "tuesday"), 3: ("wed", "wednesday"),
                      4: ("thu", "thursday"), 5: ("fri", "friday"), 6: ("sat", "saturday")}


class Translator:

    @staticmethod
    def translate_seconds_and_minutes(subexpression: str, field_type: CronField) -> str:
        field_name = str(field_type.name).lower()
        past_time = f" past the {str(CronField(field_type.value + 1).name).lower()}"
        if Translator.__is_star_expression(subexpression):
            return f"every {field_name}"
        if Translator.__has_slash_in_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.SLASH.value)
            slash_expr = f"every {arguments[1]} {field_name}s"
            if Translator.__is_slashed_star_expression(subexpression):
                return slash_expr
            return f"{slash_expr}, starting at {field_name} {arguments[0]}{past_time}"
        if Translator.__is_list_expression(subexpression):
            list_values = subexpression.rsplit(AllowedCharacters.LIST.value)
            translation_msg = "at "
            for value in list_values:
                element_desc = value
                if Translator.__is_range_expression(element_desc):
                    arguments = element_desc.rsplit(AllowedCharacters.RANGE.value)
                    element_desc = f"{arguments[0]} through {arguments[1]}"
                if list_values[-1] == value:
                    translation_msg += f"and {element_desc} {field_name}s{past_time}"
                    break
                translation_msg += f"{element_desc}, "
            return translation_msg
        if Translator.__is_range_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.RANGE.value)
            return f"{field_name}s {arguments[0]} through {arguments[1]}{past_time}"
        return "ERROR"

    @staticmethod
    def translate_hours(subexpression: str, field_type: CronField) -> str:
        field_name = str(field_type.name).lower()
        if Translator.__is_star_expression(subexpression):
            return f"every {field_name}"
        if Translator.__has_slash_in_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.SLASH.value)
            slash_expr = f"every {arguments[1]} {field_name}s"
            if Translator.__is_slashed_star_expression(subexpression):
                return slash_expr
            return f"{slash_expr}, starting at {Translator.__get_am_pm_formatted_hour(arguments[0])}"
        if Translator.__is_list_expression(subexpression):
            list_values = subexpression.rsplit(AllowedCharacters.LIST.value)
            translation_msg = "at "
            for value in list_values:
                element_desc = value
                if Translator.__is_range_expression(element_desc):
                    arguments = element_desc.rsplit(AllowedCharacters.RANGE.value)
                    element_desc = f"{Translator.__get_am_pm_formatted_hour(arguments[0])} through " \
                                   f"{Translator.__get_am_pm_formatted_hour(arguments[1], True)}"
                else:
                    element_desc = Translator.__get_am_pm_formatted_hour(element_desc)
                if list_values[-1] == value:
                    translation_msg += f"and {element_desc}"
                    break
                translation_msg += f"{element_desc}, "
            return translation_msg
        if Translator.__is_range_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.RANGE.value)
            return f"between {Translator.__get_am_pm_formatted_hour(arguments[0])} and " \
                   f"{Translator.__get_am_pm_formatted_hour(arguments[1], True)}"
        return "ERROR"

    @staticmethod
    def translate_day_of_month(subexpression: str) -> str:
        if Translator.__is_last_week_day_expression(subexpression):
            return "on the last weekday of the month"
        if Translator.__is_week_day_expression(subexpression):
            day_of_month = [day for day in subexpression.split(AllowedCharacters.WEEK_DAY.value) if day]
            if day_of_month[0] == "1":
                return "on the first week day of the month"
            return f"on the weekday nearest day {day_of_month[0]} of the month"
        if Translator.__is_last_day_expression(subexpression):
            return "on the last day of the month"
        if Translator.__is_star_expression(subexpression) or Translator.__is_question_mark_expression(subexpression):
            return f"every day"
        if Translator.__has_slash_in_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.SLASH.value)
            slash_expr = f"every {arguments[1]} days"
            if Translator.__is_slashed_star_expression(subexpression):
                return slash_expr
            return f"{slash_expr}, starting on day {arguments[0]} of the month"
        if Translator.__is_list_expression(subexpression):
            list_values = subexpression.rsplit(AllowedCharacters.LIST.value)
            translation_msg = "on day "
            for value in list_values:
                element_desc = value
                if Translator.__is_range_expression(element_desc):
                    arguments = element_desc.rsplit(AllowedCharacters.RANGE.value)
                    element_desc = f"{arguments[0]} through {arguments[1]}"
                if list_values[-1] == value:
                    translation_msg += f"and {element_desc} of the month"
                    break
                translation_msg += f"{element_desc}, "
            return translation_msg
        if Translator.__is_range_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.RANGE.value)
            return f"between day {arguments[0]} and {arguments[1]} of the month"
        return "ERROR"

    @staticmethod
    def translate_month(subexpression: str, field_type: CronField) -> str:
        subexpression = subexpression.lower()
        field_name = str(field_type.name).lower()
        if Translator.__is_star_expression(subexpression):
            return f"every {field_name}"
        if Translator.__has_slash_in_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.SLASH.value)
            slash_expr = f"every {Translator.__get_full_description(arguments[1], MONTHS_MAPPER, True)} {field_name}s"
            if Translator.__is_slashed_star_expression(subexpression, False):
                return slash_expr
            return f"{slash_expr}, {Translator.__get_full_description(arguments[0], MONTHS_MAPPER)} through december"
        if Translator.__is_list_expression(subexpression):
            list_values = subexpression.rsplit(AllowedCharacters.LIST.value)
            translation_msg = "only in "
            for value in list_values:
                element_desc = value
                if Translator.__is_range_expression(element_desc):
                    arguments = element_desc.rsplit(AllowedCharacters.RANGE.value)
                    element_desc = f"{Translator.__get_full_description(arguments[0], MONTHS_MAPPER)} through " \
                                   f"{Translator.__get_full_description(arguments[1], MONTHS_MAPPER)}"
                else:
                    element_desc = Translator.__get_full_description(element_desc, MONTHS_MAPPER)
                if list_values[-1] == value:
                    translation_msg += f"and {element_desc}"
                    break
                translation_msg += f"{element_desc}, "
            return translation_msg
        if Translator.__is_range_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.RANGE.value)
            return f"{Translator.__get_full_description(arguments[0], MONTHS_MAPPER)} through " \
                   f"{Translator.__get_full_description(arguments[1], MONTHS_MAPPER)}"
        return "ERROR"

    @staticmethod
    def translate_day_of_week(subexpression: str) -> str:
        # TODO: Add question mark description
        if Translator.__is_last_day_expression(subexpression):
            day_of_week = [day for day in subexpression.split(AllowedCharacters.LAST_DAY.value) if day]
            if len(day_of_week) > 0:
                return f"on the last {Translator.__get_full_description(day_of_week[0], DAY_OF_WEEK_MAPPER)} of the " \
                       f"month"
            return "only on saturday"
        subexpression = subexpression.lower()
        if Translator.__is_star_expression(subexpression):
            return f"every day of the week"
        if Translator.__has_slash_in_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.SLASH.value)
            slash_expr = f"every {Translator.__get_full_description(arguments[1], DAY_OF_WEEK_MAPPER, True)} days of " \
                         f"the week"
            if Translator.__is_slashed_star_expression(subexpression):
                return slash_expr
            return f"{slash_expr}, {Translator.__get_full_description(arguments[0], DAY_OF_WEEK_MAPPER)} through " \
                   f"saturday"
        if Translator.__is_list_expression(subexpression):
            list_values = subexpression.rsplit(AllowedCharacters.LIST.value)
            translation_msg = "only on "
            for value in list_values:
                element_desc = value
                if Translator.__is_range_expression(element_desc):
                    arguments = element_desc.rsplit(AllowedCharacters.RANGE.value)
                    element_desc = f"{Translator.__get_full_description(arguments[0], DAY_OF_WEEK_MAPPER)} through " \
                                   f"{Translator.__get_full_description(arguments[1], DAY_OF_WEEK_MAPPER)}"
                else:
                    element_desc = Translator.__get_full_description(element_desc, DAY_OF_WEEK_MAPPER)
                if list_values[-1] == value:
                    translation_msg += f"and {element_desc}"
                    break
                translation_msg += f"{element_desc}, "
            return translation_msg
        if Translator.__is_range_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.RANGE.value)
            return f"{Translator.__get_full_description(arguments[0], DAY_OF_WEEK_MAPPER)} through " \
                   f"{Translator.__get_full_description(arguments[1], DAY_OF_WEEK_MAPPER)}"
        return "ERROR"

    @staticmethod
    def translate_year(subexpression: str, field_type: CronField) -> str:
        field_name = str(field_type.name).lower()
        if Translator.__is_star_expression(subexpression):
            return f"every {field_name}"
        if Translator.__has_slash_in_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.SLASH.value)
            slash_expr = f"every {arguments[1]} {field_name}s"
            if Translator.__is_slashed_star_expression(subexpression):
                return slash_expr
            return f"{slash_expr}, {arguments[0]} through 2099"
        if Translator.__is_list_expression(subexpression):
            list_values = subexpression.rsplit(AllowedCharacters.LIST.value)
            translation_msg = "only in "
            for value in list_values:
                element_desc = value
                if Translator.__is_range_expression(element_desc):
                    arguments = element_desc.rsplit(AllowedCharacters.RANGE.value)
                    element_desc = f"{arguments[0]} through {arguments[1]}"
                if list_values[-1] == value:
                    translation_msg += f"and {element_desc}"
                    break
                translation_msg += f"{element_desc}, "
            return translation_msg
        if Translator.__is_range_expression(subexpression):
            arguments = subexpression.rsplit(AllowedCharacters.RANGE.value)
            return f"{arguments[0]} through {arguments[1]}"
        return "ERROR"

    @staticmethod
    def __is_star_expression(subexpression: str) -> bool:
        return AllowedCharacters.STAR.value == subexpression

    @staticmethod
    def __is_question_mark_expression(subexpression: str) -> bool:
        return AllowedCharacters.QUESTION_MARK.value == subexpression

    @staticmethod
    def __is_last_day_expression(subexpression: str) -> bool:
        return subexpression.startswith(AllowedCharacters.LAST_DAY.value) or \
               subexpression.endswith(AllowedCharacters.LAST_DAY.value)

    @staticmethod
    def __is_slashed_star_expression(subexpression: str, zero_based: bool = True) -> bool:
        return_value = subexpression.startswith(f"{AllowedCharacters.STAR.value}{AllowedCharacters.SLASH.value}")
        if zero_based:
            return return_value or subexpression.startswith(f"0{AllowedCharacters.SLASH.value}")
        return return_value or subexpression.startswith(f"1{AllowedCharacters.SLASH.value}")

    @staticmethod
    def __has_slash_in_expression(subexpression: str) -> bool:
        return AllowedCharacters.SLASH.value in subexpression

    @staticmethod
    def __is_list_expression(subexpression: str) -> bool:
        return AllowedCharacters.LIST.value in subexpression

    @staticmethod
    def __is_week_day_expression(subexpression: str) -> bool:
        return subexpression.startswith(AllowedCharacters.WEEK_DAY.value) or \
               subexpression.endswith(AllowedCharacters.WEEK_DAY.value)

    @staticmethod
    def __is_last_week_day_expression(subexpression: str) -> bool:
        return Translator.__is_week_day_expression(subexpression) and \
               Translator.__is_last_day_expression(subexpression)

    @staticmethod
    def __is_range_expression(subexpression: str) -> bool:
        return AllowedCharacters.RANGE.value in subexpression

    @staticmethod
    def __get_hour_period(hours: str) -> str:
        if 0 <= int(hours) < 12:
            return "AM"
        return "PM"

    @staticmethod
    def __get_am_pm_formatted_hour(hour_24_format: str, is_last: bool = False) -> str:
        hour_int_value = int(hour_24_format)
        if hour_int_value == 0:
            hour_int_value = 12
        if hour_int_value > 12 and is_last:
            return f"{str(hour_int_value - 12)}:59 {Translator.__get_hour_period(hour_24_format)}"
        elif hour_int_value > 12 and not is_last:
            return f"{str(hour_int_value - 12)}:00 {Translator.__get_hour_period(hour_24_format)}"
        elif is_last and not hour_int_value > 12:
            return f"{hour_int_value}:59 {Translator.__get_hour_period(hour_24_format)}"
        return f"{hour_int_value}:00 {Translator.__get_hour_period(hour_24_format)}"

    @staticmethod
    def __get_full_description(value: str, mapper_dict: dict, numeric_value: bool = False) -> str:
        if value.isnumeric() and numeric_value:
            return value
        if value.isalpha():
            for key in mapper_dict:
                if value == mapper_dict[key][0]:
                    if numeric_value:
                        return str(key)
                    return mapper_dict[key][1]
        return mapper_dict.get(int(value))[1]



class Utils:
    def __init__(self):
        pass

    @staticmethod
    def get_name_in_string(string):
        """

        :param string:
        :return:
        """
        array = []
        end_name = string.find('?')
        for x in range(0, len(string)):
            if string[x] == '/' and x < end_name:
                array.append((end_name - x))
        if len(array) == 0:
            return 'NoImage.jpg'
        return string[(end_name - min(array) + 1):end_name]

    @staticmethod
    def get_numbers_in_string(text: str):
        number = [int(s) for s in text.split() if s.isdigit()]
        if len(number) == 0:
            number = [0]
        return number

    @staticmethod
    def holding_percent(length, percent):
        return int(length*(1 - percent))


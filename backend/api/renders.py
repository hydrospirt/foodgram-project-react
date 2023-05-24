import io

from rest_framework import renderers

INGREDIENT_DATA_FILE_HEADERS = ('Название', 'Кол-во', 'Ед. измерения')


class IngredientDataRendererTXT(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        text_buffer = io.StringIO()
        text_buffer.write(
            '''
_________________________________________________________________
|    _____                    _                                 |
|   |  ___|  ___    ___    __| |  __ _  _ __   __ _  _ __ ___   |
|   | |_    / _ \  / _ \  / _` | / _` || '__| / _` || '_ ` _  | |
|   |  _|  | (_) || (_) || (_| || (_| || |   | (_| || | | | | | |
|   |_|     \___/  \___/  \__,_| \__, ||_|    \__,_||_| |_| |_| |
|                                |___/                          |
|_______________________________________________________________|
'''
        )
        text_buffer.write(
            ' '.join(header for header in INGREDIENT_DATA_FILE_HEADERS) + '\n')

        for ingredient_data in data:
            text_buffer.write(
                ' '.join(str(i) for i in list(ingredient_data.values()))
                + '\n')
        text_buffer.write('_' * 65 + '\n')
        text_buffer.write(f'{"Большое спасибо за использование": ^65} \n'
                          + f'{"приложения Foodgram ©": ^65} \n')
        text_buffer.write('_' * 65 + '\n')
        return text_buffer.getvalue()

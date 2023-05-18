import io

from rest_framework import renderers

INGREDIENT_DATA_FILE_HEADERS = ('Название', 'Кол-во', 'Ед. измерения')


class IngredientDataRendererTXT(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        text_buffer = io.StringIO()
        text_buffer.write(
            ' '.join(header for header in INGREDIENT_DATA_FILE_HEADERS) + '\n')

        for ingredient_data in data:
            text_buffer.write(
                '    '.join(str(i) for i in list(ingredient_data.values()))
                + '\n')

        return text_buffer.getvalue()

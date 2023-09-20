import os
from functools import wraps
from typing import Callable

from docx.shared import Cm
from word.tools import HighchartsCreator
from .mixins import DiagramPickerInjector
from docxtpl import DocxTemplate, InlineImage
from .auxiliary_functions import determine_size_of_diagram


def render_diagram(color_flag: str = None, context_flag: bool = False) -> Callable:

    colors_palette = {
        'sentiments': ['#1BB394', '#EC5D5D', '#F2C94C'],
        'distribution': ['#1BB394', '#EC5D5D'],
        'smi_distribution': ['#1BB394', '#EC5D5D'],
    }

    def outter_wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner_wrapper(self, **kwargs) -> None:

            template: DocxTemplate = DocxTemplate(self._template_path)

            _position: str = self.proc_obj.settings.get('position')
            diagram_type: str = self.proc_obj.settings.get('type')
            data_labels: bool = self.proc_obj.settings.get('data_labels')

            highcharts_obj = HighchartsCreator(
                self.report_format,
                self.proc_obj.folder,
            )

            class_name = self.__class__.__name__

            path_to_image: str = os.path.join(
                os.getcwd(),
                'word',
                'highcharts_temp_images',
                f'{self.proc_obj.folder.unique_identifier}',
                class_name + '.png'
            )

            output_path: str = os.path.join(
                os.getcwd(),
                'word',
                'temp',
                f'{self.proc_obj.folder.unique_identifier}',
                f'output-{_position}-messages-{class_name}.docx'
            )

            chart_categories, chart_series, func_kwargs = func(self, diagram_type=diagram_type, **kwargs)

            query_string: str = DiagramPickerInjector(
                highcharts_obj,
                diagram_type,
                chart_color=colors_palette.get(color_flag),
                chart_categories=[chart.get('name') for chart in chart_categories],
                data_labels=data_labels,
                chart_series=chart_series,
            ).pick_and_execute()

            response: str = highcharts_obj.do_post_request_to_highcharts_server(query_string)

            highcharts_obj.save_data_as_png(response, path_to_image)

            sizes = determine_size_of_diagram(diagram_type)

            dynamics_image: InlineImage = InlineImage(template, image_descriptor=path_to_image, width=Cm(sizes[0]), height=Cm(sizes[1]))

            if context_flag:

                new_func_kwargs = {'context': func_kwargs, 'image': dynamics_image}

                template.render({
                    **new_func_kwargs
                }, autoescape=True)
            else:
                func_kwargs['image'] = dynamics_image
                template.render({
                    **func_kwargs
                }, autoescape=True)

            template.save(output_path)

        return inner_wrapper

    return outter_wrapper

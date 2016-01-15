import numpy as np

from menpo.image import Image
from menpofit.visualize import view_image_multiple_landmarks

from .error import euclidean_bb_normalised_error


class Result(object):
    r"""
    Class for storing a basic fitting result. It holds the final shape of a
    fitting process and, optionally, the initial shape, ground truth shape
    and the image.

    Parameters
    ----------
    final_shape : `menpo.shape.PointCloud`
        The final shape of the fitting process.
    image : `menpo.image.Image` or subclass or ``None``, optional
        The image on which the fitting process was applied. Note that a copy
        of the image will be assigned as an attribute. If ``None``, then no
        image is assigned.
    initial_shape : `menpo.shape.PointCloud` or ``None``, optional
        The initial shape from which the fitting process started. If ``None``,
        then no initial shape is assigned.
    gt_shape : `menpo.shape.PointCloud` or ``None``, optional
        The ground truth shape associated with the image. If ``None``, then no
        ground truth shape is assigned.
    """
    def __init__(self, final_shape, image=None, initial_shape=None,
                 gt_shape=None):
        self.final_shape = final_shape
        self.initial_shape = initial_shape
        self.gt_shape = gt_shape
        self.image = None
        if image is not None:
            self.image = Image(image.pixels)

    def final_error(self, compute_error=None):
        r"""
        Returns the final error of the fitting process, if the ground truth
        shape exists.

        Parameters
        -----------
        compute_error: `callable`, optional
            Callable that computes the error between the fitted and
            ground truth shapes.

        Returns
        -------
        final_error : `float`
            The final error at the end of the fitting process.

        Raises
        ------
        ValueError
            Ground truth shape has not been set, so the final error cannot be
            computed
        """
        if compute_error is None:
            compute_error = euclidean_bb_normalised_error
        if self.gt_shape is not None:
            return compute_error(self.final_shape, self.gt_shape)
        else:
            raise ValueError('Ground truth shape has not been set, so the '
                             'final error cannot be computed')

    def initial_error(self, compute_error=None):
        r"""
        Returns the initial error of the fitting process, if the ground truth
        shape exists.

        Parameters
        -----------
        compute_error: `callable`, optional
            Callable that computes the error between the initial and
            ground truth shapes.

        Returns
        -------
        initial_error : `float`
            The initial error at the beginning of the fitting process.

        Raises
        ------
        ValueError
            Initial shape has not been set, so the initial error cannot be
            computed
        ValueError
            Ground truth shape has not been set, so the initial error cannot be
            computed
        """
        if compute_error is None:
            compute_error = euclidean_bb_normalised_error
        if self.initial_shape is None:
            raise ValueError('Initial shape has not been set, so the initial '
                             'error cannot be computed')
        elif self.gt_shape is None:
            raise ValueError('Ground truth shape has not been set, so the '
                             'initial error cannot be computed')
        else:
            return compute_error(self.initial_shape, self.gt_shape)

    def view(self, figure_id=None, new_figure=False, render_image=True,
             render_final_shape=True, render_initial_shape=False,
             render_gt_shape=False, subplots_enabled=True, channels=None,
             interpolation='bilinear', cmap_name=None, alpha=1., masked=True,
             render_markers=True, final_markers_colour='r',
             initial_markers_colour='b', gt_markers_colour='y',
             marker_style='o', marker_size=20, marker_edge_colour='k',
             marker_edge_width=1., render_numbering=False,
             numbers_horizontal_align='center',
             numbers_vertical_align='bottom',
             numbers_font_name='sans-serif', numbers_font_size=10,
             numbers_font_style='normal', numbers_font_weight='normal',
             numbers_font_colour='k', render_legend=True,
             legend_title='', legend_font_name='sans-serif',
             legend_font_style='normal', legend_font_size=10,
             legend_font_weight='normal', legend_marker_scale=None,
             legend_location=2, legend_bbox_to_anchor=(1.05, 1.),
             legend_border_axes_pad=None, legend_n_columns=1,
             legend_horizontal_spacing=None, legend_vertical_spacing=None,
             legend_border=True, legend_border_padding=None,
             legend_shadow=False, legend_rounded_corners=False,
             render_axes=False, axes_font_name='sans-serif', axes_font_size=10,
             axes_font_style='normal', axes_font_weight='normal',
             axes_x_limits=None, axes_y_limits=None, axes_x_ticks=None,
             axes_y_ticks=None, figure_size=(10, 8)):
        """
        Visualize the fitting result. The method renders the final fitted
        shape and optionally the initial shape, ground truth shape and the
        image, id they were provided.

        Parameters
        ----------
        figure_id : `object`, optional
            The id of the figure to be used.
        new_figure : `bool`, optional
            If ``True``, a new figure is created.
        render_image : `bool`, optional
            If ``True`` and the image exists, then it gets rendered.
        render_final_shape : `bool`, optional
            If ``True``, then the final fitting shape gets rendered.
        render_initial_shape : `bool`, optional
            If ``True`` and the initial fitting shape exists, then it gets
            rendered.
        render_gt_shape : `bool`, optional
            If ``True`` and the ground truth shape exists, then it gets
            rendered.
        subplots_enabled : `bool`, optional
            If ``True``, then the requested final, initial and ground truth
            shapes get rendered on separate subplots.
        channels : `int` or `list` of `int` or ``all`` or ``None``
            If `int` or `list` of `int`, the specified channel(s) will be
            rendered. If ``all``, all the channels will be rendered in subplots.
            If ``None`` and the image is RGB, it will be rendered in RGB mode.
            If ``None`` and the image is not RGB, it is equivalent to ``all``.
        interpolation : See Below, optional
            The interpolation used to render the image. For example, if
            ``bilinear``, the image will be smooth and if ``nearest``, the
            image will be pixelated. Example options ::

                {none, nearest, bilinear, bicubic, spline16, spline36, hanning,
                hamming, hermite, kaiser, quadric, catrom, gaussian, bessel,
                mitchell, sinc, lanczos}

        cmap_name: `str`, optional,
            If ``None``, single channel and three channel images default
            to greyscale and rgb colormaps respectively.
        alpha : `float`, optional
            The alpha blending value, between 0 (transparent) and 1 (opaque).
        masked : `bool`, optional
            If ``True``, then the image is rendered as masked.
        render_markers : `bool`, optional
            If ``True``, the markers will be rendered.
        final_markers_colour : See Below, optional
            The face (filling) colour of the markers of the final fitting shape.
            Example options ::

                {r, g, b, c, m, k, w}
                or
                (3, ) ndarray

        initial_markers_colour : See Below, optional
            The face (filling) colour of the markers of the initial shape.
            Example options ::

                {r, g, b, c, m, k, w}
                or
                (3, ) ndarray

        gt_markers_colour : See Below, optional
            The face (filling) colour of the markers of the ground truth shape.
            Example options ::

                {r, g, b, c, m, k, w}
                or
                (3, ) ndarray

        marker_style : See Below, optional
            The style of the markers. Example options ::

                {., ,, o, v, ^, <, >, +, x, D, d, s, p, *, h, H, 1, 2, 3, 4, 8}

        marker_size : `int`, optional
            The size of the markers in points^2.
        marker_edge_colour : See Below, optional
            The edge colour of the markers.
            Example options ::

                {r, g, b, c, m, k, w}
                or
                (3, ) ndarray

        marker_edge_width : `float`, optional
            The width of the markers' edge.
        render_numbering : `bool`, optional
            If ``True``, the landmarks will be numbered.
        numbers_horizontal_align : ``{center, right, left}``, optional
            The horizontal alignment of the numbers' texts.
        numbers_vertical_align : ``{center, top, bottom, baseline}``, optional
            The vertical alignment of the numbers' texts.
        numbers_font_name : See Below, optional
            The font of the numbers. Example options ::

                {serif, sans-serif, cursive, fantasy, monospace}

        numbers_font_size : `int`, optional
            The font size of the numbers.
        numbers_font_style : ``{normal, italic, oblique}``, optional
            The font style of the numbers.
        numbers_font_weight : See Below, optional
            The font weight of the numbers.
            Example options ::

                {ultralight, light, normal, regular, book, medium, roman,
                 semibold, demibold, demi, bold, heavy, extra bold, black}

        numbers_font_colour : See Below, optional
            The font colour of the numbers.
            Example options ::

                {r, g, b, c, m, k, w}
                or
                (3, ) ndarray

        render_legend : `bool`, optional
            If ``True``, the legend will be rendered.
        legend_title : `str`, optional
            The title of the legend.
        legend_font_name : See below, optional
            The font of the legend. Example options ::

                {serif, sans-serif, cursive, fantasy, monospace}

        legend_font_style : ``{normal, italic, oblique}``, optional
            The font style of the legend.
        legend_font_size : `int`, optional
            The font size of the legend.
        legend_font_weight : See Below, optional
            The font weight of the legend.
            Example options ::

                {ultralight, light, normal, regular, book, medium, roman,
                 semibold, demibold, demi, bold, heavy, extra bold, black}

        legend_marker_scale : `float`, optional
            The relative size of the legend markers with respect to the original
        legend_location : `int`, optional
            The location of the legend. The predefined values are:

            =============== ==
            'best'          0
            'upper right'   1
            'upper left'    2
            'lower left'    3
            'lower right'   4
            'right'         5
            'center left'   6
            'center right'  7
            'lower center'  8
            'upper center'  9
            'center'        10
            =============== ==

        legend_bbox_to_anchor : (`float`, `float`) `tuple`, optional
            The bbox that the legend will be anchored.
        legend_border_axes_pad : `float`, optional
            The pad between the axes and legend border.
        legend_n_columns : `int`, optional
            The number of the legend's columns.
        legend_horizontal_spacing : `float`, optional
            The spacing between the columns.
        legend_vertical_spacing : `float`, optional
            The vertical space between the legend entries.
        legend_border : `bool`, optional
            If ``True``, a frame will be drawn around the legend.
        legend_border_padding : `float`, optional
            The fractional whitespace inside the legend border.
        legend_shadow : `bool`, optional
            If ``True``, a shadow will be drawn behind legend.
        legend_rounded_corners : `bool`, optional
            If ``True``, the frame's corners will be rounded (fancybox).
        render_axes : `bool`, optional
            If ``True``, the axes will be rendered.
        axes_font_name : See Below, optional
            The font of the axes. Example options ::

                {serif, sans-serif, cursive, fantasy, monospace}

        axes_font_size : `int`, optional
            The font size of the axes.
        axes_font_style : ``{normal, italic, oblique}``, optional
            The font style of the axes.
        axes_font_weight : See Below, optional
            The font weight of the axes.
            Example options ::

                {ultralight, light, normal, regular, book, medium, roman,
                 semibold,demibold, demi, bold, heavy, extra bold, black}

        axes_x_limits : `float` or (`float`, `float`) or ``None``, optional
            The limits of the x axis. If `float`, then it sets padding on the
            right and left of the Image as a percentage of the Image's width. If
            `tuple` or `list`, then it defines the axis limits. If ``None``, then
            the limits are set automatically.
        axes_y_limits : (`float`, `float`) `tuple` or ``None``, optional
            The limits of the y axis. If `float`, then it sets padding on the
            top and bottom of the Image as a percentage of the Image's height. If
            `tuple` or `list`, then it defines the axis limits. If ``None``, then
            the limits are set automatically.
        axes_x_ticks : `list` or `tuple` or ``None``, optional
            The ticks of the x axis.
        axes_y_ticks : `list` or `tuple` or ``None``, optional
            The ticks of the y axis.
        figure_size : (`float`, `float`) `tuple` or ``None`` optional
            The size of the figure in inches.
        """
        # Create image instance
        if self.image is None:
            image = Image(np.zeros((10, 10)))
            render_image = False
        else:
            image = Image(self.image.pixels)
        # Assign pointclouds to image
        groups = []
        colours = []
        subplots_titles = {}
        if render_final_shape:
            image.landmarks['final'] = self.final_shape
            groups.append('final')
            colours.append(final_markers_colour)
            subplots_titles['final'] = 'Final'
        if self.initial_shape is not None and render_initial_shape:
            image.landmarks['initial'] = self.initial_shape
            groups.append('initial')
            colours.append(initial_markers_colour)
            subplots_titles['initial'] = 'Initial'
        if self.gt_shape is not None and render_gt_shape:
            image.landmarks['groundtruth'] = self.gt_shape
            groups.append('groundtruth')
            colours.append(gt_markers_colour)
            subplots_titles['groundtruth'] = 'Groundtruth'
        # Render
        view_image_multiple_landmarks(
                image, groups, with_labels=None, figure_id=figure_id,
                new_figure=new_figure, subplots_enabled=subplots_enabled,
                subplots_titles=subplots_titles, render_image=render_image,
                render_landmarks=True, masked=masked,
                channels=channels, interpolation=interpolation,
                cmap_name=cmap_name, alpha=alpha, image_view=True,
                render_lines=False, line_style='-', line_width=2,
                line_colour='k', render_markers=render_markers,
                marker_style=marker_style, marker_size=marker_size,
                marker_edge_width=marker_edge_width,
                marker_edge_colour=marker_edge_colour,
                marker_face_colour=colours,
                render_numbering=render_numbering,
                numbers_horizontal_align=numbers_horizontal_align,
                numbers_vertical_align=numbers_vertical_align,
                numbers_font_name=numbers_font_name,
                numbers_font_size=numbers_font_size,
                numbers_font_style=numbers_font_style,
                numbers_font_weight=numbers_font_weight,
                numbers_font_colour=numbers_font_colour,
                render_legend=render_legend, legend_title=legend_title,
                legend_font_name=legend_font_name,
                legend_font_style=legend_font_style,
                legend_font_size=legend_font_size,
                legend_font_weight=legend_font_weight,
                legend_marker_scale=legend_marker_scale,
                legend_location=legend_location,
                legend_bbox_to_anchor=legend_bbox_to_anchor,
                legend_border_axes_pad=legend_border_axes_pad,
                legend_n_columns=legend_n_columns,
                legend_horizontal_spacing=legend_horizontal_spacing,
                legend_vertical_spacing=legend_vertical_spacing,
                legend_border=legend_border,
                legend_border_padding=legend_border_padding,
                legend_shadow=legend_shadow,
                legend_rounded_corners=legend_rounded_corners,
                render_axes=render_axes, axes_font_name=axes_font_name,
                axes_font_size=axes_font_size, axes_font_style=axes_font_style,
                axes_font_weight=axes_font_weight, axes_x_limits=axes_x_limits,
                axes_y_limits=axes_y_limits, axes_x_ticks=axes_x_ticks,
                axes_y_ticks=axes_y_ticks, figure_size=figure_size)

    def view_widget(self, figure_size=(10, 8), style='coloured'):
        r"""
        Visualizes the result object using an interactive widget.

        Parameters
        ----------
        figure_size : (`int`, `int`), optional
            The initial size of the rendered figure.
        style : {``'coloured'``, ``'minimal'``}, optional
            If ``'coloured'``, then the style of the widget will be coloured. If
            ``minimal``, then the style is simple using black and white colours.
        """
        if self.image is not None:
            from menpowidgets import visualize_images
            image = Image(self.image.pixels)
            image.landmarks['final'] = self.final_shape
            if self.initial_shape is not None:
                image.landmarks['initial'] = self.initial_shape
            if self.gt_shape is not None:
                image.landmarks['groundtruth'] = self.gt_shape
            visualize_images(image, figure_size=figure_size, style=style)
        else:
            from menpowidgets import visualize_pointclouds
            pointclouds = [self.final_shape]
            if self.initial_shape is not None:
                pointclouds.append(self.initial_shape)
            if self.gt_shape is not None:
                pointclouds.append(self.gt_shape)
            visualize_pointclouds(pointclouds, figure_size=figure_size,
                                  style=style, browser_style='slider')

    def __str__(self):
        out = "Fitting result of {} landmark points.".format(
                self.final_shape.n_points)
        if self.gt_shape is not None:
            if self.initial_shape is not None:
                out += "\nInitial error: {:.4f}".format(self.initial_error())
            out += "\nFinal error: {:.4f}".format(self.final_error())
        return out


# class IterativeResult(Result):
#     def __init__(self, final_shape, image=None, initial_shape=None,
#                  gt_shape=None):
#         self.final_shape = final_shape
#         self.initial_shape = initial_shape
#         self.gt_shape = gt_shape
#         self.image = None
#         if image is not None:
#             self.image = Image(image.pixels)
#
#     @abc.abstractproperty
#     def n_iters(self):
#         r"""
#         Returns the number of iterations.
#         """
#
#     @abc.abstractproperty
#     def shapes(self):
#         r"""
#         Generates a list containing the shapes obtained at each fitting
#         iteration.
#
#         Returns
#         -------
#         shapes : :map:`PointCloud`s or ndarray list
#             A list containing the shapes obtained at each fitting iteration.
#         """
#
#     @property
#     def iter_image(self):
#         r"""
#         Returns a copy of the fitted image with a as many landmark groups as
#         iteration run by fitting procedure:
#             - ``iter_0``, containing the initial shape.
#             - ``iter_1``, containing the the fitted shape at the first
#             iteration.
#             - ``...``
#             - ``iter_n``, containing the final fitted shape.
#
#         :type: :map:`Image`
#         """
#         image = Image(self.image.pixels)
#         for j, s in enumerate(self.shapes):
#             image.landmarks['iter_'+str(j)] = s
#         return image
#
#     def errors(self, compute_error=None):
#         r"""
#         Returns a list containing the error at each fitting iteration.
#
#         Parameters
#         -----------
#         compute_error: `callable`, optional
#             Callable that computes the error between the fitted and
#             ground truth shapes.
#
#         Returns
#         -------
#         errors : `list` of `float`
#             The errors at each iteration of the fitting process.
#         """
#         if compute_error is None:
#             compute_error = euclidean_bb_normalised_error
#         if self.gt_shape is not None:
#             return [compute_error(t, self.gt_shape)
#                     for t in self.shapes]
#         else:
#             raise ValueError('Ground truth has not been set, errors cannot '
#                              'be computed')
#
#     def plot_errors(self, error_type=None, figure_id=None,
#                     new_figure=False, render_lines=True, line_colour='b',
#                     line_style='-', line_width=2, render_markers=True,
#                     marker_style='o', marker_size=4, marker_face_colour='b',
#                     marker_edge_colour='k', marker_edge_width=1.,
#                     render_axes=True, axes_font_name='sans-serif',
#                     axes_font_size=10, axes_font_style='normal',
#                     axes_font_weight='normal', figure_size=(10, 6),
#                     render_grid=True, grid_line_style='--',
#                     grid_line_width=0.5):
#         r"""
#         Plot of the error evolution at each fitting iteration.
#         Parameters
#         ----------
#         error_type : {``me_norm``, ``me``, ``rmse``}, optional
#             Specifies the way in which the error between the fitted and
#             ground truth shapes is to be computed.
#         figure_id : `object`, optional
#             The id of the figure to be used.
#         new_figure : `bool`, optional
#             If ``True``, a new figure is created.
#         render_lines : `bool`, optional
#             If ``True``, the line will be rendered.
#         line_colour : {``r``, ``g``, ``b``, ``c``, ``m``, ``k``, ``w``} or
#                       ``(3, )`` `ndarray`, optional
#             The colour of the lines.
#         line_style : {``-``, ``--``, ``-.``, ``:``}, optional
#             The style of the lines.
#         line_width : `float`, optional
#             The width of the lines.
#         render_markers : `bool`, optional
#             If ``True``, the markers will be rendered.
#         marker_style : {``.``, ``,``, ``o``, ``v``, ``^``, ``<``, ``>``, ``+``,
#                         ``x``, ``D``, ``d``, ``s``, ``p``, ``*``, ``h``, ``H``,
#                         ``1``, ``2``, ``3``, ``4``, ``8``}, optional
#             The style of the markers.
#         marker_size : `int`, optional
#             The size of the markers in points^2.
#         marker_face_colour : {``r``, ``g``, ``b``, ``c``, ``m``, ``k``, ``w``}
#                              or ``(3, )`` `ndarray`, optional
#             The face (filling) colour of the markers.
#         marker_edge_colour : {``r``, ``g``, ``b``, ``c``, ``m``, ``k``, ``w``}
#                              or ``(3, )`` `ndarray`, optional
#             The edge colour of the markers.
#         marker_edge_width : `float`, optional
#             The width of the markers' edge.
#         render_axes : `bool`, optional
#             If ``True``, the axes will be rendered.
#         axes_font_name : {``serif``, ``sans-serif``, ``cursive``, ``fantasy``,
#                           ``monospace``}, optional
#             The font of the axes.
#         axes_font_size : `int`, optional
#             The font size of the axes.
#         axes_font_style : {``normal``, ``italic``, ``oblique``}, optional
#             The font style of the axes.
#         axes_font_weight : {``ultralight``, ``light``, ``normal``, ``regular``,
#                             ``book``, ``medium``, ``roman``, ``semibold``,
#                             ``demibold``, ``demi``, ``bold``, ``heavy``,
#                             ``extra bold``, ``black``}, optional
#             The font weight of the axes.
#         figure_size : (`float`, `float`) or `None`, optional
#             The size of the figure in inches.
#         render_grid : `bool`, optional
#             If ``True``, the grid will be rendered.
#         grid_line_style : {``-``, ``--``, ``-.``, ``:``}, optional
#             The style of the grid lines.
#         grid_line_width : `float`, optional
#             The width of the grid lines.
#         Returns
#         -------
#         viewer : :map:`GraphPlotter`
#             The viewer object.
#         """
#         from menpo.visualize import GraphPlotter
#         errors_list = self.errors(compute_error=error_type)
#         return GraphPlotter(figure_id=figure_id, new_figure=new_figure,
#                             x_axis=range(len(errors_list)),
#                             y_axis=[errors_list],
#                             title='Fitting Errors per Iteration',
#                             x_label='Iteration', y_label='Fitting Error',
#                             x_axis_limits=(0, len(errors_list)-1),
#                             y_axis_limits=None).render(
#                 render_lines=render_lines, line_colour=line_colour,
#                 line_style=line_style, line_width=line_width,
#                 render_markers=render_markers, marker_style=marker_style,
#                 marker_size=marker_size, marker_face_colour=marker_face_colour,
#                 marker_edge_colour=marker_edge_colour,
#                 marker_edge_width=marker_edge_width, render_legend=False,
#                 render_axes=render_axes, axes_font_name=axes_font_name,
#                 axes_font_size=axes_font_size, axes_font_style=axes_font_style,
#                 axes_font_weight=axes_font_weight, render_grid=render_grid,
#                 grid_line_style=grid_line_style, grid_line_width=grid_line_width,
#                 figure_size=figure_size)
#
#     def displacements(self):
#         r"""
#         A list containing the displacement between the shape of each iteration
#         and the shape of the previous one.
#         :type: `list` of ndarray
#         """
#         return [np.linalg.norm(s1.points - s2.points, axis=1)
#                 for s1, s2 in zip(self.shapes, self.shapes[1:])]
#
#     def displacements_stats(self, stat_type='mean'):
#         r"""
#         A list containing the a statistical metric on the displacement between
#         the shape of each iteration and the shape of the previous one.
#         Parameters
#         -----------
#         stat_type : `str` ``{'mean', 'median', 'min', 'max'}``, optional
#             Specifies a statistic metric to be extracted from the displacements.
#         Returns
#         -------
#         :type: `list` of `float`
#             The statistical metric on the points displacements for each
#             iteration.
#         """
#         if stat_type == 'mean':
#             return [np.mean(d) for d in self.displacements()]
#         elif stat_type == 'median':
#             return [np.median(d) for d in self.displacements()]
#         elif stat_type == 'max':
#             return [np.max(d) for d in self.displacements()]
#         elif stat_type == 'min':
#             return [np.min(d) for d in self.displacements()]
#         else:
#             raise ValueError("type must be 'mean', 'median', 'min' or 'max'")
#
#     def plot_displacements(self, stat_type='mean', figure_id=None,
#                            new_figure=False, render_lines=True, line_colour='b',
#                            line_style='-', line_width=2, render_markers=True,
#                            marker_style='o', marker_size=4,
#                            marker_face_colour='b', marker_edge_colour='k',
#                            marker_edge_width=1., render_axes=True,
#                            axes_font_name='sans-serif', axes_font_size=10,
#                            axes_font_style='normal', axes_font_weight='normal',
#                            figure_size=(10, 6), render_grid=True,
#                            grid_line_style='--', grid_line_width=0.5):
#         r"""
#         Plot of a statistical metric of the displacement between the shape of
#         each iteration and the shape of the previous one.
#         Parameters
#         ----------
#         stat_type : {``mean``, ``median``, ``min``, ``max``}, optional
#             Specifies a statistic metric to be extracted from the displacements
#             (see also `displacements_stats()` method).
#         figure_id : `object`, optional
#             The id of the figure to be used.
#         new_figure : `bool`, optional
#             If ``True``, a new figure is created.
#         render_lines : `bool`, optional
#             If ``True``, the line will be rendered.
#         line_colour : {``r``, ``g``, ``b``, ``c``, ``m``, ``k``, ``w``} or
#                       ``(3, )`` `ndarray`, optional
#             The colour of the lines.
#         line_style : {``-``, ``--``, ``-.``, ``:``}, optional
#             The style of the lines.
#         line_width : `float`, optional
#             The width of the lines.
#         render_markers : `bool`, optional
#             If ``True``, the markers will be rendered.
#         marker_style : {``.``, ``,``, ``o``, ``v``, ``^``, ``<``, ``>``, ``+``,
#                         ``x``, ``D``, ``d``, ``s``, ``p``, ``*``, ``h``, ``H``,
#                         ``1``, ``2``, ``3``, ``4``, ``8``}, optional
#             The style of the markers.
#         marker_size : `int`, optional
#             The size of the markers in points^2.
#         marker_face_colour : {``r``, ``g``, ``b``, ``c``, ``m``, ``k``, ``w``}
#                              or ``(3, )`` `ndarray`, optional
#             The face (filling) colour of the markers.
#         marker_edge_colour : {``r``, ``g``, ``b``, ``c``, ``m``, ``k``, ``w``}
#                              or ``(3, )`` `ndarray`, optional
#             The edge colour of the markers.
#         marker_edge_width : `float`, optional
#             The width of the markers' edge.
#         render_axes : `bool`, optional
#             If ``True``, the axes will be rendered.
#         axes_font_name : {``serif``, ``sans-serif``, ``cursive``, ``fantasy``,
#                           ``monospace``}, optional
#             The font of the axes.
#         axes_font_size : `int`, optional
#             The font size of the axes.
#         axes_font_style : {``normal``, ``italic``, ``oblique``}, optional
#             The font style of the axes.
#         axes_font_weight : {``ultralight``, ``light``, ``normal``, ``regular``,
#                             ``book``, ``medium``, ``roman``, ``semibold``,
#                             ``demibold``, ``demi``, ``bold``, ``heavy``,
#                             ``extra bold``, ``black``}, optional
#             The font weight of the axes.
#         figure_size : (`float`, `float`) or `None`, optional
#             The size of the figure in inches.
#         render_grid : `bool`, optional
#             If ``True``, the grid will be rendered.
#         grid_line_style : {``-``, ``--``, ``-.``, ``:``}, optional
#             The style of the grid lines.
#         grid_line_width : `float`, optional
#             The width of the grid lines.
#         Returns
#         -------
#         viewer : :map:`GraphPlotter`
#             The viewer object.
#         """
#         from menpo.visualize import GraphPlotter
#         # set labels
#         if stat_type == 'max':
#             ylabel = 'Maximum Displacement'
#             title = 'Maximum displacement per Iteration'
#         elif stat_type == 'min':
#             ylabel = 'Minimum Displacement'
#             title = 'Minimum displacement per Iteration'
#         elif stat_type == 'mean':
#             ylabel = 'Mean Displacement'
#             title = 'Mean displacement per Iteration'
#         elif stat_type == 'median':
#             ylabel = 'Median Displacement'
#             title = 'Median displacement per Iteration'
#         else:
#             raise ValueError('stat_type must be one of {max, min, mean, '
#                              'median}.')
#         # plot
#         displacements_list = self.displacements_stats(stat_type=stat_type)
#         return GraphPlotter(figure_id=figure_id, new_figure=new_figure,
#                             x_axis=range(len(displacements_list)),
#                             y_axis=[displacements_list],
#                             title=title,
#                             x_label='Iteration', y_label=ylabel,
#                             x_axis_limits=(0, len(displacements_list)-1),
#                             y_axis_limits=None).render(
#                 render_lines=render_lines, line_colour=line_colour,
#                 line_style=line_style, line_width=line_width,
#                 render_markers=render_markers, marker_style=marker_style,
#                 marker_size=marker_size, marker_face_colour=marker_face_colour,
#                 marker_edge_colour=marker_edge_colour,
#                 marker_edge_width=marker_edge_width, render_legend=False,
#                 render_axes=render_axes, axes_font_name=axes_font_name,
#                 axes_font_size=axes_font_size, axes_font_style=axes_font_style,
#                 axes_font_weight=axes_font_weight, render_grid=render_grid,
#                 grid_line_style=grid_line_style, grid_line_width=grid_line_width,
#                 figure_size=figure_size)
#
#     def as_serializableresult(self):
#         return SerializableIterativeResult(
#                 self.image, self.shapes, self.n_iters, gt_shape=self.gt_shape)

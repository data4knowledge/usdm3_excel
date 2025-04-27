from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_sheet.study_sheet import StudySheet
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4_excel.excel_table_writer.excel_table_writer import ExcelTableWriter


class TestStudySheet:
    """Tests for the StudySheet class."""

    def test_init(self):
        """Test initialization of StudySheet."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a mock ExcelTableWriter
        mock_etw = MagicMock(spec=ExcelTableWriter)

        # Create a StudySheet instance
        sheet = StudySheet(ct_version, mock_etw)

        # Verify that the CTVersion and ExcelTableWriter instances are stored correctly
        assert sheet.ct_version is ct_version
        assert sheet.ct_version.versions["test"] == "1.0.0"
        assert sheet.etw is mock_etw

    def test_save(self):
        """Test the save method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a mock ExcelTableWriter
        mock_etw = MagicMock(spec=ExcelTableWriter)
        mock_etw.add_table.return_value = (
            10  # Simulate adding a table and returning the last row
        )

        # Create a StudySheet instance
        sheet = StudySheet(ct_version, mock_etw)

        # Create a mock Study
        mock_study = MagicMock()

        # Mock the MainPanel and DatesPanel classes
        with (
            patch(
                "usdm3_excel.export.study_sheet.study_sheet.MainPanel"
            ) as mock_main_panel_class,
            patch(
                "usdm3_excel.export.study_sheet.study_sheet.DatesPanel"
            ) as mock_dates_panel_class,
        ):
            # Configure the mock MainPanel
            mock_main_panel = MagicMock()
            mock_main_panel.execute.return_value = [
                ["header1", "header2"],
                [1, 2],
                [3, 4],
            ]
            mock_main_panel_class.return_value = mock_main_panel

            # Configure the mock DatesPanel
            mock_dates_panel = MagicMock()
            mock_dates_panel.execute.return_value = [
                ["header3", "header4"],
                [5, 6],
                [7, 8],
            ]
            mock_dates_panel_class.return_value = mock_dates_panel

            # Call the save method
            sheet.save(mock_study)

            # Verify that the MainPanel was created with the correct CTVersion
            mock_main_panel_class.assert_called_once_with(ct_version)

            # Verify that the MainPanel's execute method was called with the mock Study
            mock_main_panel.execute.assert_called_once_with(mock_study)

            # Verify that the ExcelTableWriter's add_table method was called with the result from the MainPanel
            mock_etw.add_table.assert_any_call(
                [["header1", "header2"], [1, 2], [3, 4]], "study"
            )

            # Verify that the DatesPanel was created with the correct CTVersion
            mock_dates_panel_class.assert_called_once_with(ct_version)

            # Verify that the DatesPanel's execute method was called with the mock Study
            mock_dates_panel.execute.assert_called_once_with(mock_study)

            # Verify that the ExcelTableWriter's add_table method was called with the result from the DatesPanel
            mock_etw.add_table.assert_any_call(
                [["header3", "header4"], [5, 6], [7, 8]], "study", 12
            )

            # Verify that the ExcelTableWriter's format_cells method was called for the first formatting
            mock_etw.format_cells.assert_any_call(
                "study",
                (1, 1, 10, 1),
                font_style="bold",
                background_color=sheet.HEADING_BG,
            )

            # Verify that the ExcelTableWriter's format_cells method was called for the second formatting
            mock_etw.format_cells.assert_any_call(
                "study",
                (1, 2, 10, 2),
                wrap_text=True,
            )

            # Verify that the ExcelTableWriter's format_cells method was called for the third formatting
            mock_etw.format_cells.assert_any_call(
                "study",
                (12, 1, 12, 7),
                font_style="bold",
                background_color=sheet.HEADING_BG,
            )

            # Verify that the ExcelTableWriter's set_column_width method was called for the first set of columns
            mock_etw.set_column_width.assert_any_call("study", [1, 3, 4, 5, 6, 7], 20.0)

            # Verify that the ExcelTableWriter's set_column_width method was called for the second column
            mock_etw.set_column_width.assert_any_call("study", 2, 40.0)

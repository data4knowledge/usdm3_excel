from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_timing_sheet.study_timing_sheet import StudyTimingSheet
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4_excel.excel_table_writer.excel_table_writer import ExcelTableWriter


class TestStudyTimingSheet:
    """Tests for the StudyTimingSheet class."""

    def test_init(self):
        """Test initialization of StudyTimingSheet."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a mock ExcelTableWriter
        mock_etw = MagicMock(spec=ExcelTableWriter)

        # Create a StudyTimingSheet instance
        sheet = StudyTimingSheet(ct_version, mock_etw)

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
        mock_etw.add_table.return_value = 10  # Simulate adding a table and returning the last row

        # Create a StudyTimingSheet instance
        sheet = StudyTimingSheet(ct_version, mock_etw)

        # Create a mock Study
        mock_study = MagicMock()

        # Mock the TimingPanel class
        with patch(
            "usdm3_excel.export.study_timing_sheet.study_timing_sheet.TimingPanel"
        ) as mock_timing_panel_class:
            # Configure the mock TimingPanel
            mock_timing_panel = MagicMock()
            mock_timing_panel.execute.return_value = [
                ["name", "description", "label", "type", "from", "to", "timingValue", "toFrom", "window"],
                ["Timing1", "Description1", "Label1", "Type1", "From1", "To1", "Value1", "ToFrom1", "Window1"],
                ["Timing2", "Description2", "Label2", "Type2", "From2", "To2", "Value2", "ToFrom2", "Window2"],
            ]
            mock_timing_panel_class.return_value = mock_timing_panel

            # Call the save method
            sheet.save(mock_study)

            # Verify that the TimingPanel was created with the correct CTVersion
            mock_timing_panel_class.assert_called_once_with(ct_version)

            # Verify that the TimingPanel's execute method was called with the mock Study
            mock_timing_panel.execute.assert_called_once_with(mock_study)

            # Verify that the ExcelTableWriter's add_table method was called with the result from the TimingPanel
            mock_etw.add_table.assert_called_once_with(
                [
                    ["name", "description", "label", "type", "from", "to", "timingValue", "toFrom", "window"],
                    ["Timing1", "Description1", "Label1", "Type1", "From1", "To1", "Value1", "ToFrom1", "Window1"],
                    ["Timing2", "Description2", "Label2", "Type2", "From2", "To2", "Value2", "ToFrom2", "Window2"],
                ],
                "studyDesignTiming",
            )

            # Verify that the ExcelTableWriter's format_cells method was called
            mock_etw.format_cells.assert_called_once_with(
                "studyDesignTiming",
                (1, 1, 1, 9),
                font_style="bold",
                background_color=sheet.HEADING_BG,
            )

            # Verify that the ExcelTableWriter's set_column_width method was called for the first set of columns
            mock_etw.set_column_width.assert_any_call(
                "studyDesignTiming", [1, 2, 3], 30.0
            )

            # Verify that the ExcelTableWriter's set_column_width method was called for the second set of columns
            mock_etw.set_column_width.assert_any_call(
                "studyDesignTiming", [4, 5, 6, 7, 8, 9], 15.0
            )

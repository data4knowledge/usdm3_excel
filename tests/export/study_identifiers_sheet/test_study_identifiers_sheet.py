from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_identifiers_sheet.study_identifiers_sheet import StudyIdentifiersSheet
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4_excel.excel_table_writer.excel_table_writer import ExcelTableWriter


class TestStudyIdentifiersSheet:
    """Tests for the StudyIdentifiersSheet class."""

    def test_init(self):
        """Test initialization of StudyIdentifiersSheet."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a mock ExcelTableWriter
        mock_etw = MagicMock(spec=ExcelTableWriter)

        # Create a StudyIdentifiersSheet instance
        sheet = StudyIdentifiersSheet(ct_version, mock_etw)

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

        # Create a StudyIdentifiersSheet instance
        sheet = StudyIdentifiersSheet(ct_version, mock_etw)

        # Create a mock Study
        mock_study = MagicMock()

        # Mock the IdentifiersPanel class
        with patch(
            "usdm3_excel.export.study_identifiers_sheet.study_identifiers_sheet.IdentifiersPanel"
        ) as mock_identifiers_panel_class:
            # Configure the mock IdentifiersPanel
            mock_identifiers_panel = MagicMock()
            mock_identifiers_panel.execute.return_value = [
                ["header1", "header2", "header3", "header4", "header5", "header6"],
                [1, 2, 3, 4, 5, 6],
                [7, 8, 9, 10, 11, 12],
            ]
            mock_identifiers_panel_class.return_value = mock_identifiers_panel

            # Call the save method
            sheet.save(mock_study)

            # Verify that the IdentifiersPanel was created with the correct CTVersion
            mock_identifiers_panel_class.assert_called_once_with(ct_version)

            # Verify that the IdentifiersPanel's execute method was called with the mock Study
            mock_identifiers_panel.execute.assert_called_once_with(mock_study)

            # Verify that the ExcelTableWriter's add_table method was called with the result from the IdentifiersPanel
            mock_etw.add_table.assert_called_once_with(
                [
                    ["header1", "header2", "header3", "header4", "header5", "header6"],
                    [1, 2, 3, 4, 5, 6],
                    [7, 8, 9, 10, 11, 12],
                ],
                "studyIdentifiers",
            )

            # Verify that the ExcelTableWriter's format_cells method was called
            mock_etw.format_cells.assert_called_once_with(
                "studyIdentifiers",
                (1, 1, 1, 6),
                font_style="bold",
                background_color=sheet.HEADING_BG,
            )

            # Verify that the ExcelTableWriter's set_column_width method was called
            mock_etw.set_column_width.assert_called_once_with(
                "studyIdentifiers", [1, 6], 20.0
            )

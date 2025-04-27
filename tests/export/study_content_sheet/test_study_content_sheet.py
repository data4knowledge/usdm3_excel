from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_content_sheet.study_content_sheet import StudyContentSheet
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4_excel.excel_table_writer.excel_table_writer import ExcelTableWriter


class TestStudyContentSheet:
    """Tests for the StudyContentSheet class."""

    def test_init(self):
        """Test initialization of StudyContentSheet."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a mock ExcelTableWriter
        mock_etw = MagicMock(spec=ExcelTableWriter)

        # Create a StudyContentSheet instance
        sheet = StudyContentSheet(ct_version, mock_etw)

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

        # Create a StudyContentSheet instance
        sheet = StudyContentSheet(ct_version, mock_etw)

        # Create a mock Study
        mock_study = MagicMock()

        # Mock the ContentPanel class
        with patch(
            "usdm3_excel.export.study_content_sheet.study_content_sheet.ContentPanel"
        ) as mock_content_panel_class:
            # Configure the mock ContentPanel
            mock_content_panel = MagicMock()
            mock_content_panel.execute.return_value = [
                ["name", "sectionNumber", "sectionTitle", "text"],
                ["Content1", "1.0", "Introduction", "This is the introduction text."],
                ["Content2", "2.0", "Methods", "This is the methods text."],
            ]
            mock_content_panel_class.return_value = mock_content_panel

            # Call the save method
            sheet.save(mock_study)

            # Verify that the ContentPanel was created with the correct CTVersion
            mock_content_panel_class.assert_called_once_with(ct_version)

            # Verify that the ContentPanel's execute method was called with the mock Study
            mock_content_panel.execute.assert_called_once_with(mock_study)

            # Verify that the ExcelTableWriter's add_table method was called with the result from the ContentPanel
            mock_etw.add_table.assert_called_once_with(
                [
                    ["name", "sectionNumber", "sectionTitle", "text"],
                    ["Content1", "1.0", "Introduction", "This is the introduction text."],
                    ["Content2", "2.0", "Methods", "This is the methods text."],
                ],
                "studyDesignContent",
            )

            # Verify that the ExcelTableWriter's format_cells method was called for text wrapping
            mock_etw.format_cells.assert_any_call(
                "studyDesignContent",
                (2, 1, 10, 2),
                wrap_text=True,
                vertical_alignment="top",
            )

            # Verify that the ExcelTableWriter's format_cells method was called for header formatting
            mock_etw.format_cells.assert_any_call(
                "studyDesignContent",
                (1, 1, 1, 4),
                font_style="bold",
                background_color=sheet.HEADING_BG,
            )

            # Verify that the ExcelTableWriter's set_column_width method was called for the first set of columns
            mock_etw.set_column_width.assert_any_call(
                "studyDesignContent", [1, 2], 20.0
            )

            # Verify that the ExcelTableWriter's set_column_width method was called for the second set of columns
            mock_etw.set_column_width.assert_any_call(
                "studyDesignContent", [3, 4], 100.0
            )

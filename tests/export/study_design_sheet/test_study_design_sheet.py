from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_design_sheet.study_design_sheet import StudyDesignSheet
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4_excel.excel_table_writer.excel_table_writer import ExcelTableWriter


class TestStudyDesignSheet:
    """Tests for the StudyDesignSheet class."""

    def test_init(self):
        """Test initialization of StudyDesignSheet."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a mock ExcelTableWriter
        mock_etw = MagicMock(spec=ExcelTableWriter)

        # Create a StudyDesignSheet instance
        sheet = StudyDesignSheet(ct_version, mock_etw)

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
        mock_etw.add_table.side_effect = [
            10,
            20,
        ]  # Return values for the two add_table calls

        # Create a StudyDesignSheet instance
        sheet = StudyDesignSheet(ct_version, mock_etw)

        # Create a mock Study
        mock_study = MagicMock()

        # Mock the MainPanel and HighLevelDesignPanel classes
        with (
            patch(
                "usdm3_excel.export.study_design_sheet.study_design_sheet.MainPanel"
            ) as mock_main_panel_class,
            patch(
                "usdm3_excel.export.study_design_sheet.study_design_sheet.HighLevelDesignPanel"
            ) as mock_high_level_design_panel_class,
        ):
            # Configure the mock MainPanel
            mock_main_panel = MagicMock()
            mock_main_panel.execute.return_value = [
                ["header1", "header2"],
                [1, 2],
                [3, 4],
            ]
            mock_main_panel_class.return_value = mock_main_panel

            # Configure the mock HighLevelDesignPanel
            mock_high_level_design_panel = MagicMock()
            mock_high_level_design_panel.execute.return_value = [
                ["Epoch/Arms", "Epoch1", "Epoch2"],
                ["Arm1", "", ""],
                ["Arm2", "", ""],
            ]
            mock_high_level_design_panel_class.return_value = (
                mock_high_level_design_panel
            )

            # Call the save method
            sheet.save(mock_study)

            # Verify that the MainPanel was created with the correct CTVersion
            mock_main_panel_class.assert_called_once_with(ct_version)

            # Verify that the MainPanel's execute method was called with the mock Study
            mock_main_panel.execute.assert_called_once_with(mock_study)

            # Verify that the ExcelTableWriter's add_table method was called with the result from the MainPanel
            mock_etw.add_table.assert_any_call(
                [["header1", "header2"], [1, 2], [3, 4]], "studyDesign"
            )

            # Verify that the HighLevelDesignPanel was created with the correct CTVersion
            mock_high_level_design_panel_class.assert_called_once_with(ct_version)

            # Verify that the HighLevelDesignPanel's execute method was called with the mock Study
            mock_high_level_design_panel.execute.assert_called_once_with(mock_study)

            # Verify that the ExcelTableWriter's add_table method was called with the result from the HighLevelDesignPanel
            mock_etw.add_table.assert_any_call(
                [
                    ["Epoch/Arms", "Epoch1", "Epoch2"],
                    ["Arm1", "", ""],
                    ["Arm2", "", ""],
                ],
                "studyDesign",
                12,  # 10 (last_row) + 2
            )

            # Verify that the ExcelTableWriter's format_cells method was called
            mock_etw.format_cells.assert_called_once_with(
                "study",
                (1, 1, 20, 1),
                font_style="bold",
                background_color=sheet.HEADING_BG,
            )

            # Verify that the ExcelTableWriter's set_column_width method was called
            mock_etw.set_column_width.assert_called_once_with(
                "studyDesign", [1, 3, 4, 5, 6, 7], 20.0
            )

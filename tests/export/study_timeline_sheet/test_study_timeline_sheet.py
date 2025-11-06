from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_timeline_sheet.study_timeline_sheet import (
    StudyTimelineSheet,
)
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4_excel.export.excel_table_writer.excel_table_writer import ExcelTableWriter


class TestStudyTimelineSheet:
    """Tests for the StudyTimelineSheet class."""

    def test_init(self):
        """Test initialization of StudyTimelineSheet."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a mock ExcelTableWriter
        mock_etw = MagicMock(spec=ExcelTableWriter)

        # Create a StudyTimelineSheet instance
        sheet = StudyTimelineSheet(ct_version, mock_etw)

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
            5,
            8,
            15,
        ]  # Return values for the three add_table calls

        # Create a StudyTimelineSheet instance
        sheet = StudyTimelineSheet(ct_version, mock_etw)

        # Create a mock Study
        mock_study = MagicMock()

        # Mock the MainPanel, HeadingsPanel, and ActivitiesPanel classes
        with (
            patch(
                "usdm3_excel.export.study_timeline_sheet.study_timeline_sheet.MainPanel"
            ) as mock_main_panel_class,
            patch(
                "usdm3_excel.export.study_timeline_sheet.study_timeline_sheet.HeadingsPanel"
            ) as mock_headings_panel_class,
            patch(
                "usdm3_excel.export.study_timeline_sheet.study_timeline_sheet.ActivitiesPanel"
            ) as mock_activities_panel_class,
        ):
            # Configure the mock MainPanel
            mock_main_panel = MagicMock()
            mock_main_panel.execute.return_value = [
                ["Name", "Main Timeline"],
                ["Description", "Main timeline description"],
                ["Condition", "Entry condition"],
            ]
            mock_main_panel_class.return_value = mock_main_panel

            # Configure the mock HeadingsPanel
            mock_headings_panel = MagicMock()
            mock_headings_panel.execute.return_value = [
                ["name", "Timepoint1", "Timepoint2"],
                ["description", "Description1", "Description2"],
                ["label", "Label1", "Label2"],
            ]
            mock_headings_panel_class.return_value = mock_headings_panel

            # Configure the mock ActivitiesPanel
            mock_activities_panel = MagicMock()
            mock_activities_panel.execute.return_value = [
                ["Parent Activity", "Child Activity", "BC/Procedure/Timeline", "", ""],
                ["", "Activity1", "", "X", ""],
                ["", "Activity2", "", "", "X"],
            ]
            mock_activities_panel_class.return_value = mock_activities_panel

            # Call the save method
            sheet.save(mock_study)

            # Verify that the MainPanel was created with the correct CTVersion
            mock_main_panel_class.assert_called_once_with(ct_version)

            # Verify that the MainPanel's execute method was called with the mock Study
            mock_main_panel.execute.assert_called_once_with(mock_study)

            # Verify that the ExcelTableWriter's add_table method was called with the result from the MainPanel
            mock_etw.add_table.assert_any_call(
                [
                    ["Name", "Main Timeline"],
                    ["Description", "Main timeline description"],
                    ["Condition", "Entry condition"],
                ],
                "mainTimeline",
                1,
                1,
            )

            # Verify that the HeadingsPanel was created with the correct CTVersion
            mock_headings_panel_class.assert_called_once_with(ct_version)

            # Verify that the HeadingsPanel's execute method was called with the mock Study
            mock_headings_panel.execute.assert_called_once_with(mock_study)

            # Verify that the ExcelTableWriter's add_table method was called with the result from the HeadingsPanel
            mock_etw.add_table.assert_any_call(
                [
                    ["name", "Timepoint1", "Timepoint2"],
                    ["description", "Description1", "Description2"],
                    ["label", "Label1", "Label2"],
                ],
                "mainTimeline",
                1,
                3,
            )

            # Verify that the ActivitiesPanel was created with the correct CTVersion
            mock_activities_panel_class.assert_called_once_with(ct_version)

            # Verify that the ActivitiesPanel's execute method was called with the mock Study
            mock_activities_panel.execute.assert_called_once_with(mock_study)

            # Verify that the ExcelTableWriter's add_table method was called with the result from the ActivitiesPanel
            mock_etw.add_table.assert_any_call(
                [
                    [
                        "Parent Activity",
                        "Child Activity",
                        "BC/Procedure/Timeline",
                        "",
                        "",
                    ],
                    ["", "Activity1", "", "X", ""],
                    ["", "Activity2", "", "", "X"],
                ],
                "mainTimeline",
                9,
                1,
            )

            # Verify that the ExcelTableWriter's format_cells method was called
            mock_etw.format_cells.assert_called_once_with(
                "mainTimeline",
                (1, 1, 15, 1),
                font_style="bold",
                background_color=sheet.HEADING_BG,
            )

            # Verify that the ExcelTableWriter's set_column_width method was called
            mock_etw.set_column_width.assert_called_once_with(
                "mainTimeline", [1, 3, 4, 5, 6, 7], 20.0
            )

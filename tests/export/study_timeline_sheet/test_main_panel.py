from unittest.mock import MagicMock

from usdm3_excel.export.study_timeline_sheet.main_panel import MainPanel
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4.api.schedule_timeline import ScheduleTimeline


class TestMainPanel:
    """Tests for the MainPanel class."""

    def test_init(self):
        """Test initialization of MainPanel."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a MainPanel instance
        panel = MainPanel(ct_version)

        # Verify that the CTVersion instance is stored correctly
        assert panel.ct_version is ct_version
        assert panel.ct_version.versions["test"] == "1.0.0"

    def test_execute_with_timeline(self):
        """Test the execute method with a timeline."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a MainPanel instance
        panel = MainPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()
        mock_timeline = MagicMock(spec=ScheduleTimeline)

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]
        mock_design.main_timeline.return_value = mock_timeline
        mock_timeline.name = "Main Timeline"
        mock_timeline.description = "Main timeline description"
        mock_timeline.entryCondition = "Entry condition"

        # Call the execute method
        result = panel.execute(mock_study)

        # Verify the result
        expected_result = [
            ["Name", "Main Timeline"],
            ["Description", "Main timeline description"],
            ["Condition", "Entry condition"],
        ]
        assert result == expected_result

    def test_execute_without_timeline(self):
        """Test the execute method without a timeline."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a MainPanel instance
        panel = MainPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]
        mock_design.main_timeline.return_value = None

        # Call the execute method
        result = panel.execute(mock_study)

        # Verify the result
        expected_result = [
            ["Name", ""],
            ["Description", ""],
            ["Condition", ""],
        ]
        assert result == expected_result

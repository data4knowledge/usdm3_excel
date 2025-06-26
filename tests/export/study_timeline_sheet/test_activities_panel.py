from unittest.mock import MagicMock

from usdm3_excel.export.study_timeline_sheet.activities_panel import ActivitiesPanel
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4.api.schedule_timeline import ScheduleTimeline


class TestActivitiesPanel:
    """Tests for the ActivitiesPanel class."""

    def test_init(self):
        """Test initialization of ActivitiesPanel."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create an ActivitiesPanel instance
        panel = ActivitiesPanel(ct_version)

        # Verify that the CTVersion instance is stored correctly
        assert panel.ct_version is ct_version
        assert panel.ct_version.versions["test"] == "1.0.0"

    def test_execute_with_timeline_and_activities(self):
        """Test the execute method with a timeline and activities."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create an ActivitiesPanel instance
        panel = ActivitiesPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()
        mock_timeline = MagicMock(spec=ScheduleTimeline)
        mock_activity1 = MagicMock()
        mock_activity2 = MagicMock()
        mock_timepoint1 = MagicMock()
        mock_timepoint2 = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]
        mock_design.main_timeline.return_value = mock_timeline
        mock_design.activity_list.return_value = [mock_activity1, mock_activity2]
        mock_timeline.timepoint_list.return_value = [mock_timepoint1, mock_timepoint2]

        # Configure the mock activities
        mock_activity1.id = "activity1_id"
        mock_activity1.name = "Activity1"
        mock_activity1.label = "Activity1 Label"

        mock_activity2.id = "activity2_id"
        mock_activity2.name = "Activity2"
        mock_activity2.label = None

        # Configure the mock timepoints
        mock_timepoint1.id = "timepoint1_id"
        mock_timepoint1.activityIds = ["activity1_id"]

        mock_timepoint2.id = "timepoint2_id"
        mock_timepoint2.activityIds = ["activity2_id"]

        # Call the execute method
        result = panel.execute(mock_study)

        # Verify the result
        expected_result = [
            ["Parent Activity", "Child Activity", "BC/Procedure/Timeline", "", ""],
            ["", "Activity1 Label", "", "X", ""],
            ["", "Activity2", "", "", "X"],
        ]
        assert result == expected_result

    def test_execute_with_timeline_no_activities(self):
        """Test the execute method with a timeline but no activities."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create an ActivitiesPanel instance
        panel = ActivitiesPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()
        mock_timeline = MagicMock(spec=ScheduleTimeline)
        mock_timepoint1 = MagicMock()
        mock_timepoint2 = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]
        mock_design.main_timeline.return_value = mock_timeline
        mock_design.activity_list.return_value = []
        mock_timeline.timepoint_list.return_value = [mock_timepoint1, mock_timepoint2]

        # Configure the mock timepoints
        mock_timepoint1.id = "timepoint1_id"
        mock_timepoint2.id = "timepoint2_id"

        # Call the execute method
        result = panel.execute(mock_study)

        # Verify the result
        expected_result = [
            ["Parent Activity", "Child Activity", "BC/Procedure/Timeline", "", ""],
        ]
        assert result == expected_result

    def test_execute_without_timeline(self):
        """Test the execute method without a timeline."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create an ActivitiesPanel instance
        panel = ActivitiesPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()
        mock_activity1 = MagicMock()
        mock_activity2 = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]
        mock_design.main_timeline.return_value = None
        mock_design.activity_list.return_value = [mock_activity1, mock_activity2]

        # Call the execute method
        result = panel.execute(mock_study)

        # Verify the result
        expected_result = [
            ["Parent Activity", "Child Activity", "BC/Procedure/Timeline"],
        ]
        assert result == expected_result

    def test_execute_with_shared_activities(self):
        """Test the execute method with activities shared across timepoints."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create an ActivitiesPanel instance
        panel = ActivitiesPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()
        mock_timeline = MagicMock(spec=ScheduleTimeline)
        mock_activity1 = MagicMock()
        mock_timepoint1 = MagicMock()
        mock_timepoint2 = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]
        mock_design.main_timeline.return_value = mock_timeline
        mock_design.activity_list.return_value = [mock_activity1]
        mock_timeline.timepoint_list.return_value = [mock_timepoint1, mock_timepoint2]

        # Configure the mock activity
        mock_activity1.id = "activity1_id"
        mock_activity1.name = "Activity1"
        mock_activity1.label = "Activity1 Label"

        # Configure the mock timepoints - both reference the same activity
        mock_timepoint1.id = "timepoint1_id"
        mock_timepoint1.activityIds = ["activity1_id"]

        mock_timepoint2.id = "timepoint2_id"
        mock_timepoint2.activityIds = ["activity1_id"]

        # Call the execute method
        result = panel.execute(mock_study)

        # Verify the result
        expected_result = [
            ["Parent Activity", "Child Activity", "BC/Procedure/Timeline", "", ""],
            ["", "Activity1 Label", "", "X", "X"],
        ]
        assert result == expected_result

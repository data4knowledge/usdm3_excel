from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_timing_sheet.timing_panel import TimingPanel
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4.api.timing import Timing
from usdm4.api.schedule_timeline import ScheduleTimeline


class TestTimingPanel:
    """Tests for the TimingPanel class."""

    def test_init(self):
        """Test initialization of TimingPanel."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a TimingPanel instance
        panel = TimingPanel(ct_version)

        # Verify that the CTVersion instance is stored correctly
        assert panel.ct_version is ct_version
        assert panel.ct_version.versions["test"] == "1.0.0"

    def test_execute(self):
        """Test the execute method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a TimingPanel instance
        panel = TimingPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()
        mock_timeline = MagicMock(spec=ScheduleTimeline)
        mock_timing = MagicMock(spec=Timing)

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]
        mock_design.scheduleTimelines = [mock_timeline]
        mock_timeline.timings = [mock_timing]

        # Mock the _add_timing method
        with patch.object(panel, "_add_timing") as mock_add_timing:
            # Call the execute method
            panel.execute(mock_study)

            # Verify that _add_timing was called with the correct arguments
            mock_add_timing.assert_called_once_with([], mock_timing, mock_timeline)

    def test_add_timing(self):
        """Test the _add_timing method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a TimingPanel instance
        panel = TimingPanel(ct_version)

        # Create mock objects
        collection = []
        mock_timing = MagicMock(spec=Timing)
        mock_timeline = MagicMock(spec=ScheduleTimeline)
        mock_from_timepoint = MagicMock()
        mock_to_timepoint = MagicMock()
        mock_type = MagicMock()
        mock_relative_to_from = MagicMock()

        # Configure the mock objects
        # Set the attributes directly on the mock_timing
        mock_timing.type = mock_type
        mock_timing.relativeFromScheduledInstanceId = "from_id"
        mock_timing.relativeToScheduledInstanceId = "to_id"
        mock_timing.valueLabel = "Value1"
        mock_timing.windowLabel = "Window1"
        mock_timing.relativeToFrom = mock_relative_to_from
        
        mock_timing.model_dump.return_value = {
            "name": "Timing1",
            "description": "Description1",
            "label": "Label1",
            "type": mock_type,
            "relativeFromScheduledInstanceId": "from_id",
            "relativeToScheduledInstanceId": "to_id",
            "valueLabel": "Value1",
            "windowLabel": "Window1",
            "relativeToFrom": mock_relative_to_from,
        }
        mock_timeline.find_timepoint.side_effect = lambda id: {
            "from_id": mock_from_timepoint,
            "to_id": mock_to_timepoint,
        }.get(id)
        mock_from_timepoint.name = "From1"
        mock_to_timepoint.name = "To1"

        # Mock the helper methods
        with (
            patch.object(panel, "_pt_from_code") as mock_pt_from_code,
        ):
            # Configure the _pt_from_code mock to return different values for different inputs
            mock_pt_from_code.side_effect = lambda x: {
                mock_type: "Type1",
                mock_relative_to_from: "ToFrom1",
            }[x]

            # Call the _add_timing method
            panel._add_timing(collection, mock_timing, mock_timeline)

            # Verify that the helper methods were called with the correct arguments
            mock_pt_from_code.assert_any_call(mock_type)
            mock_pt_from_code.assert_any_call(mock_relative_to_from)

            # Verify that the timeline's find_timepoint method was called with the correct arguments
            mock_timeline.find_timepoint.assert_any_call("from_id")
            mock_timeline.find_timepoint.assert_any_call("to_id")

            # Verify that the collection was updated correctly
            assert len(collection) == 1
            assert collection[0]["name"] == "Timing1"
            assert collection[0]["description"] == "Description1"
            assert collection[0]["label"] == "Label1"
            assert collection[0]["type"] == "Type1"
            assert collection[0]["from"] == "From1"
            assert collection[0]["to"] == "To1"
            assert collection[0]["timingValue"] == "Value1"
            assert collection[0]["window"] == "Window1"
            assert collection[0]["toFrom"] == "ToFrom1"

    def test_add_timing_no_timepoints(self):
        """Test the _add_timing method when no timepoints are found."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a TimingPanel instance
        panel = TimingPanel(ct_version)

        # Create mock objects
        collection = []
        mock_timing = MagicMock(spec=Timing)
        mock_timeline = MagicMock(spec=ScheduleTimeline)
        mock_type = MagicMock()
        mock_relative_to_from = MagicMock()

        # Configure the mock objects
        # Set the attributes directly on the mock_timing
        mock_timing.type = mock_type
        mock_timing.relativeFromScheduledInstanceId = "from_id"
        mock_timing.relativeToScheduledInstanceId = "to_id"
        mock_timing.valueLabel = "Value1"
        mock_timing.windowLabel = "Window1"
        mock_timing.relativeToFrom = mock_relative_to_from
        
        mock_timing.model_dump.return_value = {
            "name": "Timing1",
            "description": "Description1",
            "label": "Label1",
            "type": mock_type,
            "relativeFromScheduledInstanceId": "from_id",
            "relativeToScheduledInstanceId": "to_id",
            "valueLabel": "Value1",
            "windowLabel": "Window1",
            "relativeToFrom": mock_relative_to_from,
        }
        mock_timeline.find_timepoint.return_value = None

        # Mock the helper methods
        with (
            patch.object(panel, "_pt_from_code") as mock_pt_from_code,
        ):
            # Configure the _pt_from_code mock to return different values for different inputs
            mock_pt_from_code.side_effect = lambda x: {
                mock_type: "Type1",
                mock_relative_to_from: "ToFrom1",
            }[x]

            # Call the _add_timing method
            panel._add_timing(collection, mock_timing, mock_timeline)

            # Verify that the helper methods were called with the correct arguments
            mock_pt_from_code.assert_any_call(mock_type)
            mock_pt_from_code.assert_any_call(mock_relative_to_from)

            # Verify that the timeline's find_timepoint method was called with the correct arguments
            mock_timeline.find_timepoint.assert_any_call("from_id")
            mock_timeline.find_timepoint.assert_any_call("to_id")

            # Verify that the collection was updated correctly
            assert len(collection) == 1
            assert collection[0]["name"] == "Timing1"
            assert collection[0]["description"] == "Description1"
            assert collection[0]["label"] == "Label1"
            assert collection[0]["type"] == "Type1"
            assert collection[0]["from"] == ""
            assert collection[0]["to"] == ""
            assert collection[0]["timingValue"] == "Value1"
            assert collection[0]["window"] == "Window1"
            assert collection[0]["toFrom"] == "ToFrom1"

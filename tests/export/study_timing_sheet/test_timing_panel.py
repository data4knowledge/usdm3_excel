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
        mock_timing.value = "P1D"
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
            patch.object(panel, "_encode_type") as mock_encode_type,
            patch.object(panel, "_encode_to_from") as mock_encode_to_from,
        ):
            # Configure the mock methods to return expected values
            mock_encode_type.return_value = "Type1"
            mock_encode_to_from.return_value = "ToFrom1"

            # Call the _add_timing method
            panel._add_timing(collection, mock_timing, mock_timeline)

            # Verify that the helper methods were called with the correct arguments
            mock_encode_type.assert_called_once_with(mock_type)
            mock_encode_to_from.assert_called_once_with(mock_relative_to_from)

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
            assert (
                collection[0]["timingValue"] == "1 Days"
            )  # ISO 8601 duration P1D is converted to "1 Days"
            assert collection[0]["window"] == "Window1"
            assert collection[0]["toFrom"] == "ToFrom1"

    def test_decode_iso8601_duration_years(self):
        """Test _decode_iso8601_duration with years."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        assert panel._decode_iso8601_duration("P1Y") == "1 Years"
        assert panel._decode_iso8601_duration("P5Y") == "5 Years"
        assert panel._decode_iso8601_duration("P10Y") == "10 Years"

    def test_decode_iso8601_duration_months(self):
        """Test _decode_iso8601_duration with months."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        assert panel._decode_iso8601_duration("P1M") == "1 Months"
        assert panel._decode_iso8601_duration("P6M") == "6 Months"
        assert panel._decode_iso8601_duration("P12M") == "12 Months"

    def test_decode_iso8601_duration_weeks(self):
        """Test _decode_iso8601_duration with weeks."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        assert panel._decode_iso8601_duration("P1W") == "1 Weeks"
        assert panel._decode_iso8601_duration("P4W") == "4 Weeks"
        assert panel._decode_iso8601_duration("P52W") == "52 Weeks"

    def test_decode_iso8601_duration_days(self):
        """Test _decode_iso8601_duration with days."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        assert panel._decode_iso8601_duration("P1D") == "1 Days"
        assert panel._decode_iso8601_duration("P7D") == "7 Days"
        assert panel._decode_iso8601_duration("P30D") == "30 Days"
        assert panel._decode_iso8601_duration("P365D") == "365 Days"

    def test_decode_iso8601_duration_hours(self):
        """Test _decode_iso8601_duration with hours (PT prefix)."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        assert panel._decode_iso8601_duration("PT1H") == "1 Hours"
        assert panel._decode_iso8601_duration("PT12H") == "12 Hours"
        assert panel._decode_iso8601_duration("PT24H") == "24 Hours"

    def test_decode_iso8601_duration_minutes(self):
        """Test _decode_iso8601_duration with minutes (PT prefix)."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        assert panel._decode_iso8601_duration("PT1M") == "1 Minutes"
        assert panel._decode_iso8601_duration("PT30M") == "30 Minutes"
        assert panel._decode_iso8601_duration("PT60M") == "60 Minutes"

    def test_decode_iso8601_duration_seconds(self):
        """Test _decode_iso8601_duration with seconds (PT prefix)."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        assert panel._decode_iso8601_duration("PT1S") == "1 Seconds"
        assert panel._decode_iso8601_duration("PT30S") == "30 Seconds"
        assert panel._decode_iso8601_duration("PT3600S") == "3600 Seconds"

    def test_decode_iso8601_duration_lowercase(self):
        """Test _decode_iso8601_duration with lowercase prefixes."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        # PT prefix should work with lowercase (method uses .upper())
        assert panel._decode_iso8601_duration("pt1H") == "1 Hours"
        assert panel._decode_iso8601_duration("Pt5M") == "5 Minutes"

    def test_decode_iso8601_duration_invalid_format(self):
        """Test _decode_iso8601_duration with invalid formats."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        # Invalid unit character returns with None as units_str
        assert panel._decode_iso8601_duration("P1X") == "1 Day"
        assert panel._decode_iso8601_duration("PT1Q") == "1 Day"
        
    def test_decode_iso8601_duration_no_number(self):
        """Test _decode_iso8601_duration with no numeric value returns default."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        # No number should return default
        assert panel._decode_iso8601_duration("PD") == "1 Day"
        assert panel._decode_iso8601_duration("PTH") == "1 Day"

    def test_decode_iso8601_duration_empty_string(self):
        """Test _decode_iso8601_duration with empty string raises IndexError."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        # Empty string causes IndexError due to value[-1] access
        try:
            result = panel._decode_iso8601_duration("")
            assert False, f"Expected IndexError but got result: {result}"
        except IndexError:
            pass  # Expected behavior

    def test_decode_iso8601_duration_large_numbers(self):
        """Test _decode_iso8601_duration with large numeric values."""
        ct_version = CTVersion()
        panel = TimingPanel(ct_version)
        
        assert panel._decode_iso8601_duration("P100Y") == "100 Years"
        assert panel._decode_iso8601_duration("P999D") == "999 Days"
        assert panel._decode_iso8601_duration("PT1000H") == "1000 Hours"

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
        mock_timing.value = "P1D"
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
            patch.object(panel, "_encode_type") as mock_encode_type,
            patch.object(panel, "_encode_to_from") as mock_encode_to_from,
        ):
            # Configure the mock methods to return expected values
            mock_encode_type.return_value = "Type1"
            mock_encode_to_from.return_value = "ToFrom1"

            # Call the _add_timing method
            panel._add_timing(collection, mock_timing, mock_timeline)

            # Verify that the helper methods were called with the correct arguments
            mock_encode_type.assert_called_once_with(mock_type)
            mock_encode_to_from.assert_called_once_with(mock_relative_to_from)

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
            assert (
                collection[0]["timingValue"] == "1 Days"
            )  # ISO 8601 duration P1D is converted to "1 Days"
            assert collection[0]["window"] == "Window1"
            assert collection[0]["toFrom"] == "ToFrom1"

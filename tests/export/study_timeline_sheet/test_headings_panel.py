from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_timeline_sheet.headings_panel import HeadingsPanel
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4.api.schedule_timeline import ScheduleTimeline
from usdm4.api.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance


class TestHeadingsPanel:
    """Tests for the HeadingsPanel class."""

    def test_init(self):
        """Test initialization of HeadingsPanel."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a HeadingsPanel instance
        panel = HeadingsPanel(ct_version)

        # Verify that the CTVersion instance is stored correctly
        assert panel.ct_version is ct_version
        assert panel.ct_version.versions["test"] == "1.0.0"

    def test_execute_with_timeline(self):
        """Test the execute method with a timeline."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a HeadingsPanel instance
        panel = HeadingsPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()
        mock_timeline = MagicMock(spec=ScheduleTimeline)
        mock_timepoint1 = MagicMock(spec=ScheduledActivityInstance)
        mock_timepoint2 = MagicMock(spec=ScheduledDecisionInstance)

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]
        mock_design.main_timeline.return_value = mock_timeline
        mock_timeline.timepoint_list.return_value = [mock_timepoint1, mock_timepoint2]

        # Mock the _add_instance method
        with patch.object(panel, "_add_instance") as mock_add_instance:
            # Call the execute method
            result = panel.execute(mock_study)

            # Verify that the _add_instance method was called with the correct arguments
            mock_add_instance.assert_any_call(
                [
                    ["name"],
                    ["description"],
                    ["label"],
                    ["type"],
                    ["default"],
                    ["condition"],
                    ["epoch"],
                    ["encounter"],
                ],
                mock_timepoint1,
                mock_design,
                mock_timeline,
            )
            mock_add_instance.assert_any_call(
                [
                    ["name"],
                    ["description"],
                    ["label"],
                    ["type"],
                    ["default"],
                    ["condition"],
                    ["epoch"],
                    ["encounter"],
                ],
                mock_timepoint2,
                mock_design,
                mock_timeline,
            )

            # Verify the result structure
            assert len(result) == 8
            assert result[0][0] == "name"
            assert result[1][0] == "description"
            assert result[2][0] == "label"
            assert result[3][0] == "type"
            assert result[4][0] == "default"
            assert result[5][0] == "condition"
            assert result[6][0] == "epoch"
            assert result[7][0] == "encounter"

    def test_execute_without_timeline(self):
        """Test the execute method without a timeline."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a HeadingsPanel instance
        panel = HeadingsPanel(ct_version)

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
            ["name"],
            ["description"],
            ["label"],
            ["type"],
            ["default"],
            ["condition"],
            ["epoch"],
            ["encounter"],
        ]
        assert result == expected_result

    def test_add_instance_activity(self):
        """Test the _add_instance method with an activity instance."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a HeadingsPanel instance
        panel = HeadingsPanel(ct_version)

        # Create mock objects
        collection = [
            ["name"],
            ["description"],
            ["label"],
            ["type"],
            ["default"],
            ["condition"],
            ["epoch"],
            ["encounter"],
        ]
        mock_instance = MagicMock(spec=ScheduledActivityInstance)
        mock_design = MagicMock()
        mock_timeline = MagicMock(spec=ScheduleTimeline)
        mock_default = MagicMock()
        mock_epoch = MagicMock()
        mock_encounter = MagicMock()

        # Configure the mock objects
        # Set the attributes directly on the mock_instance
        mock_instance.instanceType = "ScheduledActivityInstance"
        mock_instance.defaultConditionId = "default_condition_id"
        mock_instance.epochId = "epoch_id"
        mock_instance.encounterId = "encounter_id"
        
        mock_instance.model_dump.return_value = {
            "name": "Activity1",
            "description": "Activity description",
            "label": "Activity label",
            "instanceType": "ScheduledActivityInstance",
            "defaultConditionId": "default_condition_id",
            "epochId": "epoch_id",
            "encounterId": "encounter_id",
        }
        mock_timeline.find_timepoint.return_value = mock_default
        mock_design.find_epoch.return_value = mock_epoch
        mock_design.find_encounter.return_value = mock_encounter
        mock_default.name = "Default Condition"
        mock_epoch.name = "Epoch1"
        mock_encounter.name = "Encounter1"

        # Call the _add_instance method
        panel._add_instance(collection, mock_instance, mock_design, mock_timeline)

        # Verify the result
        assert collection[0] == ["name", "Activity1"]
        assert collection[1] == ["description", "Activity description"]
        assert collection[2] == ["label", "Activity label"]
        assert collection[3] == ["type", "Activity"]
        assert collection[4] == ["default", mock_default]
        assert collection[5] == ["condition", ""]
        assert collection[6] == ["epoch", "Epoch1"]
        assert collection[7] == ["encounter", "Encounter1"]

    def test_add_instance_decision(self):
        """Test the _add_instance method with a decision instance."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a HeadingsPanel instance
        panel = HeadingsPanel(ct_version)

        # Create mock objects
        collection = [
            ["name"],
            ["description"],
            ["label"],
            ["type"],
            ["default"],
            ["condition"],
            ["epoch"],
            ["encounter"],
        ]
        mock_instance = MagicMock(spec=ScheduledDecisionInstance)
        mock_design = MagicMock()
        mock_timeline = MagicMock(spec=ScheduleTimeline)
        mock_default = MagicMock()

        # Configure the mock objects
        # Set the attributes directly on the mock_instance
        mock_instance.instanceType = "ScheduledDecisionInstance"
        mock_instance.defaultConditionId = "default_condition_id"
        mock_instance.epochId = "epoch_id"
        mock_instance.encounterId = "encounter_id"
        
        mock_instance.model_dump.return_value = {
            "name": "Decision1",
            "description": "Decision description",
            "label": "Decision label",
            "instanceType": "ScheduledDecisionInstance",
            "defaultConditionId": "default_condition_id",
            "epochId": "epoch_id",
            "encounterId": "encounter_id",
        }
        mock_timeline.find_timepoint.return_value = mock_default
        mock_design.find_epoch.return_value = None
        mock_design.find_encounter.return_value = None
        mock_default.name = "Default Condition"

        # Call the _add_instance method
        panel._add_instance(collection, mock_instance, mock_design, mock_timeline)

        # Verify the result
        assert collection[0] == ["name", "Decision1"]
        assert collection[1] == ["description", "Decision description"]
        assert collection[2] == ["label", "Decision label"]
        assert collection[3] == ["type", "Decision"]
        assert collection[4] == ["default", mock_default]
        assert collection[5] == ["condition", ""]
        assert collection[6] == ["epoch", ""]
        assert collection[7] == ["encounter", ""]

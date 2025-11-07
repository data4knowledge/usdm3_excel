from unittest.mock import MagicMock

from usdm3_excel.export.study_design_sheet.high_level_design_panel import (
    HighLevelDesignPanel,
)
from usdm4_excel.export.base.ct_version import CTVersion


class TestHighLevelDesignPanel:
    """Tests for the HighLevelDesignPanel class."""

    def test_init(self):
        """Test initialization of HighLevelDesignPanel."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a HighLevelDesignPanel instance
        panel = HighLevelDesignPanel(ct_version)

        # Verify that the CTVersion instance is stored correctly
        assert panel.ct_version is ct_version
        assert panel.ct_version.versions["test"] == "1.0.0"

    def test_execute(self):
        """Test the execute method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a HighLevelDesignPanel instance
        panel = HighLevelDesignPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()
        mock_epoch1 = MagicMock()
        mock_epoch2 = MagicMock()
        mock_arm1 = MagicMock()
        mock_arm2 = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]

        mock_epoch1.name = "Epoch1"
        mock_epoch2.name = "Epoch2"
        mock_design.epochs = [mock_epoch1, mock_epoch2]

        mock_arm1.name = "Arm1"
        mock_arm2.name = "Arm2"
        mock_design.arms = [mock_arm1, mock_arm2]

        # Call the execute method
        result = panel.execute(mock_study)

        # Verify the result
        # The implementation adds the header row for each epoch
        expected_result = [
            ["Epoch/Arms", "Epoch1", "Epoch2"],
            ["Arm1", "", ""],
            ["Arm2", "", ""],
        ]
        assert result == expected_result

    def test_execute_no_epochs_no_arms(self):
        """Test the execute method with no epochs and no arms."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a HighLevelDesignPanel instance
        panel = HighLevelDesignPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]

        mock_design.epochs = []
        mock_design.arms = []

        # Call the execute method
        result = panel.execute(mock_study)

        # Verify the result
        # When there are no epochs and no arms, the implementation returns an empty list
        expected_result = [['Epoch/Arms']]
        assert result == expected_result

    def test_execute_with_epochs_no_arms(self):
        """Test the execute method with epochs but no arms."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a HighLevelDesignPanel instance
        panel = HighLevelDesignPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()
        mock_epoch1 = MagicMock()
        mock_epoch2 = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]

        mock_epoch1.name = "Epoch1"
        mock_epoch2.name = "Epoch2"
        mock_design.epochs = [mock_epoch1, mock_epoch2]

        mock_design.arms = []

        # Call the execute method
        result = panel.execute(mock_study)

        # Verify the result
        # The implementation adds the header row for each epoch
        expected_result = [
            ["Epoch/Arms", "Epoch1", "Epoch2"],
        ]
        assert result == expected_result

    def test_execute_no_epochs_with_arms(self):
        """Test the execute method with no epochs but with arms."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a HighLevelDesignPanel instance
        panel = HighLevelDesignPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()
        mock_arm1 = MagicMock()
        mock_arm2 = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]

        mock_design.epochs = []

        mock_arm1.name = "Arm1"
        mock_arm2.name = "Arm2"
        mock_design.arms = [mock_arm1, mock_arm2]

        # Call the execute method
        result = panel.execute(mock_study)

        # Verify the result
        # The implementation doesn't add the header row when there are no epochs
        expected_result = [['Epoch/Arms'], ['Arm1'], ['Arm2']]
        assert result == expected_result

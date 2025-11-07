from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_design_sheet.main_panel import MainPanel
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4.api.study_design import StudyDesign


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

    def test_execute(self):
        """Test the execute method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a MainPanel instance
        panel = MainPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock(spec=StudyDesign)
        mock_blinding_schema = MagicMock()
        mock_intent_type1 = MagicMock()
        mock_intent_type2 = MagicMock()
        mock_sub_type1 = MagicMock()
        mock_sub_type2 = MagicMock()
        mock_model = MagicMock()
        mock_characteristic1 = MagicMock()
        mock_characteristic2 = MagicMock()
        mock_study_type = MagicMock()
        mock_study_phase = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyDesigns = [mock_design]

        mock_design.name = "Test Design"
        mock_design.description = "Test Description"
        mock_design.rationale = "Test Rationale"
        mock_design.blindingSchema = mock_blinding_schema
        mock_design.intentTypes = [mock_intent_type1, mock_intent_type2]
        mock_design.subTypes = [mock_sub_type1, mock_sub_type2]
        mock_design.model = mock_model
        mock_design.characteristics = [mock_characteristic1, mock_characteristic2]
        mock_design.studyType = mock_study_type
        mock_design.studyPhase = mock_study_phase

        # Mock the helper methods
        with (
            patch.object(panel, "_tas", return_value="TA1, TA2") as mock_tas,
            patch.object(panel, "_pt_from_code") as mock_pt_from_code,
            patch.object(panel, "_pt_from_alias_code") as mock_pt_from_alias_code,
        ):
            # Configure the _pt_from_code mock to return different values for different inputs
            mock_pt_from_code.side_effect = lambda x: {
                mock_intent_type1: "Treatment",
                mock_intent_type2: "Prevention",
                mock_sub_type1: "Safety",
                mock_sub_type2: "Efficacy",
                mock_model: "Parallel",
                mock_characteristic1: "Randomized",
                mock_characteristic2: "Controlled",
                mock_study_type: "Interventional",
            }[x]
            
            # Configure the _pt_from_alias_code mock to return different values for different inputs
            mock_pt_from_alias_code.side_effect = lambda x: {
                mock_blinding_schema: "Double Blind",
                mock_study_phase: "Phase 1",
            }[x]

            # Call the execute method
            result = panel.execute(mock_study)

            # Verify that the helper methods were called with the correct arguments
            mock_tas.assert_called_once_with(mock_design)
            mock_pt_from_alias_code.assert_any_call(mock_blinding_schema)
            mock_pt_from_code.assert_any_call(mock_intent_type1)
            mock_pt_from_code.assert_any_call(mock_intent_type2)
            mock_pt_from_code.assert_any_call(mock_sub_type1)
            mock_pt_from_code.assert_any_call(mock_sub_type2)
            mock_pt_from_code.assert_any_call(mock_model)
            mock_pt_from_code.assert_any_call(mock_characteristic1)
            mock_pt_from_code.assert_any_call(mock_characteristic2)
            # mock_pt_from_code.assert_any_call(mock_study_type)
            # mock_pt_from_alias_code.assert_any_call(mock_study_phase)

            # Verify the result
            expected_result = [
                ["studyDesignName", "Test Design"],
                ["studyDesignDescription", "Test Description"],
                ["therapeuticAreas", "TA1, TA2"],
                ["studyDesignRationale", "Test Rationale"],
                ["studyDesignBlindingScheme", "Double Blind"],
                ["trialIntentTypes", "Treatment, Prevention"],
                ["trialSubTypes", "Safety, Efficacy"],
                ["interventionModel", "Parallel"],
                ["masking", ""],
                ["characteristics", "Randomized, Controlled"],
                ["mainTimeline", "mainTimeline"],
                ["otherTimelines", ""],
                # ["studyType", "Interventional"],
                # ["studyPhase", "Phase 1"],
                # ["spare", ""],
            ]
            assert result == expected_result

    def test_tas(self):
        """Test the _tas method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a MainPanel instance
        panel = MainPanel(ct_version)

        # Create a mock StudyDesign
        mock_design = MagicMock(spec=StudyDesign)

        # Configure the mock StudyDesign
        mock_area1 = MagicMock()
        mock_area1.codeSystem = "CodeSystem1"
        mock_area1.codeSystemVersion = "1.0.0"
        mock_area1.code = "Code1"
        mock_area1.decode = "Decode1"

        mock_area2 = MagicMock()
        mock_area2.codeSystem = "CodeSystem2"
        mock_area2.codeSystemVersion = "2.0.0"
        mock_area2.code = "Code2"
        mock_area2.decode = "Decode2"

        mock_design.therapeuticAreas = [mock_area1, mock_area2]

        # Call the _tas method
        result = panel._tas(mock_design)

        # Verify that the CTVersion's add method was called with the correct arguments
        assert ct_version.versions["CodeSystem1"] == "1.0.0"
        assert ct_version.versions["CodeSystem2"] == "2.0.0"

        # Verify the result
        expected_result = "CodeSystem1: Code1 = Decode1, CodeSystem2: Code2 = Decode2"
        assert result == expected_result

    def test_tas_empty(self):
        """Test the _tas method with no therapeutic areas."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a MainPanel instance
        panel = MainPanel(ct_version)

        # Create a mock StudyDesign with no therapeutic areas
        mock_design = MagicMock(spec=StudyDesign)
        mock_design.therapeuticAreas = []

        # Call the _tas method
        result = panel._tas(mock_design)

        # Verify the result
        assert result == ""

from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_sheet.main_panel import MainPanel
from usdm4_excel.export.base.ct_version import CTVersion


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

        # Create mock objects for Study and StudyVersion
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_design = MagicMock()
        mock_phase = MagicMock()
        mock_document = MagicMock()
        mock_doc_version = MagicMock()
        mock_status = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_study.name = "Test Study"
        mock_study.documentedBy = [mock_document]

        mock_version.versionIdentifier = "1.0.0"
        mock_version.studyDesigns = [mock_design]
        mock_version.rationale = "Test Rationale"

        mock_design.phase.return_value = mock_phase
        mock_phase.decode = "Phase 1"

        mock_version.acronym_text.return_value = "TEST"
        mock_version.short_title_text.return_value = "Short Title"
        mock_version.official_title_text.return_value = "Official Title"

        mock_document.versions = [mock_doc_version]
        mock_doc_version.version = "1.0.0"
        mock_doc_version.status = mock_status
        mock_status.decode = "Final"

        # Mock the _business_tas method
        with patch.object(
            panel, "_business_tas", return_value="TA1, TA2"
        ) as mock_business_tas:
            # Call the execute method
            result = panel.execute(mock_study)

            # Verify that the _business_tas method was called with the mock version
            mock_business_tas.assert_called_once_with(mock_version)

            # Verify the result
            expected_result = [
                ["name", "Test Study"],
                ["studyTitle", ""],
                ["studyVersion", "1.0.0"],
                ["studyType", ""],
                ["studyPhase", "Phase 1"],
                ["studyAcronym", "TEST"],
                ["studyRationale", "Test Rationale"],
                ["businessTherapeuticAreas", "TA1, TA2"],
                ["briefTitle", "Short Title"],
                ["officialTitle", "Official Title"],
                ["publicTitle", ""],
                ["scientificTitle", ""],
                ["protocolVersion", "1.0.0"],
                ["protocolStatus", "Final"],
            ]
            assert result == expected_result

    def test_business_tas(self):
        """Test the _business_tas method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a MainPanel instance
        panel = MainPanel(ct_version)

        # Create a mock StudyVersion
        mock_version = MagicMock()

        # Configure the mock StudyVersion
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

        mock_version.businessTherapeuticAreas = [mock_area1, mock_area2]

        # Call the _business_tas method
        result = panel._business_tas(mock_version)

        # Verify that the CTVersion's add method was called with the correct arguments
        assert ct_version.versions["CodeSystem1"] == "1.0.0"
        assert ct_version.versions["CodeSystem2"] == "2.0.0"

        # Verify the result
        expected_result = "CodeSystem1: Code1 = Decode1, CodeSystem2: Code2 = Decode2"
        assert result == expected_result

    def test_business_tas_empty(self):
        """Test the _business_tas method with no therapeutic areas."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a MainPanel instance
        panel = MainPanel(ct_version)

        # Create a mock StudyVersion with no therapeutic areas
        mock_version = MagicMock()
        mock_version.businessTherapeuticAreas = []

        # Call the _business_tas method
        result = panel._business_tas(mock_version)

        # Verify the result
        assert result == ""

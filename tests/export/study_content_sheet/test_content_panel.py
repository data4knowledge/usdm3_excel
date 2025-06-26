from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_content_sheet.content_panel import ContentPanel
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4.api.narrative_content import NarrativeContent, NarrativeContentItem
from usdm4.api.study_definition_document_version import StudyDefinitionDocumentVersion


class TestContentPanel:
    """Tests for the ContentPanel class."""

    def test_init(self):
        """Test initialization of ContentPanel."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a ContentPanel instance
        panel = ContentPanel(ct_version)

        # Verify that the CTVersion instance is stored correctly
        assert panel.ct_version is ct_version
        assert panel.ct_version.versions["test"] == "1.0.0"

    def test_execute(self):
        """Test the execute method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a ContentPanel instance
        panel = ContentPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_doc_version = MagicMock(spec=StudyDefinitionDocumentVersion)
        mock_narrative_content = MagicMock(spec=NarrativeContent)

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.documentVersionIds = ["doc_version_1"]
        mock_doc_version.contents = [mock_narrative_content]

        # Mock the helper methods
        with (
            patch.object(
                panel, "_find_document_version", return_value=mock_doc_version
            ) as mock_find_document_version,
            patch.object(panel, "_add_content") as mock_add_content,
        ):
            # Call the execute method
            panel.execute(mock_study)

            # Verify that the helper methods were called with the correct arguments
            mock_find_document_version.assert_called_once_with(
                mock_study, "doc_version_1"
            )
            mock_add_content.assert_called_once_with(
                [], mock_narrative_content, mock_version
            )

    def test_execute_no_document_version(self):
        """Test the execute method when no document version is found."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a ContentPanel instance
        panel = ContentPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.documentVersionIds = ["doc_version_1"]

        # Mock the helper methods
        with (
            patch.object(
                panel, "_find_document_version", return_value=None
            ) as mock_find_document_version,
            patch.object(panel, "_add_content") as mock_add_content,
        ):
            # Call the execute method
            panel.execute(mock_study)

            # Verify that the helper methods were called with the correct arguments
            mock_find_document_version.assert_called_once_with(
                mock_study, "doc_version_1"
            )
            mock_add_content.assert_not_called()

    def test_add_content(self):
        """Test the _add_content method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a ContentPanel instance
        panel = ContentPanel(ct_version)

        # Create mock objects
        collection = []
        mock_narrative_content = MagicMock(spec=NarrativeContent)
        mock_version = MagicMock()
        mock_content_item = MagicMock(spec=NarrativeContentItem)

        # Configure the mock objects
        mock_narrative_content.model_dump.return_value = {
            "name": "Content1",
            "sectionNumber": "1.0",
            "sectionTitle": "Introduction",
            "contentItemId": "content_item_1",
        }
        mock_narrative_content.contentItemId = "content_item_1"
        mock_content_item.text = "This is the introduction text."

        # Mock the helper method
        with patch.object(
            panel, "_find_content_item", return_value=mock_content_item
        ) as mock_find_content_item:
            # Call the _add_content method
            panel._add_content(collection, mock_narrative_content, mock_version)

            # Verify that the helper method was called with the correct arguments
            mock_find_content_item.assert_called_once_with(
                mock_version, "content_item_1"
            )

            # Verify that the collection was updated correctly
            assert len(collection) == 1
            assert collection[0]["name"] == "Content1"
            assert collection[0]["sectionNumber"] == "1.0"
            assert collection[0]["sectionTitle"] == "Introduction"
            assert collection[0]["text"] == "This is the introduction text."

    def test_add_content_no_content_item(self):
        """Test the _add_content method when no content item is found."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a ContentPanel instance
        panel = ContentPanel(ct_version)

        # Create mock objects
        collection = []
        mock_narrative_content = MagicMock(spec=NarrativeContent)
        mock_version = MagicMock()

        # Configure the mock objects
        mock_narrative_content.model_dump.return_value = {
            "name": "Content1",
            "sectionNumber": "1.0",
            "sectionTitle": "Introduction",
            "contentItemId": "content_item_1",
        }
        mock_narrative_content.contentItemId = "content_item_1"

        # Mock the helper method
        with patch.object(
            panel, "_find_content_item", return_value=None
        ) as mock_find_content_item:
            # Call the _add_content method
            panel._add_content(collection, mock_narrative_content, mock_version)

            # Verify that the helper method was called with the correct arguments
            mock_find_content_item.assert_called_once_with(
                mock_version, "content_item_1"
            )

            # Verify that the collection was updated correctly
            assert len(collection) == 1
            assert collection[0]["name"] == "Content1"
            assert collection[0]["sectionNumber"] == "1.0"
            assert collection[0]["sectionTitle"] == "Introduction"
            assert collection[0]["text"] is None

    def test_find_document_version(self):
        """Test the _find_document_version method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a ContentPanel instance
        panel = ContentPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_doc = MagicMock()
        mock_doc_version = MagicMock(spec=StudyDefinitionDocumentVersion)

        # Configure the mock objects
        mock_study.documentedBy = [mock_doc]
        mock_doc.versions = [mock_doc_version]
        mock_doc_version.id = "doc_version_1"

        # Call the _find_document_version method
        result = panel._find_document_version(mock_study, "doc_version_1")

        # Verify the result
        assert result is mock_doc_version

    def test_find_document_version_not_found(self):
        """Test the _find_document_version method when the document version is not found."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a ContentPanel instance
        panel = ContentPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_doc = MagicMock()
        mock_doc_version = MagicMock(spec=StudyDefinitionDocumentVersion)

        # Configure the mock objects
        mock_study.documentedBy = [mock_doc]
        mock_doc.versions = [mock_doc_version]
        mock_doc_version.id = "doc_version_1"

        # Call the _find_document_version method with a non-existent ID
        result = panel._find_document_version(mock_study, "doc_version_2")

        # Verify the result
        assert result is None

    def test_find_content_item(self):
        """Test the _find_content_item method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a ContentPanel instance
        panel = ContentPanel(ct_version)

        # Create mock objects
        mock_version = MagicMock()
        mock_content_item = MagicMock(spec=NarrativeContentItem)

        # Configure the mock objects
        mock_version.narrativeContentItems = [mock_content_item]
        mock_content_item.id = "content_item_1"

        # Call the _find_content_item method
        result = panel._find_content_item(mock_version, "content_item_1")

        # Verify the result
        assert result is mock_content_item

    def test_find_content_item_not_found(self):
        """Test the _find_content_item method when the content item is not found."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a ContentPanel instance
        panel = ContentPanel(ct_version)

        # Create mock objects
        mock_version = MagicMock()
        mock_content_item = MagicMock(spec=NarrativeContentItem)

        # Configure the mock objects
        mock_version.narrativeContentItems = [mock_content_item]
        mock_content_item.id = "content_item_1"

        # Call the _find_content_item method with a non-existent ID
        result = panel._find_content_item(mock_version, "content_item_2")

        # Verify the result
        assert result is None

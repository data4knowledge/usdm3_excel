from usdm4.api.study import Study
from usdm4.api.identifier import StudyIdentifier
from usdm4.api.address import Address
from usdm4.api.organization import Organization
from usdm4.api.study_version import StudyVersion
from usdm3_excel.export.base.collection_panel import CollectionPanel


class IdentifiersPanel(CollectionPanel):
    def execute(self, study: Study) -> list[list[dict]]:
        collection = []
        for version in study.versions:
            for item in version.studyIdentifiers:
                self._add_identifier(collection, item, version)
        return super().execute(
            collection,
            [
                "organizationIdentifierScheme",
                "organizationIdentifier",
                "organizationName",
                "organizationType",
                "studyIdentifier",
                "organizationAddress",
            ],
        )

    def _add_identifier(
        self, collection: list, item: StudyIdentifier, version: StudyVersion
    ):
        org: Organization = version.organization(item.scopeId)
        data = org.model_dump()
        data["organizationIdentifierScheme"] = data["identifierScheme"]
        data["organizationIdentifier"] = data["identifier"]
        data["organizationName"] = data["name"]
        data["organizationType"] = self._pt_from_code(org.type)
        data["organizationAddress"] = self._from_address(org.legalAddress)
        data["studyIdentifier"] = item.text
        collection.append(data)

    def _from_address(self, address: Address):
        if address is None:
            return "|||||"
        items = address.lines
        items.append(address.district)
        items.append(address.city)
        items.append(address.state)
        items.append(address.postalCode)
        code = address.country.code.code if address.country else ""
        items.append(code)
        return ("|").join(items)

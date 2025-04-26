from usdm4.api.study import Study
from usdm4.api.study_arm import StudyArm
from usdm3_excel.export.base.collection_panel import CollectionPanel


class ArmsPanel(CollectionPanel):
    def execute(self, study: Study) -> list[list[dict]]:
        collection = []
        for version in study.versions:
            for design in version.studyDesigns:
                for item in design.arms:
                    self._add_activity(collection, item)
        return super().execute(
            collection,
            [
                "name",
                "description",
                "label",
                "type",
                "dataOriginDescription",
                "dataOriginType",
            ],
        )

    def _add_activity(self, collection: list, item: StudyArm):
        data = item.model_dump()
        data["type"] = self._pt_from_code(item.type)
        data["dataOriginType"] = self._pt_from_code(item.dataOriginType)
        collection.append(data)

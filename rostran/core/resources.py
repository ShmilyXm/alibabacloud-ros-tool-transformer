from openpyxl.cell.cell import Cell

from .exceptions import InvalidTemplateResource, InvalidTemplateParameter
from .properties import Properties
from .utils import get_and_validate_cell


class Resource:

    PROPERTIES_ = (TYPE, PROPERTIES, DEPENDS_ON, CONDITION, DELETION_POLICY) = (
        "Type",
        "Properties",
        "DependsOn",
        "Condition",
        "DeletionPolicy",
    )

    def __init__(
        self,
        resource_id,
        resource_type,
        properties: Properties = None,
        depends_on=None,
        condition=None,
        deletion_policy=None,
    ):
        self.resource_id = resource_id
        self.type = resource_type
        self.properties = properties or Properties()
        self.depends_on = depends_on
        self.condition = condition
        self.deletion_policy = deletion_policy

    @classmethod
    def initialize_from_excel(cls, header_cell: Cell, data_cell: Cell):
        # resource type
        orig_resource_type = header_cell.value
        resource_type = get_and_validate_cell(header_cell, InvalidTemplateResource)

        if not resource_type.startswith("ALIYUN::"):
            resource_type = f"ALIYUN::{resource_type}"

        if len(resource_type.split("::")) != 3:
            raise InvalidTemplateResource(
                name=orig_resource_type,
                reason=f"Value of {header_cell} must be format of "
                f"{{Product}}::{{Resource}} or ALIYUN::{{Product}}::{{Resource}}",
            )
        # resource id
        resource_id = data_cell.value
        if not isinstance(resource_id, str):
            raise InvalidTemplateResource(
                name=resource_id, reason=f"Value of {data_cell} must be str"
            )

        if not resource_id:
            raise InvalidTemplateResource(
                name=resource_id, reason=f"Value of {data_cell} must not be empty"
            )

        return cls(resource_id=resource_id, resource_type=resource_type)


class Resources(dict):
    def add(self, resource: Resource):
        if resource.resource_id is None:
            raise InvalidTemplateParameter(
                resource_id=resource.resource_id,
                reason="Resource logical id should not be None",
            )

        self[resource.resource_id] = resource

    def as_dict(self) -> dict:
        data = {}
        for key, resource in self.items():
            resource: Resource
            value = {
                Resource.TYPE: resource.type,
                Resource.PROPERTIES: resource.properties.resolve().as_dict(),
            }
            if resource.depends_on:
                value[Resource.DEPENDS_ON] = resource.depends_on
            if resource.condition:
                value[Resource.CONDITION] = resource.condition
            if resource.deletion_policy:
                value[Resource.DELETION_POLICY] = resource.deletion_policy

            data[key] = value

        return data

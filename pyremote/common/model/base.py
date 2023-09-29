import json
from typing import Any, Dict
from pyremote.common.model import utils, excpetions


class BaseModel:
    """
    This class is used for presenting data(just dataclass with type validation.)
    This can be modified for database and storing cases.
    """
    # TODO: Support union types validation.
    def __init__(self, **kwargs):
        self.__DATA = self._validate_required_data(**kwargs)
        self._validate_fields_type(**self.data)
        self._set_attrs(**self.data)

    def _validate_required_data(self, **kwargs) -> Dict[str, Any]:
        # TODO:HANDLE EXTRA FIELDS
        fields = {}
        for cls_field, cls_field_type in self.__annotations__.items():
            expected_type = utils.get_exact_type(cls_field_type)
            if not kwargs.__contains__(cls_field):
                if hasattr(self, cls_field):
                    fields[cls_field] = getattr(self, cls_field)
                elif expected_type is None:
                    fields[cls_field] = None
                else:
                    raise excpetions.NotProvidedFieldException(f'Field "{cls_field}" is required and not provided.')
            else:
                fields[cls_field] = kwargs[cls_field]

        return fields

    def _validate_fields_type(self, **fields) -> None:
        for cls_field, cls_field_type in self.__annotations__.items():
            expected_type = utils.get_exact_type(cls_field_type)
            # TODO: The validation process needs improvement.
            if expected_type is None and \
                    fields[cls_field] is not None or \
                    not isinstance(fields[cls_field], expected_type):
                raise excpetions.FiledTypeException(
                    f'Field "{cls_field}" should be type of "{cls_field_type}" and not "{type(fields.get(cls_field))}".'
                )

    def _set_attrs(self, **attrs) -> None:
        for key, value in attrs.items():
            setattr(self, key, value)

    @property
    def data(self) -> Dict:
        return self.__DATA

    def as_json(self, start: str = '', end: str = '') -> str:
        return str(start) + json.dumps(self.data) + str(end)

    @classmethod
    def from_json(cls, data: str) -> 'BaseModel':
        return cls(**json.loads(data))

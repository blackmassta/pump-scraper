import operator as op

from enum import Enum
from datetime import datetime
from typing import TypeVar, Union, Callable, Generic, Any, List, Tuple, Optional

from pydantic import BaseModel


T = TypeVar("T")
FieldType = Union[str, Callable[[T], Union[str, float, datetime, set, list]]]


class OperatorEnum(str, Enum):
    EQ = "=="
    NEQ = "!="
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="
    IN = "IN"
    NOT_IN = "NOT IN"
    NULL = "IS NULL"
    NOT_NULL = "IS NOT NULL"

    def has_value(self):
        return self.value not in [OperatorEnum.NULL, OperatorEnum.NOT_NULL]

    def to_sql(self):
        if self == OperatorEnum.EQ:
            return "="
        elif self == OperatorEnum.NEQ:
            return "<>"
        else:
            return self.value


class ConjunctionEnum(str, Enum):
    AND = "AND"
    OR = "OR"


class ConditionBase(Generic[T]):
    def __or__(self, other: "ConditionBase[T]") -> "ConditionGroup[T]":
        return ConditionGroup(left=self, conjunction=ConjunctionEnum.OR, right=other)

    def __and__(self, other: "ConditionBase[T]") -> "ConditionGroup[T]":
        return ConditionGroup(left=self, conjunction=ConjunctionEnum.AND, right=other)

    def evaluate(self, obj: T) -> bool:
        pass

    def to_sql(self, obj: T) -> Tuple[str, List[Any]]:
        pass


class ConditionConstant(ConditionBase[T]):
    def __init__(self, is_true: bool = True):
        self.is_true = is_true

    def evaluate(self, obj: T) -> bool:
        return self.is_true

    def to_sql(self, obj: T) -> Tuple[str, List[Any]]:
        return ("1=1", []) if self.is_true else ("1=0", [])


class Condition(ConditionBase[T]):
    def __init__(self, field: FieldType, operator: OperatorEnum, value: Optional[Union[str, float, datetime, set, list]]):
        self.field = field
        self.operator = operator
        self.value = value

        if value is None and operator.has_value():
            raise Exception(f"Value is required for operator: {operator}")

        # If `field` is a string, dynamically get attribute
        if isinstance(field, str):
            self.getter: Callable[[T], Union[str, float, datetime, set, list]] = op.attrgetter(field)
        else:
            self.getter = field  # Use lambda function directly

    def evaluate(self, obj: T) -> bool:
        """Evaluates the condition against an object of type T."""
        field_value = self.getter(obj)

        match self.operator:
            case OperatorEnum.EQ:
                return field_value == self.value
            case OperatorEnum.NEQ:
                return field_value != self.value
            case OperatorEnum.GT:
                return field_value > self.value
            case OperatorEnum.LT:
                return field_value < self.value
            case OperatorEnum.GTE:
                return field_value >= self.value
            case OperatorEnum.LTE:
                return field_value <= self.value
            case OperatorEnum.IN:
                return field_value in self.value if isinstance(self.value, (set, list)) else False
            case OperatorEnum.NOT_IN:
                return field_value not in self.value if isinstance(self.value, (set, list)) else False
            case OperatorEnum.NULL:
                return field_value is None
            case OperatorEnum.NOT_NULL:
                return field_value is not None
            case _:
                raise ValueError(f"Unsupported operator: {self.operator}")

    def to_sql(self, obj: T) -> Tuple[str, List[Any]]:
        """Converts a predicate function into an SQL WHERE clause."""
        if not isinstance(self.field, str):
            raise Exception("Unsupported where predicate. Field must be a string")

        field_name = self.field
        operator_value = self.operator.to_sql()

        if self.operator.has_value():
            placeholders = '?'
            field_value = self.getter(obj)
            if isinstance(field_value, (list, set)):
                placeholders = "(" + ", ".join("?" * len(field_value)) + ")"

            return f"{field_name} {operator_value} {placeholders}", [field_value]
        else:
            return f"{field_name} {operator_value}", []


class ConditionGroup(ConditionBase[T]):
    def __init__(self, left: ConditionBase[T], conjunction: ConjunctionEnum, right: ConditionBase[T] = None):
        self.left = left
        self.right = right
        self.conjunction = conjunction

    def evaluate(self, obj: T) -> bool:
        """Evaluate the condition group recursively."""

        def default():
            return True if self.conjunction == ConjunctionEnum.AND else False

        left_result = self.left.evaluate(obj)
        right_result = self.right.evaluate(obj) if self.right else default()

        if self.conjunction == ConjunctionEnum.AND:
            return left_result and right_result
        else:
            return left_result or right_result

    def to_sql(self, obj: BaseModel) -> Tuple[str, List[Any]]:
        """Converts a predicate function into an SQL WHERE clause."""
        def default() -> Tuple[str, List[Any]]:
            return "1=1" if self.conjunction == ConjunctionEnum.AND else "1=0", []

        left_where, left_bindings = self.left.to_sql(obj)
        right_where, right_bindings = self.right.to_sql(obj) if self.right else default()
        return f"({left_where}) {self.conjunction.value} ({right_where})", (left_bindings + right_bindings)


# Example Usage:
if __name__ == "__main__":
    # Using a string field
    condition1 = Condition("age", OperatorEnum.GT, 18)
    condition2 = Condition("country", OperatorEnum.EQ, "USA")
    condition3 = Condition("status", OperatorEnum.IN, {"active", "pending"})

    # Using a lambda field
    condition4 = Condition(lambda u: u.age, OperatorEnum.LT, 30)

    group = condition1 & condition2 | condition3 & condition4


    class MyModel(BaseModel):
        age: int
        country: str
        status: str


    obj1 = MyModel(age=25, country="USA", status="active")  # Should be True
    obj2 = MyModel(age=15, country="Canada", status="inactive")  # Should be False
    obj3 = MyModel(age=29, country="Canada", status="pending")  # Should be True (due to condition4)

    print(group.evaluate(obj1))  # True
    print(group.evaluate(obj2))  # False
    print(group.evaluate(obj3))  # True

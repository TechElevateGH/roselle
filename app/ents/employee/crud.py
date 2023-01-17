from typing import Optional
import uuid
from app.core.security import security

from app.ents.base.crud import CRUDBase
from app.ents.employee.models import Employee
from app.ents.employee.schema import (
    EmployeeInDB,
    EmployeeCreateInput,
    EmployeeRead,
)


class EmployeeCRUD(CRUDBase[Employee, EmployeeInDB, EmployeeRead]):
    def __create_full_name(self, data: EmployeeCreateInput):
        """Creates the full name of the employee."""
        return data.first_name + " " + data.middle_name + " " + data.last_name

    def read(self, employee_id: str) -> Optional[EmployeeRead]:
        """Read employee with id `employee_id`."""
        return super().read(employee_id)

    def read_by_email(self, employee_email: str) -> Optional[EmployeeInDB]:
        """Read employee with email `employee_email`."""
        return Employee.query.filter_by(email=employee_email).first()

    def read_multi(self) -> list[EmployeeRead]:
        """Read all employees."""
        return super().read_multi()

    def create(self, data: EmployeeCreateInput) -> EmployeeRead:
        """Create an employee with `data`."""

        employee_obj = EmployeeInDB(
            **{
                "public_id": str(uuid.uuid4()),
                "hashed_password": security.hash_password(data.password),
                "full_name": self.__create_full_name(data),
            },
            **data.dict(
                exclude={"password"},
            )
        )
        return super().create(employee_obj)


crud = EmployeeCRUD(Employee, EmployeeRead)

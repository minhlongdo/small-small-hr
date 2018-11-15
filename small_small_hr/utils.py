"""
Utils module for small small hr
"""
from django.conf import settings

from small_small_hr.models import AnnualLeave, Leave


def get_carry_over(staffprofile: object, year: int, leave_type: str):
    """
    Get carried over leave days
    """
    # pylint: disable=no-member
    if leave_type == Leave.REGULAR:
        previous_obj = AnnualLeave.objects.filter(
            staff=staffprofile, year=year - 1, leave_type=leave_type).first()
        if previous_obj:
            remaining = previous_obj.get_available_leave_days()
            max_carry_over = settings.SSHR_MAX_CARRY_OVER
            if remaining > max_carry_over:
                carry_over = max_carry_over
            else:
                carry_over = remaining

            return carry_over

    return 0


def create_annual_leave(staffprofile: object, year: int, leave_type: str):
    """
    Creates an annuall leave object for the staff member
    """
    # pylint: disable=no-member
    try:
        annual_leave = AnnualLeave.objects.get(
            staff=staffprofile, year=year, leave_type=leave_type)
    except AnnualLeave.DoesNotExist:
        carry_over = get_carry_over(staffprofile, year, leave_type)

        if leave_type == Leave.REGULAR:
            allowed_days = staffprofile.leave_days
        elif leave_type == Leave.SICK:
            allowed_days = staffprofile.sick_days

        annual_leave = AnnualLeave(
            staff=staffprofile,
            year=year,
            leave_type=leave_type,
            allowed_days=allowed_days,
            carried_over_days=carry_over
        )
        annual_leave.save()

    return annual_leave

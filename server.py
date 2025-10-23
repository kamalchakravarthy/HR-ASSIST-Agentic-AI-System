from mcp.server.fastmcp import FastMCP 
from typing import List, Dict 
from HRMS import *
from emails import EmailSender
from utils import seed_services
from dotenv import load_dotenv 
import os

load_dotenv()

mcp = FastMCP("hr-assist-project")

employee_manager = EmployeeManager()
leave_manager = LeaveManager()
meeting_manager = MeetingManager()
ticket_manager = TicketManager()

seed_services(employee_manager, leave_manager, meeting_manager, ticket_manager)

emailer = EmailSender(
    smtp_server="smtp.gmail.com",
    port=587,
    username=os.getenv("EMAIL"),
    password=os.getenv("APP_PASSWORD"),
    use_tls=True,
)


@mcp.tool()
def add_employee(emp_name:str,manager_id:str,email:str) -> str:
    """
    Add a new employee to the HRMS system.
    :param emp_name: Employee name
    :param manager_id: Manager ID (optional)
    :param email: Email ID
    :return: Confirmation message
    """   
    emp = EmployeeCreate(
        emp_id=employee_manager.get_next_emp_id(),
        name = emp_name,
        manager_id=manager_id,
        email = email
    )

    employee_manager.add_employee(emp)
    return f"{emp_name} was succesfully added tp HRMS system."

@mcp.tool()
def get_employee_details(name:str) -> Dict[str,str]:
    """
    Get employee details by name.
    :param name: Name of the employee
    :return: Dict[str,str]
    """

    matches = employee_manager.search_employee_by_name(name)

    if len(matches) == 0:
        raise ValueError(f"No employees found with the name: {name}")
    
    emp_id = matches[0]
    emp_details = employee_manager.get_employee_details(emp_id)
    return emp_details

@mcp.tool()
def send_email(to_emails: List[str],subject:str, body:str, html:bool =False) -> str:
    """
    Send emails with subject, body from to_emails.
    :param to_emails: List to receiver email ID's
    :param subject: Subject of the email
    :param body: Body of the email
    :return: str
    """

    emailer.send_email(subject,body,to_emails, from_email=emailer.username,html=html)
    return "Email sent successfully"

@mcp.tool()
def create_ticket(emp_id:str, item: str, reason:str) -> str: 
    """
    Create a ticket for buying required items for an employee.
    :param emp_id: Employee ID
    :param item: Item requested(Laptop,keyboard,mouse,bag etc.)
    :param reason: Reason for request
    :return: Confirmation message
    """
    ticket_item = TicketCreate(emp_id=emp_id, item=item, reason=reason)
    return ticket_manager.create_ticket(ticket_item)

@mcp.tool()
def update_ticket_status(ticket_id:str,status:str) -> str: 
    """
    Update the status of the ticket.
    :param ticket_id: Ticket ID
    :param status: New status of the ticket
    :return: Confirmation message
    """
    ticket_item = TicketStatusUpdate(status)
    return ticket_manager.update_ticket_status(ticket_item,ticket_id)

@mcp.tool()
def list_tickets(emp_id:str,status:str) -> List[Dict[str, str]]:
    """
    List the tickets of the employee.
    :param emp_id: Employee ID
    :param status: Ticket Status (Optional)
    :return: List of the tickets
    """
    return ticket_manager.list_tickets(emp_id,status)

@mcp.tool()
def schedule_meeting(employee_id: str, meeting_datetime: datetime, topic: str) -> str:
    """
    Schedule a meeting for an employee.
    :param employee_id: Employee ID
    :param meeting_datetime: Date and time of the meeting in python datetime format
    :param topic: Topic of the meeting
    :return: Confirmation message
    """
    meeting_req = MeetingCreate(
        emp_id=employee_id,
        meeting_dt=meeting_datetime,
        topic=topic
    )
    return meeting_manager.schedule_meeting(meeting_req)


@mcp.tool()
def get_meetings(employee_id: str) -> str:
    """
    Get the list of meetings scheduled for an employee.
    :param employee_id: Employee ID
    :return: List of meetings
    """
    return meeting_manager.get_meetings(employee_id)


@mcp.tool()
def cancel_meeting(employee_id: str, meeting_datetime: datetime, topic: str) -> str:
    """
    Cancel a scheduled meeting for an employee.
    :param employee_id: Employee ID
    :param meeting_datetime: Date and time of the meeting in python datetime format
    :param topic: Topic of the meeting (optional)
    :return: Confirmation message
    """
    meeting_req = MeetingCancelRequest(
        emp_id=employee_id,
        meeting_dt=meeting_datetime,
        topic=topic
    )
    return meeting_manager.cancel_meeting(meeting_req)

@mcp.tool()
def get_employee_leave_balance(emp_id: str) -> str:
    """
    Get the leave balance of an employee.
    :param emp_id: Employee ID
    :return: Leave balance message
    """
    return leave_manager.get_leave_balance(emp_id)

@mcp.tool()
def apply_leave(emp_id: str, leave_dates: list) -> str:
    """
    Apply for leave for an employee.
    :param emp_id: Employee ID
    :param leave_dates: List of leave dates
    :return: Leave application status message
    """
    req = LeaveApplyRequest(emp_id=emp_id, leave_dates=leave_dates)
    return leave_manager.apply_leave(req)


@mcp.tool()
def get_leave_history(emp_id: str) -> str:
    """
    Get the leave history of an employee.
    :param emp_id: Employee ID
    :return: Leave history message
    """
    return leave_manager.get_leave_history(emp_id)

@mcp.prompt("onboard_new_employee") 
def onboard_new_employee(emp_name: str, manager_name: str):
    return f"""
    Onboard a new employee with the following details:
    -Name: {emp_name}
    -Manager Name: {manager_name}
    Steps to follow:
    1. Add employee to the HRMS system.
    2. Send a welcome email to the employee with their login credentials. (Format: employee_name@tcs.com)
    3. Notify the manager about the new employee's onboarding.
    4. Raise tickets for new laptop, id card, bag, and other necessary equipment.
    5. Schedule an introductory meeting between the employee and the manager.
    """

if __name__ == "__main__":
    print(type(employee_manager.get_next_emp_id()))
import frappe
from malaria_partners.transport.transport_utils import send_compliance_reminders

def run():
    """Send reminders for statutory compliance."""
    print('start \n')
    send_compliance_reminders()
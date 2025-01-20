import frappe

@frappe.whitelist()
def updated_odometer_value(vehical, new_odometer_value):
    check_permissions()
    frappe.db.set_value('Vehicle', vehical, 'last_odometer', new_odometer_value)

def check_permissions():
    if not frappe.has_permission('Vehicle', 'write'):
        frappe.throw('You do not have permission to update the odometer.')

def get_fleet_settings():
    return frappe.get_cached_doc('Fleet Settings', 'Fleet Settings')

def get_due_vehicles():
    """
    Send reminders for statutory compliance.
    if date is within the set number of days from today, send a reminder"""
    settings = get_fleet_settings()
    # get all vehicles where custom_send_email_reminders is not 'No' and any of the dates is within 14 days of today going forward
    due_date = frappe.utils.add_days(frappe.utils.nowdate(), settings.days_to_expiry or 14)
    if settings.pause_reminders == 1:
        return None, None

    vehicles = frappe.db.sql("""
        SELECT name, last_odometer, custom_send_emails, custom_road_tax_expiry_date, custom_fitness_expiry_date, custom_insurance_expiry_date
        FROM `tabVehicle`
        WHERE (custom_road_tax_expiry_date <= %s
        OR custom_fitness_expiry_date <= %s
        OR custom_insurance_expiry_date <= %s)
    """, (due_date, due_date, due_date), as_dict=1)

    return vehicles, due_date

def generate_vehicle_due_items_message(vehicles, due_date):
    message = """
    <div style="font-family: Arial, sans-serif; color: #333; max-width: 800px; margin: 0 auto; text-align: left;">
        <h1 style="color: #2c3e50; margin-bottom: 20px;">Compliance Items for Renewal</h1>
        <p style="color: #777; margin-top: 20px;  margin-bottom: 20px;">Please ensure all due items are renewed on time.</p>
        
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); min-width: 600px;">
                <thead>
                    <tr style="background-color: #f6f8fa;">
                        <th style="padding: 12px 15px; border-bottom: 1px solid #e1e4e8; text-align: left;">Vehicle</th>
                        <th style="padding: 12px 15px; border-bottom: 1px solid #e1e4e8; text-align: left;">Fitness</th>
                        <th style="padding: 12px 15px; border-bottom: 1px solid #e1e4e8; text-align: left;">Road Tax</th>
                        <th style="padding: 12px 15px; border-bottom: 1px solid #e1e4e8; text-align: left;">Insurance</th>
                    </tr>
                </thead>
                <tbody>
    """

    for i, v in enumerate(vehicles):
        # Alternate row colors for better readability
        row_color = "#ffffff" if i % 2 == 0 else "#f6f8fa"

        # Check and add fitness
        fitness = f"{v.custom_fitness_expiry_date}" if hasattr(v, 'custom_fitness_expiry_date') and v.custom_fitness_expiry_date <= due_date else "--"

        # Check and add road tax
        road_tax = f"{v.custom_road_tax_expiry_date}" if hasattr(v, 'custom_road_tax_expiry_date') and v.custom_road_tax_expiry_date <= due_date else "--"

        # Check and add insurance
        insurance = f"{v.custom_insurance_expiry_date}" if hasattr(v, 'custom_insurance_expiry_date') and v.custom_insurance_expiry_date <= due_date else "--"

        message += f"""
            <tr style="background-color: {row_color};">
                <td style="padding: 12px 15px; border-bottom: none;">{v.name}</td>
                <td style="padding: 12px 15px; border-bottom: none;">{fitness}</td>
                <td style="padding: 12px 15px; border-bottom: none;">{road_tax}</td>
                <td style="padding: 12px 15px; border-bottom: none;">{insurance}</td>
            </tr>
        """

    message += """
                </tbody>
            </table>
        </div>
        
        <style>
            @media (max-width: 600px) {
                table {
                    display: block;
                    width: 100%;
                    overflow-x: auto;
                }
                th, td {
                    white-space: nowrap;
                }
            }
        </style>
    </div>
    """

    return message

def get_recipients():
    """Return a list of recipients with roles `fleet manager` and `accounts manager`."""
    
    nested_recipient_list = get_users_based_on_role(("Fleet Manager", "Accounts Manager"))
    if nested_recipient_list: return [item for sublist in nested_recipient_list for item in sublist]
        

def get_users_based_on_role(roles):
    """Get information of all users that have been assigned this role
        :param roles is a tuple"""
    
    # SQL query to get users with the specified role
    query = """
        SELECT DISTINCT parent AS user_name
        FROM `tabHas Role`
        WHERE parent != 'Administrator' AND 
            role IN %s AND
            parenttype = 'User'
    """
    
    # Execute the query
    return frappe.db.sql(query, (roles,), as_list=1)

def send_compliance_reminders():
    """Send reminders for statutory compliance."""
    
    recipients = get_recipients()
    if not recipients:
        return

    vehicles, due_date = get_due_vehicles()
    if not due_date or not vehicles:
        return

    due_date = frappe.utils.getdate(due_date)

    fitness = []
    road_tax = []
    insurance = []
    
    for v in vehicles:
        if v.custom_fitness_expiry_date <= due_date:
            fitness.append(v)
        if v.custom_road_tax_expiry_date <= due_date:
            road_tax.append(v)
        if v.custom_insurance_expiry_date <= due_date:
            insurance.append(v)

    email_msg = generate_vehicle_due_items_message(vehicles, due_date)
    frappe.sendmail(recipients=recipients, subject="Vehicle Compliance Renewal Reminder", message=email_msg)

    """
    - get email recipients
    - settings
    
    """
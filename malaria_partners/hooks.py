app_name = "malaria_partners"
app_title = "Malaria Partners"
app_publisher = "Fabric"
app_description = "Custom applications for Malaria Partners Zambia"
app_email = "devs@thebantoo.com"
app_license = "mit"
required_apps = ["flex", "erpnext"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/malaria_partners/css/malaria_partners.css"
# app_include_js = "/assets/malaria_partners/js/malaria_partners.js"

# include js, css files in header of web template
# web_include_css = "/assets/malaria_partners/css/malaria_partners.css"
# web_include_js = "/assets/malaria_partners/js/malaria_partners.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "malaria_partners/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "malaria_partners/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "malaria_partners.utils.jinja_methods",
# 	"filters": "malaria_partners.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "malaria_partners.install.before_install"
# after_install = "malaria_partners.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "malaria_partners.uninstall.before_uninstall"
# after_uninstall = "malaria_partners.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "malaria_partners.utils.before_app_install"
# after_app_install = "malaria_partners.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "malaria_partners.utils.before_app_uninstall"
# after_app_uninstall = "malaria_partners.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "malaria_partners.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"malaria_partners.tasks.all"
# 	],
# 	"daily": [
# 		"malaria_partners.tasks.daily"
# 	],
# 	"hourly": [
# 		"malaria_partners.tasks.hourly"
# 	],
# 	"weekly": [
# 		"malaria_partners.tasks.weekly"
# 	],
# 	"monthly": [
# 		"malaria_partners.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "malaria_partners.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "malaria_partners.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "malaria_partners.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["malaria_partners.utils.before_request"]
# after_request = ["malaria_partners.utils.after_request"]

# Job Events
# ----------
# before_job = ["malaria_partners.utils.before_job"]
# after_job = ["malaria_partners.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"malaria_partners.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


fixtures = [    
    {
        "doctype": "Custom HTML Block",
        "filters": {
            "name": ["in", [
                "made in zambia",
                "easter_egg"
            ]]
        }        
    },
    {
        "doctype": "Custom DocPerm", 
        "filters": {
            "role": ["in", [
                "Director",
                "Employee Self Service",
                "Director Approver Level 1",
                "Director Approver Level 2",
                "Executive Director",
                "Projects Manager",
                "Projects User",
                "All Finance",
                "Volunteer",
                "All"
            ]]
        }           
    },
    {
        "doctype": "Property Setter",
        "filters": {
            "doc_type": ["in", [
                 "Salary Slip",
                 "Salary Structure Assignment",
                 "Employee",
                 "Project",
                 "Compensatory Leave Request"
            ]]
        }
    }
]
# "filters": [["role", "=", ""]]},
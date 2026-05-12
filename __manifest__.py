{
    "name": "Hospital Management",
    "version": "19.0.1.0.0",
    "category": "Hospital",
    "summary": "Hospital management",
    "author": "Igor Bagriy",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_hospital_doctor_views.xml",
        "views/hr_hospital_patient_views.xml",
        "views/hr_hospital_disease_views.xml",
        "views/hr_hospital_visit_views.xml",
        "views/hr_hospital_menus.xml",
    ],
    "demo": [
        "demo/hr_hospital_demo.xml",
            ],
    "installable": True,
    "application": True,
    'images':
        ['static/description/icon.png'],
}

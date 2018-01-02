#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe

def pre_process(contacts):
	return {
		'id': contacts["id"],
		'firstname': contacts["fields"]["all"]["firstname"],
		'lastname': contacts["fields"]["all"]["lastname"],
		'email': contacts["fields"]["all"]["email"]
	}

def post_process(remote_doc=None, local_doc=None, **kwargs):
	if not local_doc:
		return

	contacts = remote_doc
	erpnext_contact = local_doc
	if contacts:
		organization = contacts["fields"]["all"]["company"]
		if organization:
			if frappe.db.exists("Customer", organization):
				erpnext_contact.append("links",{"link_doctype": "Customer", "link_name": organization})
				erpnext_contact.save()
				frappe.db.commit()

			elif frappe.db.exists("Lead", dict(company_name=organization)):
				leadorg = frappe.get_doc("Lead", dict(company_name=organization))
				erpnext_contact.append("links",{"link_doctype": "Lead", "link_name": leadorg.name})
				erpnext_contact.save()
				frappe.db.commit()

			else:
				return


		else:
			if not frappe.db.exists("Lead", dict(email_id=contacts["fields"]["all"]["email"])):
				newlead = frappe.get_doc({
					'doctype': 'Lead',
					'lead_name': contacts["fields"]["all"]["firstname"] + " " + contacts["fields"]["all"]["lastname"],
					'email_id': contacts["fields"]["all"]["email"]
				}).insert(ignore_permissions=True)

				erpnext_contact.append("links",{"link_doctype": "Lead", "link_name": newlead.name})
				erpnext_contact.save()
				frappe.db.commit()

# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase


class TestSharedWebhookEventTable(IntegrationTestCase):
	def test_atlas_and_gateway_rows_coexist_and_filter_by_source(self):
		atlas_row = frappe.get_doc(
			{
				"doctype": "Webhook Event",
				"source": "Atlas",
				"event_id": "atlas-shared-test-1",
				"event_type": "vm.created",
				"status": "Received",
			}
		).insert(ignore_permissions=True)
		gateway_row = frappe.get_doc(
			{
				"doctype": "Webhook Event",
				"source": "Stripe",
				"event_id": "stripe-shared-test-1",
				"event_type": "payment_intent.succeeded",
				"status": "Received",
			}
		).insert(ignore_permissions=True)

		atlas_only = frappe.get_all("Webhook Event", filters={"source": "Atlas"}, pluck="name")
		gateway_only = frappe.get_all("Webhook Event", filters={"source": "Stripe"}, pluck="name")

		self.assertIn(atlas_row.name, atlas_only)
		self.assertNotIn(gateway_row.name, atlas_only)
		self.assertIn(gateway_row.name, gateway_only)
		self.assertNotIn(atlas_row.name, gateway_only)

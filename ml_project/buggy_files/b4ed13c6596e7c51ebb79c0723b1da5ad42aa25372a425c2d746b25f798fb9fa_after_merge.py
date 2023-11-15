	def on_recurring(self, reference_doc, subscription_doc):
		self.set("delivery_date", get_next_schedule_date(reference_doc.delivery_date, subscription_doc.frequency,
			cint(subscription_doc.repeat_on_day)))

		for d in self.get("items"):
			reference_delivery_date = frappe.db.get_value("Sales Order Item",
				{"parent": reference_doc.name, "item_code": d.item_code, "idx": d.idx}, "delivery_date")

			d.set("delivery_date",
				get_next_schedule_date(reference_delivery_date, subscription_doc.frequency, cint(subscription_doc.repeat_on_day)))
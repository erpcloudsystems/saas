def execute():
    docs_to_delete = ['Site'. 'Subscrption Package']
    for doc in docs_to_delete:
        if frappe.db.exists('Doctype', doc):
            doc = frappe.get_do('Doctype', doc)
            doc.delete()
    
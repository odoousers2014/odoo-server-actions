
# Execution : just once
# Update the records created after the create of some cutom fields (x_finalpartner_id, x_destinataire, x_categ_ids, x_titre and x_client_order_ref)

task_ids = context.get('active_ids')

for task in self.pool['project.task'].browse(cr, uid, task_ids, context=context):

    # prepare the values to update, since they are common for the SO and the invoice
    values = {}
    if task.x_client_order_ref:
        values['name'] = task.x_client_order_ref
    if task.x_finalpartner_id:
        values['x_finalpartner_id'] = task.x_finalpartner_id.id
    if task.x_destinataire:
        values['x_destinataire'] = task.x_destinataire.id
    if task.categ_ids:
        values['x_categ_ids'] = [(6, 0, [categ.id for categ in task.categ_ids])]

    # update the related account.invoice
    if task.x_invoice_id:
        self.pool['account.invoice'].write(cr, uid, task.x_invoice_id.id, values, context=context)

    # update the related sale.order
    SaleOrder = self.pool['sale.order']
    Invoice = self.pool['account.invoice']
    for sale in task.x_saleorder_ids:
        # clear values for SO : name is replace by client_order_ref in dict
        vals = values.copy()
        vals['client_order_ref'] = task.x_client_order_ref
        'name' in vals and vals.pop("name")
        SaleOrder.write(cr, uid, sale.id, vals, context=context)
        invoice_ids = Invoice.search(cr, uid, [('origin', '=', sale.name)], context=context)
        for invoice in Invoice.browse(cr, uid, invoice_ids, context=context):
            Invoice.write(cr, uid, invoice.id, values, context=context)


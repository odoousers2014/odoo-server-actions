# You can use the following variables:
#  - self: ORM model of the record on which the action is triggered
#  - object: Record on which the action is triggered if there is one, otherwise None
#  - pool: ORM model pool (i.e. self.pool)
#  - cr: database cursor
#  - uid: current user id
#  - context: current context
#  - time: Python time module
#  - workflow: Workflow engine
# If you plan to return an action, assign: action = {...}


# Execution : on creation of account.invoice
# Transfer x_finalpartner_id, x_destinataire, x_categ_ids, x_titre, x_partner_id, partner_shipping_id and name from the SO to the Invoice

if object.origin:
    sale_ids = self.pool['sale.order'].search(cr, uid, [('name', '=', object.origin)], context=context)
    if sale_ids:
        sale = self.pool['sale.order'].browse(cr, uid, sale_ids[0], context=context)
        values = {
            'x_partner_id' : sale.partner_id.id,
        }
        if sale.partner_shipping_id:
            values['x_partner_shipping_id'] = sale.partner_shipping_id
        if sale.x_titre:
            values['x_titre'] = sale.x_titre
        if sale.client_order_ref:
            values['name'] = sale.client_order_ref
        if sale.x_task_id:
            values['x_task_ids'] = [(4, sale.x_task_id.id)]
        if sale.x_finalpartner_id:
            values['x_finalpartner_id'] = sale.x_finalpartner_id.id
        if sale.x_destinataire:
            values['x_destinataire'] = sale.x_destinataire.id
        if sale.x_categ_ids:
            values['x_categ_ids'] = [(6, 0, [categ.id for categ in sale.x_categ_ids])]
        self.write(cr, uid, object.id, values, context=context)
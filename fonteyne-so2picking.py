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


# Execution : on creation on stock.picking
# When the SO is confirmed and a picking is created, need to move the content of x_remark on the  picking created, in the field "x_remark"
if object.origin:
    sale_ids = self.pool['sale.order'].search(cr, uid, [('name', 'like', object.origin)], context=context)
    if sale_ids:
        sale = self.pool['sale.order'].browse(cr, uid, sale_ids[0])
        self.write(cr, uid, object.id, {'x_remark' : sale.x_remark}, context=context)
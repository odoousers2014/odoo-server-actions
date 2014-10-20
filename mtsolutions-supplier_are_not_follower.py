# Execution : on creation of mail.follower
# if the new follower is a supplier, and this is a task follower, remove the object

if object.partner_id.supplier and object.res_model == 'project.task':
        object.unlink()
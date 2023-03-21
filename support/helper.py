
from .tasks import User, ticketEmailSend

def ticket_update_email(mailData, differences, request_user):

    if len(differences)>0:
        try:
            if 'support_agent' in differences:
                old_agent = differences['support_agent'][0]

                if old_agent:
                    data={}
                    data['subject'] = "Agent have been changed"

                    data['content'] = "You are not assigned in the ticket ( Ticket Name: " + mailData['title'] +", Ticket ID: "+ str(mailData['id']) + ",  anymore"
                    old_agent_object = User.objects.get(pk=old_agent)
                    data['users'] = [old_agent_object.email]
                    data['template_path'] = "email/template.html"

                    agentMailSendResult = ticketEmailSend.delay(data)

                new_agent = differences['support_agent'][1]
                if new_agent:
                    data={}
                    data['subject'] = "You are assigned to a ticket"
                    data['content'] = "You are now assigned in the ticket ( Ticket Name: " + mailData['title'] +", Ticket ID: "+ str(mailData["id"])
                    new_agent_object = User.objects.get(pk=new_agent)
                    data['users'] = [new_agent_object.email]
                    data['template_path'] = "email/template.html"

                    agentMailSendResult = ticketEmailSend.delay(data)
            
            else:
                data = {}
                data['subject'] = "A ticket have some changes."
                data['content'] = "Ticket Name: " + mailData['title'] +", Ticket ID: "+ str(mailData['id'])
                data['template_path'] = "email/template.html"

                is_admin = User.objects.filter(id=request_user.id, groups__name="admin").first()
                
                # request user is in admin group.

                if is_admin:
                    if 'approved_by' in mailData:
                        if mailData['approved_by'] is not None and 'email' in mailData['approved_by']:
                            data['users'] = [mailData['approved_by']['email']]
                        else:
                            data['users'] = [mailData['email']]

                else:
                    data['users'] = [mailData['email']]
                        
                # request user is in admin group.

                if 'priority' in differences:
                    data['content'] += " Priority of the ticket is changed from " + differences['priority'][0] + " to " + differences['priority'][1] +"."

                if 'status' in differences:
                    data['content'] += " Status of the ticket is changed from " + differences['status'][0] + " to " + differences['status'][1] +"."

                    clientEmailData = {}
                    clientEmailData['subject'] = "Status of you ticket updated"
                    clientEmailData['content'] = " Status of the ticket (Ticket Name: "+ mailData['title'] +") is changed from " + differences['status'][0] + " to " + differences['status'][1] +"."
                    clientEmailData['template_path'] = "email/template.html"
                    clientEmailData['users'] = [mailData['email']]

                    clientMailSendResult = ticketEmailSend.delay(data)

                if 'due_date' in differences:
                    data['content'] += " Due date of the ticket is changed from " + differences['due_date'][0] + " to " + differences['due_date'][1] +"."

                print("data",data)
                agentOrAdminMailSendResult = ticketEmailSend.delay(data)

                try:
                    status = agentOrAdminMailSendResult.get(timeout=30)
                except TimeoutError:
                    status = None

            print(differences)

        except Exception as e:
            print("hello error",str(e))
            return False
        else:
            return True
    else:
        return True



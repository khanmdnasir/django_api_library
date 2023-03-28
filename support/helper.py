from .tasks import *
from .models import TicketModel
from .serializers import TicketSerializer

def ticket_create_email(data):

    # send email to creator
    mailDataOfUser = {}
    mailDataOfUser['subject'] = "Your Ticket Have been created"
    mailDataOfUser['content'] = "Your Ticket's Content"
    mailDataOfUser['template_path'] = "email/template.html"
    mailDataOfUser['users'] = [data['email']]
    userResult = ticketEmailSend.delay(mailDataOfUser)

    # try:
    #     status = userResult.get(timeout=30)
    # except TimeoutError:
    #     status = None

    # send email to support agent
    if data["support_agent"] is not None:
        mailDataOfAgent = {}
        mailDataOfAgent['subject'] = "You are assigned to a ticket"
        mailDataOfAgent['content'] = "You are now assigned in the ticket ( Ticket Name: " + data['title'] +", Ticket ID: "+ str(data["id"])
        mailDataOfAgent['template_path'] = "email/template.html"
        new_agent_object = User.objects.get(pk=data['support_agent']['id'])
        mailDataOfAgent['users'] = [new_agent_object.email]

        agentResult = ticketEmailSend.delay(mailDataOfAgent)

    # send email to admins
    mailDataOfAdmins = {}
    all_admin = User.objects.filter(groups__name="admin").values('email')
    all_admins_email = [admin['email'] for admin in all_admin]
    mailDataOfAdmins['subject'] = "A Ticket Have been created"
    mailDataOfAdmins['content'] = "A Ticket's Content"
    mailDataOfAdmins['template_path'] = "email/template.html"
    mailDataOfAdmins['users'] = all_admins_email
    adminResult = ticketEmailSend.delay(mailDataOfAdmins)


def ticket_update_email(mailData, differences, request_user):

    if len(differences)>0:
        try:
            if 'support_agent' in differences:
                old_agent = differences['support_agent'][0]

                if old_agent:
                    data={}
                    data['subject'] = "Agent have been changed"

                    data['content'] = "You are not assigned in the ticket ( Ticket Name: " + mailData['title'] +", Ticket ID: "+ str(mailData['id']) + "), anymore"
                    old_agent_object = User.objects.get(pk=old_agent)
                    data['users'] = [old_agent_object.email]
                    data['template_path'] = "email/template.html"

                    agentMailSendResult = ticketEmailSend.delay(data)

                new_agent = differences['support_agent'][1]
                if new_agent:
                    data={}
                    data['subject'] = "You are assigned to a ticket"
                    data['content'] = "You are now assigned in the ticket ( Ticket Name: " + mailData['title'] +", Ticket ID: "+ str(mailData["id"]) + ")"
                    new_agent_object = User.objects.get(pk=new_agent)
                    data['users'] = [new_agent_object.email]
                    data['template_path'] = "email/template.html"

                    agentMailSendResult = ticketEmailSend.delay(data)
            
                if 'status' in differences:

                    clientEmailData = {}
                    clientEmailData['subject'] = "Status of you ticket updated"
                    clientEmailData['content'] = " Status of the ticket (Ticket Name: "+ mailData['title'] +") is changed from " + differences['status'][0] + " to " + differences['status'][1] +"."
                    clientEmailData['template_path'] = "email/template.html"
                    clientEmailData['users'] = [mailData['email']]

                    clientMailSendResult = ticketEmailSend.delay(clientEmailData)

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

                agentOrAdminMailSendResult = ticketEmailSend.delay(data)

                try:
                    status = agentOrAdminMailSendResult.get(timeout=30)
                except TimeoutError:
                    status = None

        except Exception as e:
            print("hello error",str(e))
            return False
        else:
            return True
    else:
        return True


def ticket_open_or_close_email(data):

    ticket_is_open = data['is_open']

    if ticket_is_open:
        subject = "Open request of the ticket (" + data['title'] +  ") is successfull"
        content = "Request to open the ticket (" + data['title'] +  ") is successfull"
    else:
        subject = "Close request of the ticket (" + data['title'] +  ") is successfull"
        content = "Request to close the ticket (" + data['title'] +  ") is successfull"

    mailDataOfUser = {}
    mailDataOfUser['subject'] = subject
    mailDataOfUser['content'] = content
    mailDataOfUser['template_path'] = "email/template.html"
    mailDataOfUser['users'] = [data['email']]
    userResult = ticketEmailSend.delay(mailDataOfUser)
        
    # send email to support agent
    if len(data['support_agent']) > 0:
        mailDataOfAdmins = {}

        mailDataOfAdmins['subject'] = "Ticket: " + data['title'] + "Ticket ID: " + str(data['id']) + ", is now " + ("open" if ticket_is_open else "close")

        mailDataOfAdmins['content'] = "You were assigned to a Ticket: " + data['title'] + "Ticket ID: " + str(data['id']) + ", is now " + ("open" if ticket_is_open else "close")

        mailDataOfAdmins['template_path'] = "email/template.html"
        mailDataOfAdmins['users'] = [data['support_agent']['email']]
        adminResult = ticketEmailSend.delay(mailDataOfAdmins)



def ticket_comment_email(data, request_user):

    ticket_instance = TicketModel.objects.get(pk=data['ticket_id'])
    ticket_serialized = TicketSerializer(instance=ticket_instance, many=False).data

    data['title'] = ticket_serialized['title']
    data['email'] = ticket_serialized['email']
    data['support_agent_email'] = ticket_serialized['support_agent']['email'] if ticket_serialized['support_agent'] else None
    data['approved_by_email'] = ticket_serialized['approved_by']['email'] if ticket_serialized['approved_by'] else None


    if not data['is_customer']:
        subject = "Support Agent commented on your ticket"
        content = "Support Agent wrote a comment on your ticket. Ticket: " + data['title'] + "Ticket ID: " + str(data['ticket_id'])

        mailDataOfUser = {}
        mailDataOfUser['subject'] = subject
        mailDataOfUser['content'] = content
        mailDataOfUser['template_path'] = "email/template.html"
        mailDataOfUser['users'] = [data['email']]
        userResult = ticketEmailSend.delay(mailDataOfUser)

    else:

        if data['support_agent_email']:
            mailDataOfAgent = {}

            mailDataOfAgent['subject'] = "Client commented on ticket" + data['title']

            mailDataOfAgent['content'] = "Mr. "+ str(request_user.email)+ " wrote a comment on Ticket: " + data['title'] + "Ticket ID: " + str(data['ticket_id'])

            mailDataOfAgent['template_path'] = "email/template.html"
            mailDataOfAgent['users'] = [data['support_agent_email']]
            agentResult = ticketEmailSend.delay(mailDataOfAgent)

                
        elif data['approved_by_email']:
            mailDataOfApprovedBy = {}

            mailDataOfApprovedBy['subject'] = "Client commented on ticket" + data['title']

            mailDataOfApprovedBy['content'] = "Mr. "+ str(request_user.email) + " wrote a comment on Ticket: " + data['title'] + "Ticket ID: " + str(data['ticket_id'])

            mailDataOfApprovedBy['template_path'] = "email/template.html"
            mailDataOfApprovedBy['users'] = [data['approved_by_email']]
            adminResult = ticketEmailSend.delay(mailDataOfApprovedBy)



def sendTicketDataToWebSocket(data, request_user):

    socketReceiversData = {
        "user":None,
        "agent":None,
        "admin":"admin",
    }

    ticket_creator = User.objects.filter(email=data['email']).first()
    
    if ticket_creator:
        socketReceiversData['user'] = str(data['email']).replace("@",'')

    if data["support_agent"]:
        socketReceiversData['agent'] = data['support_agent']['id']

    ticketSendToWebSocketResult = sendTicketToWebSocket.delay(socketReceiversData, data)



def sendTicketDetailsDataToWebSocket(ticketDetails):

    ticketSendToWebSocketResult = sendTicketDetailsToWebSocket.delay(ticketDetails)



def sendTicketCommentDataToWebSocket(comment):

    ticketSendToWebSocketResult = sendTicketCommentToWebSocket.delay(comment)

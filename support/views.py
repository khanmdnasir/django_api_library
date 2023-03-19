from rest_framework.views import APIView
from django.db import IntegrityError, transaction
from urllib import request, response
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets, pagination, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.forms.models import model_to_dict
from phonenumbers import format_number, PhoneNumberFormat
import json
from .customPermissionClasses import users_all_permission

from support.customPermissionClasses import CustomPermissionsCheck

# Create your views here.


class CustomPagination(pagination.PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'limit'
    def paginate_queryset(self, queryset, request, view=None):
        """Checking NotFound exception"""
        try:
            return super(CustomPagination, self).paginate_queryset(queryset, request, view=view)
        except NotFound:  # intercept NotFound exception
            return list()

    def get_paginated_response(self, data):
        try:
            next = self.page.next_page_number()
        except Exception as e:
            next = None
        try:
            previous = self.page.previous_page_number()
        except Exception as e:
            previous = None
        return Response({
            'next': next,
            'previous': previous,
            'current_page': self.page.number,
            'total_object': self.page.paginator.count,
            'total_page': self.page.paginator.num_pages,
            'results': data
        })
paginator = CustomPagination()

def compare_instances(instance1, instance2):
    # get the fields of the model
    fields = instance1.keys()

    # create a dictionary to store the differences
    differences = {}

    # iterate over the fields and compare the values of the two instances
    for field in fields:
        value1 = instance1[field]
        value2 = instance2[field]
        if value1 != value2:
            differences[field] = (value1, value2)

    # return the differences dictionary
    return differences


class IssueTypesViewSet(viewsets.ModelViewSet):
    queryset = IssueTypesModel.objects.all()
    serializer_class = IssueTypesSerializer
    pagination_class = CustomPagination


    def retrieve(self, request, pk):
        try:
            ticket = IssueTypesModel.objects.filter(pk=pk, is_active = True).first()
            if ticket:
                serializer = TicketSerializer(instance=ticket, many=False)
                newData = serializer.data
                return Response({"success": True, "result": newData})
            else:
                return Response({"success": False, "result": "Issue Type Does Not Found"})
        except Exception as e:
            return Response({"success": False, "error": str(e)})

    def list(self, request):
        queryset = IssueTypesModel.objects.filter(is_active=True).all()

        if self.request.query_params.get('limit') is None or self.request.query_params.get('limit') == '0':
            serializer = IssueTypesSerializer(queryset, many=True)
            return Response({'results': serializer.data})
        else:
            page = self.paginate_queryset(queryset)
            serializer = IssueTypesSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def create(self, request):
        try:
            data = request.data
            data['created_by'] = request.user.id
            serializer = IssueTypesSerializer(data={**data})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            return Response({"success": False, "error": list(serializer.errors.values())[0][0]})
        else:
            return Response({"success": True, "data": serializer.data})

    def partial_update(self, request, pk):
        try:
            instance = IssueTypesModel.objects.filter(id=pk, is_active=True).first()
            data = request.data
            data['updated_by'] = request.user.id
            if instance:
                try:
                    serializer = IssueTypesSerializer(
                        instance=instance, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except Exception as e:
                    return Response({"success": False, "error": list(serializer.errors.values())[0][0]})
            else:
                return Response({"success": False, "error": "Issue Type Does Not Exist!"})
        except Exception as e:
            return Response({"success": False, "error": "Issue Type not found!"})
        else:
            return Response({"success": True, "data": serializer.data})

    def destroy(self, request, pk):
        try:
            instance = IssueTypesModel.objects.filter(id=pk, is_active=True).first()
            if instance:
                ticket = instance.ticket.filter(is_active=True).all()

                if len(ticket) > 0:
                    return Response({"success": False, "error": "This Issue Type has related ticket data. You are not allowed to delete this!"})
                else:
                    instance.updated_by = request.user
                    instance.is_active = False
                    instance.save()
            else:
                return Response({"success": False, "error": "Issue Type Does Not Exist!"})
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})



class TicketViewSet(viewsets.ModelViewSet):
    queryset = TicketModel.objects.filter(is_active=True).all()
    serializer_class = TicketSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create','retrieve']:
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    def retrieve(self, request, pk):
        try:
            ticket = TicketModel.objects.filter(pk=pk, is_active = True).first()
            if ticket:
                serializer = TicketSerializer(instance=ticket, many=False)
                newData = serializer.data
                comments = []
                tickete_details = ticket.ticket_comments.filter(is_active=True).all()
                for details in tickete_details:
                    details_serialize = TicketCommentsSerializer(instance=details, many=False)
                    comments.append(details_serialize.data)
                newData['comments'] = comments

                return Response({"success": True, "result": newData})
            else:
                return Response({"success": False, "result": "Ticket Does Not Found"})
        except Exception as e:
            return Response({"success": False, "error": str(e)})

    def list(self, request):
        queryset = TicketModel.objects.filter(is_active=True).all()
        agent_id = request.query_params.get('agent_id') if request.query_params else None

        if agent_id:
            queryset = TicketModel.objects.filter(
                is_active=True, support_agent=agent_id).all()
            page = self.paginate_queryset(queryset)
            serializer = TicketSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        elif self.request.query_params.get('limit') is None or self.request.query_params.get('limit') == '0':
            serializer = TicketSerializer(queryset, many=True)
            return Response({'results': serializer.data})

        else:
            page = self.paginate_queryset(queryset)
            serializer = TicketSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def create(self, request):
        try:
            data = request.data

            data['is_open'] = True
            data['is_active'] = True
            data['status'] = "pending"
            data['priority'] = None
            data['due_date'] = None


            data['is_registered_user'] = request.user.is_authenticated

            if request.user.is_authenticated:
                data['email'] = request.user.email
                data['phone'] = request.user.phone

            data['support_agent'] = data['support_agent'] if 'support_agent' in data else None
            data['support_agent_id'] = data['support_agent'] if 'support_agent' in data else None
            data['approved_by'] = data['approved_by'] if 'approved_by' in data else None
            data['approved_by_id'] = data['approved_by'] if 'approved_by' in data else None

            serializer = TicketSerializer(data={**data})
            serializer.is_valid(raise_exception=True)

            try:
                with transaction.atomic():
                    ticket = serializer.save()
                    ticket_id = ticket.id
                    # signal for storing log and send email
                    print("create ticket",ticket_id)

            except IntegrityError:
                transaction.set_rollback(True)

        except Exception as e:
            print(str(e))
            return Response({"success": False, "error": str(e)})
        else:
            newData = serializer.data

            return Response({"success": True, "data": newData})

    def partial_update(self, request, pk):
        try:
            instance = TicketModel.objects.filter(id=pk, is_active=True).first()
            if instance:
                try:
                    previous_instance = model_to_dict(instance)

                    data = request.data

                    data['support_agent_id'] = data['support_agent'] if 'support_agent' in data else (instance.support_agent.id if instance.support_agent != None else None)

                    data['approved_by_id'] = data['approved_by'] if 'approved_by' in data else (instance.support_agent.id if instance.approved_by != None else None)

                    serializer = self.get_serializer(
                        instance=instance, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    try:
                        with transaction.atomic():
                            ticket = serializer.save()
                            ticket_id = ticket.id

                            differences = compare_instances(previous_instance, model_to_dict(ticket))
                            
                            users_permissions = list(request.user.get_all_permissions())
                            if "phone" in differences:
                                previous_phone_number = differences['phone'][0]
                                prev_phone_number_string = str(format_number(previous_phone_number, PhoneNumberFormat.E164)) if previous_phone_number is not None else previous_phone_number
                                new_phone_number = differences['phone'][1]
                                new_phone_number_string = str(format_number(new_phone_number, PhoneNumberFormat.E164))
                                differences['phone'] = (prev_phone_number_string, new_phone_number_string)
                            
                            if "due_date" in differences:
                                previous_due_date = differences['due_date'][0].strftime('%Y-%m-%d') if differences['due_date'][0] is not None else differences['due_date'][0]
                                new_due_date = differences['due_date'][1].strftime('%Y-%m-%d')
                                differences['due_date'] = (previous_due_date, new_due_date)
                            
                            # check permissions for changing important data
                            if "support_agent" in differences:
                                if 'support.can_assign_support_agent' not in users_permissions:
                                    return Response({"success": False, "error": "You don't have permission to change support agent"})
                            if "status" in differences:
                                if 'support.can_change_ticket_status' not in users_permissions:
                                    return Response({"success": False, "error": "You don't have permission to change status"})
                            if "priority" in differences:
                                if 'support.can_change_ticket_priority' not in users_permissions:
                                    return Response({"success": False, "error": "You don't have permission to change priority"})
                            if "due_date" in differences:
                                if 'support.can_change_ticket_due_date' not in users_permissions:
                                    return Response({"success": False, "error": "You don't have permission to change due_date"})
                            
                            if "is_open" in differences:
                                if ticket.is_open:
                                    if 'support.can_open_closed_ticket' not in users_permissions:
                                        return Response({"success": False, "error": "You don't have permission to change due_date"}) 
                                else:
                                    if 'support.can_close_ticket' not in users_permissions:
                                        return Response({"success": False, "error": "You don't have permission to change due_date"}) 

                            # print('differences',differences)
                            # differences_txt = json.dumps(differences) dict to json
                            # signal for storing log and send email


                    except IntegrityError:
                        transaction.set_rollback(True)
                except Exception as e:
                    print(str(e))
                    return Response({"success": False, "error": list(serializer.errors.values())[0][0]})
            else:
                return Response({"success": False, "error": "Ticket Does Not Exist!"})
        except Exception as e:
            return Response({"success": False, "error": str(e)})
        else:
            newData = serializer.data
            return Response({"success": True, "data": newData})

    def destroy(self, request, pk):
        try:
            instance = TicketModel.objects.filter(id=pk, is_active=True).first()
            if instance:
                try:
                    with transaction.atomic():
                        instance.updated_by = request.user
                        instance.is_open = False
                        instance.is_active = False
                        instance.save()
                        # signal for storing log and send email
                        print("delete ticket",instance.id)
                except IntegrityError:
                    transaction.set_rollback(True)
            else:
                return Response({"success": False, "error": "Ticket Does Not Exist!"})
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})


class CloseOrOpenTicketApi(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            data = request.data
            users_permissions = list(request.user.get_all_permissions())
            id = request.query_params.get('id')
            ticket = TicketModel.objects.filter(pk=id, is_active=True).first()

            if "request_to_open" not in data:
                return Response({"success": False, "error": "request_to_open data is required!"})

            if data['request_to_open']:

                if ticket.is_open:
                    return Response({"success": False, "data": "The ticket was already opened"})
                

                if 'support.can_open_closed_ticket' not in users_permissions:
                    return Response({"success": False, "error": "You don't have permission to open the closed ticket"})

                ticket.is_open = True
                ticket.save()
                return Response({"success": True, "data": "Ticket has opened Successfully from closed."})

            elif not data['request_to_open']:
                request_user_email = request.user.email
                ticket_creators_email = ticket.email

                if not ticket.is_open:
                    return Response({"success": True, "data": "The ticket was already closed"})
                
                if ('support.can_close_ticket' not in users_permissions) and request_user_email!=ticket_creators_email:
                    return Response({"success": False, "error": "You don't have permission to close the ticket"})

                ticket.is_open = False
                ticket.save()
                return Response({"success": True, "data": "The ticket closed successfully"})

        except Exception as e:
            return Response({"success": False, "error": str(e)})




class TicketCommentsViewSet(viewsets.ModelViewSet):
    queryset = TicketModel.objects.all()
    serializer_class = TicketCommentsSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()

    def retrieve(self, request, pk):
        try:
            ticket_comment = TicketCommentsModel.objects.filter(pk=pk, is_active = True).first()

            if ticket_comment:
                serializer = self.get_serializer(instance=ticket_comment, many=False)
                newData = serializer.data
                return Response({"success": True, "result": newData})
            else:
                return Response({"success": False, "result": "Ticket Does Not Found"})
        except Exception as e:
            return Response({"success": False, "error": str(e)})

    def list(self, request):
        queryset = TicketCommentsModel.objects.filter(is_active=True).all()
        ticket_id = request.query_params.get('ticket_id') if request.query_params else None

        if ticket_id:
            queryset = TicketCommentsModel.objects.filter(
                is_active=True, ticket_id=ticket_id).all()

            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        elif self.request.query_params.get('limit') is None or self.request.query_params.get('limit') == '0':
            serializer = self.get_serializer(queryset, many=True)
            return Response({'results': serializer.data})

        else:
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def create(self, request):
        try:
            data = request.data

            data['author_id'] = data['author']

            serializer = self.get_serializer(data={**data})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # signal to ticket_comments_task
        except Exception as e:
            print(str(e))
            return Response({"success": False, "error": str(e)})
        else:
            newData = serializer.data

            return Response({"success": True, "data": newData})

    def partial_update(self, request, pk):
        try:
            instance = TicketCommentsModel.objects.filter(id=pk, is_active=True).first()
            if instance:
                try:
                    data = request.data
                    user_id = request.user.id
                    data['updated_by'] = user_id

                    serializer = self.get_serializer(
                        instance=instance, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except Exception as e:
                    print(str(e))
                    return Response({"success": False, "error": list(serializer.errors.values())[0][0]})
            else:
                return Response({"success": False, "error": "Ticket Comments Does Not Exist!"})
        except Exception as e:
            return Response({"success": False, "error": str(e)})
        else:
            newData = serializer.data
            return Response({"success": True, "data": newData})

    def destroy(self, request, pk):
        try:
            instance = TicketCommentsModel.objects.filter(id=pk, is_active=True).first()
            if instance:
                try:
                    with transaction.atomic():
                        instance.updated_by = request.user
                        instance.is_active = False
                        instance.save()
                except IntegrityError:
                    transaction.set_rollback(True)
            else:
                return Response({"success": False, "error": "Ticket Comments Does Not Exist!"})
        except Exception as e:
            return Response({"success": False, "error": "Delete unsuccesful"})
        else:
            return Response({"success": True, "data": "Deleted Successfully"})



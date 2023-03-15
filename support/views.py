from rest_framework.views import APIView
from django.db import IntegrityError
from urllib import request, response
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets, pagination, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

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


class IssueTypesViewSet(viewsets.ModelViewSet):
    queryset = IssueTypesModel.objects.all()
    serializer_class = IssueTypesSerializer
    pagination_class = CustomPagination


class TicketViewSet(viewsets.ModelViewSet):
    queryset = TicketModel.objects.all()
    serializer_class = TicketSerializer
    pagination_class = CustomPagination

    def retrieve(self, request, pk):
        try:
            ticket = TicketModel.objects.filter(pk=pk, is_active = True).first()
            if ticket:
                serializer = TicketSerializer(instance=ticket, many=False)
                newData = serializer.data
                items = []
                tickete_details = ticket.ticket_comments.filter(is_active=True).all()
                for details in tickete_details:
                    details_serialize = TicketCommentsSerializer(instance=details, many=False)
                    items.append(details_serialize.data)
                newData['items'] = items

                return Response({"success": True, "result": newData})
            else:
                return Response({"success": False, "result": "Invoice Does Not Found"})
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

    # def create(self, request):
    #     try:

    #         data = request.data
    #         data['currency_id'] = data['currency'] if 'currency' in data else None
    #         serializer = InvoiceSerializer(data={**data})
    #         serializer.is_valid(raise_exception=True)
    #         items = []
    #         try:
    #             with transaction.atomic():
    #                 invoice = serializer.save()
    #                 invoice_id = invoice.id
    #                 for invoice_details in all_items:
    #                     invoice_details['invoice_id'] = invoice_id
    #                     invoice_details['created_by'] = user_id
    #                     invoice_details['account_id_id'] = invoice_details['account_id']
    #                     item_serializer = InvoiceDetailsSerializer(data={**invoice_details})
    #                     item_serializer.is_valid(raise_exception=True)
    #                     item_serializer.save()
    #                     items.append(item_serializer.data)
    #         except IntegrityError:
    #             transaction.set_rollback(True)

    #     except Exception as e:
    #         print(str(e))
    #         return Response({"success": False, "error": str(e)})
    #     else:
    #         newData = serializer.data
    #         newData['items'] = items
    #         return Response({"success": True, "data": newData})

    # def partial_update(self, request, pk):
    #     try:
    #         instance = Invoice.objects.filter(id=pk, is_active=True).first()
    #         data = request.data
    #         user_id = request.user.id
    #         data['updated_by'] = user_id
    #         all_items = data['items']
    #         newItems = data['new_items']
    #         deleteItems = data['deleted_items']
    #         data['contact_id_id'] = data['contact_id'] if 'contact_id' in data else instance.contact_id.id
    #         data['currency_id'] = data['currency'] if 'currency' in data else None
    #         items = []
    #         if instance:
    #             try:
    #                 serializer = InvoiceSerializer(
    #                     instance=instance, data=data, partial=True)
    #                 serializer.is_valid(raise_exception=True)
    #                 try:
    #                     with transaction.atomic():
    #                         invoice = serializer.save()
    #                         invoice_id = invoice.id
    #                         for invoice_details in all_items:
    #                             invoice_details['updated_by'] = user_id
    #                             invoice_details['account_id_id'] = invoice_details['account_id']
    #                             invoiceDetailsInstance = InvoiceDetails.objects.filter(is_active=True, id=invoice_details['id'], invoice_id=invoice_id).first()
    #                             item_serializer = InvoiceDetailsSerializer( instance=invoiceDetailsInstance,
    #                                                                         data={**invoice_details}, partial=True)
    #                             item_serializer.is_valid(raise_exception=True)
    #                             item_serializer.save()
    #                             items.append(item_serializer.data)

    #                         for create_item in newItems:
    #                             create_item['invoice_id'] = invoice_id
    #                             create_item['created_by'] = user_id
    #                             create_item['account_id_id'] = create_item['account_id']
    #                             new_item_serializer = InvoiceDetailsSerializer(
    #                                 data={**create_item})
    #                             new_item_serializer.is_valid(raise_exception=True)
    #                             new_item_serializer.save()
    #                             items.append(new_item_serializer.data)

    #                         for delete_item in deleteItems:
    #                             invoiceDetailsDeleteInstance = InvoiceDetails.objects.filter(
    #                                 is_active=True, id=delete_item, invoice_id=invoice_id).first()
    #                             if invoiceDetailsDeleteInstance:
    #                                 invoiceDetailsDeleteInstance.updated_by = request.user
    #                                 invoiceDetailsDeleteInstance.is_active = False
    #                                 invoiceDetailsDeleteInstance.save()

    #                 except IntegrityError:
    #                     transaction.set_rollback(True)
    #             except Exception as e:
    #                 print(str(e))
    #                 return Response({"success": False, "error": list(serializer.errors.values())[0][0]})
    #         else:
    #             return Response({"success": False, "error": "Invoice Does Not Exist!"})
    #     except Exception as e:
    #         return Response({"success": False, "error": str(e)})
    #     else:
    #         newData = serializer.data
    #         newData['items'] = items
    #         return Response({"success": True, "data": newData})

    # def destroy(self, request, pk):
    #     try:
    #         instance = Invoice.objects.filter(id=pk, is_active=True).first()
    #         if instance:
    #             try:
    #                 with transaction.atomic():
    #                     instance.updated_by = request.user
    #                     invoiceAllDetails = instance.invoice_details.all()
    #                     for details in invoiceAllDetails:
    #                         details.is_active = False
    #                         details.save()
    #                     instance.is_active = False
    #                     instance.save()
    #             except IntegrityError:
    #                 transaction.set_rollback(True)
    #         else:
    #             return Response({"success": False, "error": "Invoice Does Not Exist!"})
    #     except Exception as e:
    #         return Response({"success": False, "error": "Delete unsuccesful"})
    #     else:
    #         return Response({"success": True, "data": "Deleted Successfully"})



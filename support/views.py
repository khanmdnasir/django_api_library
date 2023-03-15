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


class IssueTypeViewSet(viewsets.ModelViewSet):
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


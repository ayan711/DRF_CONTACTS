from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,GenericAPIView
from .models import Contact
from .serializers import ContactSerializer,ContactFilter
from rest_framework import permissions
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

class ContactList(ListCreateAPIView):

    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        # logging.info(vars(self))
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)


class ContactDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)
    
class ContactSearch(GenericAPIView):
    
    "Search contacts by name/number"
    permission_classes = (permissions.IsAuthenticated,)
    
    # queryset = Contact.objects.all()
    # serializer_class = ContactSerializer
    # filter_class = ContactFilter
    
    
    def get(self, request):
        
        logging.warn('self -            -----------')
        logging.info(vars(self.request))
        data = request.data
        
        number = data.get('number','')
        name = data.get('name', '')
        
        if len(number) != 0:
            
            res = Contact.objects.filter(phone_number__contains=number,owner=self.request.user)
            logging.info(res)
            
            serializer = ContactFilter(res.values())
            logging.info(serializer.data)


            data = {'data': serializer.data,'success':True}

            return Response(data, status=status.HTTP_200_OK)
        
        if len(name) != 0:
            
            res = Contact.objects.filter(first_name__icontains=name,owner=self.request.user)
            
            serializer = ContactFilter(res.values())
            logging.info(serializer.data)


            data = {'data': serializer.data,'success':True}

            return Response(data, status=status.HTTP_200_OK)

            # SEND RES
        return Response({'detail': 'Error','success':False }, status=status.HTTP_401_UNAUTHORIZED)
        

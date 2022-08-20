from rest_framework.serializers import ModelSerializer
from .models import Contact
import django_filters

class ContactSerializer(ModelSerializer):

    class Meta:
        model = Contact

        fields = ['country_code', 'id', 'first_name', 'last_name', 'phone_number',
                  'contact_picture', 'is_favorite'
                  ]

class ContactFilter(django_filters.FilterSet):
    class Meta:
        model = Contact
        fields = {
            'phone_number': ['contains']
        }
        # together = ['first_name', 'last_name']
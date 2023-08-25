from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from studiomanagerapi.models import Gear, Engineer, Category

class GearView(ViewSet):
    """Studio Manager gear typesview"""

    def retrieve(self, request, pk):
        """Gets gear by its pk

        Returns:
            Response --  single JSON serialized gear dictionary
        """
        gear = Gear.objects.get(pk=pk)
        serializer = GearSerializer(gear)
        return Response(serializer.data)

    def list(self, request):
        """Gets all gear

        Returns:
            Response -- JSON serialized list of gear
        """
        gear = Gear.objects.all()
        """filter by engineer id"""
        engineer = request.query_params.get('engineer_id', None)
        if engineer is not None:
                gear = gear.filter(engineer_id=engineer)
        """filter by category id"""
        category = request.query_params.get('category_id', None)
        if category is not None:
                gear = gear.filter(category_id=category)
        """serialize all list requests"""
        serializer = GearSerializer(gear, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handles POST operations

        Returns:
            Response -- JSON serialized gear instance
        """
        engineer = Engineer.objects.get(pk=request.data["engineerId"])
        category = Category.objects.get(pk=request.data["categoryId"])
        gear = Gear.objects.create(
            model=request.data["model"],
            brand=request.data["brand"],
            category_id=category,
            engineer_id=engineer,
        )
        serializer = GearSerializer(gear)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handles PUT requests for gear

        Returns:
            Response -- Empty body with 204 status code
        """
        gear = Gear.objects.get(pk=pk)
        gear.model=request.data["model"]
        gear.brand=request.data["brand"]
        engineer = Engineer.objects.get(pk=request.data["engineerId"])
        gear.engineer = engineer
        category = Category.objects.get(pk=request.data["categoryId"])
        gear.category = category
        gear.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handles DELETE requests for gear

        Returns:
            Response -- Empty body with 204 status code
        """
        gear = Gear.objects.get(pk=pk)
        gear.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class GearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gear
        fields = ('id', 'model', 'brand', 'category_id', 'engineer_id')
        depth: 1

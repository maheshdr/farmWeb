from django.shortcuts import render
from .models import Tree
from django.db.models import Q  # <-- Import this for proper OR filtering

def home(request):
    q = request.GET.get("q", "").lower()
    filter_val = request.GET.get("filter", "").lower()

    # Fetch all trees
    trees = Tree.objects.all()

    # Apply search query
    if q:
        trees = trees.filter(
            Q(name__icontains=q) | Q(desc__icontains=q)  # Correct usage of OR condition
        )

    # Apply filter by type
    if filter_val:
        trees = trees.filter(type__iexact=filter_val)

    return render(request, "trees/home.html", {"trees": trees})


# api 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tree
from .serializers import TreeSerializer

@api_view(['GET'])
def tree_list(request):
    trees = Tree.objects.all()
    serializer = TreeSerializer(trees, many=True)
    return Response(serializer.data)

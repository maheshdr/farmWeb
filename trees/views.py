from django.shortcuts import render
from .models import Tree  # Import model directly

def home(request):
    q = request.GET.get("q", "").lower()
    filter_val = request.GET.get("filter", "").lower()

    # Fetch all trees from the database
    trees = Tree.objects.all()

    # Apply search query if exists
    if q:
        trees = trees.filter(name__icontains=q) | trees.filter(desc__icontains=q)

    # Apply filter by type if exists
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

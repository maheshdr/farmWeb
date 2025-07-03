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
            Q(plantName__icontains=q) | Q(description__icontains=q)  # Correct usage of OR condition
        )

    # Apply filter by type
    if filter_val:
        trees = trees.filter(type__iexact=filter_val)

    return render(request, "trees/home.html", {"trees": trees})


# api 
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
import os
from django.conf import settings

from .models import Tree
from .serializers import TreeSerializer

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])  # To handle image uploads
def tree_list(request):
    if request.method == 'GET':
        trees = Tree.objects.all()
        serializer = TreeSerializer(trees, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TreeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def tree_detail(request, pk):
    tree = get_object_or_404(Tree, pk=pk)

    if request.method == 'GET':
        serializer = TreeSerializer(tree)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TreeSerializer(tree, data=request.data, partial=True)
        if serializer.is_valid():
            # If image is being replaced, delete the old one
            if 'image' in request.data and tree.image:
                old_image_path = tree.image.path
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if tree.image and os.path.isfile(tree.image.path):
            os.remove(tree.image.path)

        tree.delete()
        return Response({"message": "Tree deleted"}, status=status.HTTP_204_NO_CONTENT)

# trees/curd operation
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tree
from .forms import TreeForm

def tree_admin_list(request):
    trees = Tree.objects.all()
    return render(request, 'trees/admin_list.html', {'trees': trees})

def tree_create(request):
    if request.method == 'POST':
        form = TreeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tree_admin_list')
    else:
        form = TreeForm()
    return render(request, 'trees/tree_form.html', {'form': form, 'action': 'Create'})

def tree_update(request, pk):
    tree = get_object_or_404(Tree, pk=pk)
    if request.method == 'POST':
        form = TreeForm(request.POST, request.FILES, instance=tree)
        if form.is_valid():
            form.save()
            return redirect('tree_admin_list')
    else:
        form = TreeForm(instance=tree)
    return render(request, 'trees/tree_form.html', {'form': form, 'action': 'Update'})

def tree_delete(request, pk):
    tree = get_object_or_404(Tree, pk=pk)
    if request.method == 'POST':
        if tree.imageUrl:
            tree.imageUrl.delete()
        tree.delete()
        return redirect('tree_admin_list')
    return render(request, 'trees/tree_confirm_delete.html', {'tree': tree})

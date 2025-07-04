import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Tree
from .forms import TreeForm
from .serializers import TreeSerializer

# DRF imports
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status


# ------------------------------
# 🌿 Web Views
# ------------------------------

def home(request):
    """Displays all trees with optional search and filter functionality."""
    q = request.GET.get("q", "").lower()
    filter_val = request.GET.get("filter", "").lower()
    trees = Tree.objects.all()

    if q:
        trees = trees.filter(Q(plantName__icontains=q) | Q(description__icontains=q))
    if filter_val:
        trees = trees.filter(plantType__iexact=filter_val)

    return render(request, "trees/home.html", {"trees": trees})


def tree_admin_list(request):
    """Admin list view of all trees."""
    trees = Tree.objects.all()
    return render(request, 'trees/admin_list.html', {'trees': trees})


def tree_create(request):
    """Create a new tree record."""
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
    old_image = tree.imageUrl

    if request.method == 'POST':
        form = TreeForm(request.POST, request.FILES, instance=tree)

        clear_image = request.POST.get('imageUrl-clear', False)
        new_image = request.FILES.get('imageUrl', None)

        if form.is_valid():
            # Case 1: User uploaded a new image
            if new_image:
                if old_image and hasattr(old_image, 'path') and os.path.isfile(old_image.path):
                    os.remove(old_image.path)

            # Case 2: User wants to clear the image (checkbox checked)
            elif clear_image and old_image:
                if hasattr(old_image, 'path') and os.path.isfile(old_image.path):
                    os.remove(old_image.path)
                tree.imageUrl = None  # Clear the field manually

            form.save()
            return redirect('tree_admin_list')
    else:
        form = TreeForm(instance=tree)

    return render(request, 'trees/tree_form.html', {'form': form, 'action': 'Update'})



def tree_delete(request, pk):
    """Delete a tree record and its associated image."""
    tree = get_object_or_404(Tree, pk=pk)

    if request.method == 'POST':
        if tree.imageUrl:
            image_path = tree.imageUrl.path
            if os.path.isfile(image_path):
                os.remove(image_path)
        tree.delete()
        return redirect('tree_admin_list')

    return render(request, 'trees/tree_confirm_delete.html', {'tree': tree})


# ------------------------------
# 🌿 REST API Views
# ------------------------------

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def tree_list(request):
    """GET all trees, or POST to create a new tree via API."""
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
    """GET, PUT, or DELETE a specific tree record via API."""
    tree = get_object_or_404(Tree, pk=pk)

    if request.method == 'GET':
        serializer = TreeSerializer(tree)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if 'imageUrl' in request.data and tree.imageUrl:
            old_image_path = tree.imageUrl.path
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

        serializer = TreeSerializer(tree, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if tree.imageUrl:
            image_path = tree.imageUrl.path
            if os.path.isfile(image_path):
                os.remove(image_path)
        tree.delete()
        return Response({"message": "Tree deleted"}, status=status.HTTP_204_NO_CONTENT)

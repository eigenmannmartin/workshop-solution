from django.shortcuts import render, get_object_or_404
from django.forms import modelformset_factory
from todos.models import Todo, Collection
from rest_framework import viewsets
from rest_framework import permissions
from todos.serializers import CollectionSerializer, TodoSerializer


def collection(request, id):
    # Filter by owner and id
    collection = get_object_or_404(Collection, pk=id, owner=request.user)

    TodoFormSet = modelformset_factory(
        Todo,
        fields=(
            'description',
            'done',
        ),
        can_delete=True,
        can_delete_extra=False,
        can_order=True,
    )

    queryset = Todo.objects.filter(collection=collection.pk)

    if request.method == 'POST':
        formset = TodoFormSet(request.POST, request.FILES, queryset=queryset)
        if formset.is_valid():
            for new_todo in formset.save(commit=False):
                new_todo.collection = collection
                new_todo.save()

            for obj in formset.deleted_objects:
                if obj.pk:
                    obj.delete()

            formset = TodoFormSet(queryset=queryset)
    else:
        formset = TodoFormSet(queryset=queryset)
    return render(request, 'collection.html', {
                  "formset": formset, "collection": collection})


def index(request):

    CollectionFormSet = modelformset_factory(
        Collection,
        fields=(
            'name',
        ),
        can_delete=True,
        can_delete_extra=False,
        can_order=False,
    )

    # Filter by owner
    if request.user.is_authenticated:
        queryset = Collection.objects.filter(owner=request.user)
    else:
        queryset = Collection.objects.none()

    if request.method == 'POST':
        formset = CollectionFormSet(
            request.POST, request.FILES, queryset=queryset)
        if formset.is_valid():
            for new_collection in formset.save(commit=False):
                new_collection.owner = request.user
                new_collection.save()
            for obj in formset.deleted_objects:
                if obj.pk:
                    obj.delete()

            formset = CollectionFormSet(queryset=queryset)
    else:
        formset = CollectionFormSet(queryset=queryset)

    return render(request, 'index.html', {"formset": formset})


class CollectionViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TodoViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(collection__owner=self.request.user)

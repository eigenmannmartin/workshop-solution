from django.shortcuts import render, get_object_or_404
from django.forms import modelformset_factory
from todos.models import Todo, Collection


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

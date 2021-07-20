from todos.models import Collection, Todo
from rest_framework import serializers


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='todo-detail')

    class Meta:
        model = Todo
        fields = [
            'id',
            'url',
            'description',
            'created',
            'modified',
            'done',
            'collection']

    def get_fields(self):
        fields = super(TodoSerializer, self).get_fields()
        fields['collection'].queryset = Collection.objects.filter(
            owner=self.context['request'].user)
        return fields


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='collection-detail')
    todos = serializers.SerializerMethodField()

    def get_todos(self, collection):
        return TodoSerializer(collection.todos, many=True, context={
                              "request": self.context['request']}).data

    class Meta:
        model = Collection
        fields = ['id', 'url', 'name', 'created', 'modified', 'todos']

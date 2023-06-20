from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cat, Owner
from .serializers import CatSerializer, OwnerSerializer, CatListSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    # Пишем метод, а в декораторе разрешим работу со списком объектов
    # и переопределим URL на более презентабельный
    @action(detail=False, url_path='recent-white-cats')
    def recent_white_cats(self, request):
        # Нужны только последние пять котиков белого цвета
        cats = Cat.objects.filter(color='White')[:5]
        # Передадим queryset cats сериализатору
        # и разрешим работу со списком объектов
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        # Если запрошенное действие (action) —
        # получение списка объектов ('list')
        if self.action == 'list':
            # ...то применяем CatListSerializer
            return CatListSerializer
        # А если запрошенное действие — не 'list', применяем CatSerializer
        return CatSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


# Чтобы самостоятельно создать базовый вьюсет с особым набором действий —
# нужно унаследовать его от одного или нескольких миксинов с нужными
# действиями и, дополнительно, от базового класса GenericViewSet
# ===
# Собираем вьюсет, который будет уметь изменять или удалять отдельный объект.
# А ничего больше он уметь не будет.
class UpdateDeleteViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    pass


"""
В DRF есть пять предустановленных классов миксинов, они соответствуют пяти
операциям с данными:

    CreateModelMixin — создать объект (для обработки запросов POST);
    ListModelMixin — вернуть список объектов (для обработки запросов GET);
    RetrieveModelMixin — вернуть объект (для обработки запросов GET);
    UpdateModelMixin — изменить объект (для обработки запросов PUT и PATCH);
    DestroyModelMixin — удалить объект (для обработки запросов DELETE).

Опишем собственный базовый класс вьюсета: он будет создавать экземпляр объекта
и получать экземпляр объекта; назовём его CreateRetrieveViewSet
"""


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    # В теле класса никакой код не нужен! Пустячок, а приятно.
    pass


class LightCatViewSet(CreateRetrieveViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

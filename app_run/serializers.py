from django.contrib.auth.models import User
from rest_framework import serializers
from app_run.models import Run, AthleteInfo, Challenge, Position, CollectibleItem, Subscribe


class CollectibleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectibleItem
        fields = ('id', 'name', 'uid', 'value', 'latitude', 'longitude', 'picture')


# serializer to api/runs nested serializer
class UserBasicSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name')


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserBasicSerializers(read_only=True, source='athlete')

    class Meta:
        model = Run
        fields = ('id', 'created_at', 'athlete', 'comment', 'status', 'distance', 'athlete_data', 'run_time_seconds',
                  'speed')


# serializer to api/users
class UserSerializers(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()  # type - вычисляемое поле
    runs_finished = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished')

        # Метод для вычисления поля type

    def get_type(self, obj):
        return 'coach' if obj.is_staff else 'athlete'


class UserCollectibleItemSerializers(UserSerializers):
    items = CollectibleItemSerializer(many=True, source='collectible_items')

    class Meta(UserSerializers.Meta):
        model = User
        fields = UserSerializers.Meta.fields + ('items',)


class AthleteInfoViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AthleteInfo
        fields = ('user_id', 'goals', 'weight')


class ChallengeSerializer(serializers.ModelSerializer):
    athlete = serializers.IntegerField(source='athlete.user.id', read_only=True)

    class Meta:
        model = Challenge
        fields = ('full_name', 'athlete')


class PositionSerializer(serializers.ModelSerializer):
    run = serializers.PrimaryKeyRelatedField(queryset=Run.objects.all().select_related('athlete'))
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    date_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f')

    class Meta:
        model = Position
        fields = ('run', 'latitude', 'longitude', 'date_time', 'speed', 'distance')

    def validate_run(self, value):
        if value.status != 'in_progress':
            raise serializers.ValidationError('Забег должен быть в статусе "in progress"')
        return value

    def validate_latitude(self, value):
        if float(value) < -90.0 or float(value) > 90.0:
            raise serializers.ValidationError("Широта должна находиться в диапазоне от -90.0 до +90.0 градусов")
        return value

    def validate_longitude(self, value):
        if float(value) < -180.0 or float(value) > 180.0:
            raise serializers.ValidationError("Долгота должна находиться в диапазоне от -180.0 до +180.0 градусов")
        return value


